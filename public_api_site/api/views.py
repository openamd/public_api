# Create your views here.
from django.http import HttpResponse
import simplejson as json
import time

# TODO: Refactor Cassandra code into the model
import pycassa

def true_time(x):
    end_of_days = time.mktime((2012,12,31,0,0,0,0,0,0))
    return time.asctime(time.localtime((end_of_days*1e6-int(x))/1e6))

def speakers(request):
    client = pycassa.connect()
    sp = pycassa.ColumnFamily(client, 'HOPE2008', 'Speakers')
    last_7 = list(sp.get_range(row_count=7))
    res = "\n".join(json.dumps(speaker) for speaker in last_7 )
    return HttpResponse(res,mimetype='text/plain')

def talks(request):
    string = "Talks here"
    return HttpResponse(string, mimetype='text/plain')
    
def interests(request):
    string = "Interests here"
    return HttpResponse(string, mimetype='text/plain')

def stats(request):
    string = "Statistics here"
    return HttpResponse(string, mimetype='text/plain')

def locations(request):
    keys = ["user","x","y"]
    filtering = "false"
    for key in keys:
        if request.REQUEST.has_key(key):
            filtering = "true"

    client = pycassa.connect()
    location_history = pycassa.ColumnFamily(client, 'HOPE2008', 'LocationHistory',super=True)

    if filtering == "false":
        results =  location_history.get_range(row_count=100)
    else:
        results = None
        # FIXME: it hangs here...
        # results = map(lambda x:x[0], location_history.get_range(row_count=100))
        for key in keys:
            if request.REQUEST.has_key(key):
                    datum = request.REQUEST[key]
                    # TODO: s/range/rows
                    range = location_history.get_range(super_column=key)
                    range = set(map(lambda x:x[0], filter(lambda x:x[1] == datum,range)))
                    if results == None:
                        results = range
                    else:
                        results = results.intersect(range)
                    break

        string = "\n".join(results)
    return HttpResponse(results, mimetype='text/plain')

def users(request):
    client = pycassa.connect()
    lh = pycassa.ColumnFamily(client, 'HOPE2008', 'LocationHistory',super=True)

    # Check if they want a specific user
    if request.REQUEST.has_key('user'):
        user = request.REQUEST['user']
        last_10 =  list(lh.get_range(row_count=10))
        res = "\n".join(json.dumps({"user" : user, 
                                    "x" : r[1][user]['x'], 
                                    "y" : r[1][user]['y'], 
                                    "time" : true_time(r[0])}) for r in last_10)
    # Otherwise the current locations of all the users
    else:
        lastseen = lh.get_range(row_count=1).next()[1]
        res = "\n".join(json.dumps({"user" : user, 
                                    "x" : lastseen[user]['x'],
                                    "y" : lastseen[user]['y']}) for user in lastseen)
    return HttpResponse(res,mimetype='text/plain')

