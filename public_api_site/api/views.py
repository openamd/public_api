# Create your views here.
from django.http import HttpResponse
import simplejson as json
import time

# TODO: Refactor Cassandra code into the model
import pycassa

def true_time(x):
    end_of_days = time.mktime((2012,12,31,0,0,0,0,0,0))
    return time.asctime(time.localtime((end_of_days*1e6-int(x))/1e6))

def users(request):
    client = pycassa.connect()
    users = pycassa.ColumnFamily(client, 'HOPE2008', 'Users')

    # Check if they want a specific user
    if request.REQUEST.has_key('id'):
        user = request.REQUEST['id']
        users = users.get_range(user, row_count=1)

        res = "\n".join(json.dumps({"user" : user,
                                    "name" : u[1]['name']}) for u in users )
    # Otherwise dump all profiles
    else:
        res = json.dumps(list(users.get_range()))
    return HttpResponse(res,mimetype='text/plain')

def locations(request):
    client = pycassa.connect()
    lh = pycassa.ColumnFamily(client, 'HOPE2008', 'LocationHistory', super=True)

    # Check if they want a specific user
    if request.REQUEST.has_key('user'):
        user = request.REQUEST['user']
        last_10 =  list(lh.get_range(row_count=10))
        res = "\n".join(json.dumps({"user" : user, 
                                    "x" : r[1][user]['x'], 
                                    "y" : r[1][user]['y'], 
                                    "area" : r[1][user]['area'], 
                                    "button" : r[1][user]['button'], 
                                    "time" : true_time(r[0])}) for r in last_10)
    # Otherwise the current locations of all the users
    else:
        lastseen = lh.get_range(row_count=1).next()[1]
        res = "\n".join(json.dumps({"user" : user, 
                                    "x" : lastseen[user]['x'],
                                    "y" : lastseen[user]['y']}) for user in lastseen)
    return HttpResponse(res,mimetype='text/plain')

#def huhnow(request):
#    client = pycassa.connect()
#
#    # TODO: s/LocationHistory/LocationHistoryByUser
#    location_history = pycassa.ColumnFamily(client, 'HOPE2008', 'LocationHistory',super=True)
#
#    # TODO: switch to multiget so we can query users=bob,johnny
#    if request.REQUEST.has_key(index):
#        history = location_history.get_range(request.REQUEST[index])
#    else:
#        history = location_history.get_range(row_count=100)
#
#    # filter by any keys we have
#    for key in keys:
#        if request.REQUEST.has_key(key):
#           history = filter(lambda row:row[1][key] == request.REQUEST[key], history)
#
#    return HttpResponse("\n".join(str(history)), mimetype='text/plain')

#def speakers(request):
#    client = pycassa.connect()
#    sp = pycassa.ColumnFamily(client, 'HOPE2008', 'Speakers')
#    last_7 = list(sp.get_range(row_count=7))
#    res = "\n".join(json.dumps(speaker) for speaker in last_7 )
#    return HttpResponse(res,mimetype='text/plain')

#def talks(request):
#    indices = [ "speaker", "interest" ]
#    string = "Talks here"
#    return HttpResponse(string, mimetype='text/plain')
    
#def interests(request):
#    string = "Interests here"
#    return HttpResponse(string, mimetype='text/plain')

#def stats(request):
#    string = "Statistics here"
#    return HttpResponse(string, mimetype='text/plain')

