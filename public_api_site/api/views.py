# Create your views here.
from django.http import HttpResponse
import simplejson as json
import time

# Not the most elegant of way. Cassandra code should go into the model.
# I have placed into all in one file for your own clarity. Refactor once you get up to speed.
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
    lh = pycassa.ColumnFamily(client, 'HOPE2008', 'LocationHistory',super=True)
    pr = map(lambda x:x[0], lh.get_range(row_count=100))

    if filtering == "true":
        # FIXME: it hangs here...
        # pr = None
        for key in keys:
            if request.REQUEST.has_key(key):
                    datum = request.REQUEST[key]
                    r = lh.get_range(super_column=key)
                    r = set(map(lambda x:x[0], filter(lambda x:x[1] == datum,r)))
                    if pr == None:
                        pr = r
                    else:
                        pr = pr.intersect(r)
                    break

    string = "\n".join(pr)
    return HttpResponse(filtering, mimetype='text/plain')

def users(request):
    client = pycassa.connect()
    lh = pycassa.ColumnFamily(client, 'HOPE2008', 'LocationHistory',super=True)

    # Check if they want a specific user
    if request.REQUEST.has_key('user'):
        user = request.REQUEST['user']
        x = request.REQUEST['x']
        y = request.REQUEST['y']
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

