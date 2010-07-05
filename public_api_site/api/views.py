# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import simplejson as json
import time

# TODO: Refactor Cassandra code into the model
import pycassa

def true_time(x):
    end_of_days = time.mktime((2012,12,31,0,0,0,0,0,0))
    return time.asctime(time.localtime((end_of_days*1e6-int(x))/1e6))

def speakers(request):
    client = pycassa.connect()
    speakers = pycassa.ColumnFamily(client, 'HOPE2008', 'Speakers')
    
    if request.REQUEST.has_key('speaker'):
        speaker = request.REQUEST['speaker']

        # FIXME: speakers.get(speaker) doesn't work...
        #        TODO: switch to speakers.multiget
        speakers = speakers.get_range(speaker, row_count=1)
        results = "\n".join(json.dumps({"speaker" : speaker,
                                    "name" : s[1]['name']}) for s in speakers)
    else:
        results = json.dumps(list(speakers.get_range()))
        
    return HttpResponse(results, mimetype='text/plain')

def users(request):
    client = pycassa.connect()
    users = pycassa.ColumnFamily(client, 'HOPE2008', 'Users')

    # Display a specific user profile
    if request.REQUEST.has_key('id'):
        user = request.REQUEST['id']

        # FIXME: speakers.get(speaker) doesn't work...
        #        TODO: switch to speakers.multiget
        users = users.get_range(user, row_count=1)
        results = "\n".join(json.dumps({"user" : user,
                                        "name" : u[1]['name'],
                                        "x" : u[1]['x'],
                                        "y" : u[1]['y'],
                                        "interests" : u[1]['interests']}) for u in users )
    # Display all user profiles
    else:
        results = json.dumps(list(users.get_range()))
    return HttpResponse(results, mimetype='text/plain')

def locations(request):
    client = pycassa.connect()
    location_history = pycassa.ColumnFamily(client, 'HOPE2008', 'LocationHistory', super=True)

    prefix = "["
    postfix = "]"

    limit = 10

    if request.REQUEST.has_key('jsoncallback'):
       prefix = request.REQUEST['jsoncallback'] + "(" + prefix
       postfix = postfix + ")"

    if request.REQUEST.has_key('limit'):
        _limit = request.REQUEST['limit']
        if _limit.isdigit() and int(_limit) < 20:
            limit = int(_limit)

    # Display the last 10 locations a specific user checked in
    if request.REQUEST.has_key('user'):
        user = request.REQUEST['user']
        last_n =  list(location_history.get_range(row_count=limit))
        res = "\n".join(json.dumps({"user" : user, 
                                    "x" : r[1][user]['x'], 
                                    "y" : r[1][user]['y'], 
                                    # "area" : r[1][user]['area'], 
                                    # "button" : r[1][user]['button'], 
                                    "time" : true_time(r[0])}) for r in last_n)
    # Display the current location of all users
    else:
        lastseen = location_history.get_range(row_count=1).next()[1]
        res = "\n".join(json.dumps({"user" : user, 
                                    "x" : lastseen[user]['x'],
                                    "y" : lastseen[user]['y']}) for user in lastseen)
    return HttpResponse(res,mimetype='text/plain')

def talks(request):
    client = pycassa.connect()
    # TODO: Create indices for each talk type
    talks = pycassa.ColumnFamily(client, 'HOPE2008', 'Talks')

    # Display a specific talk
    if request.REQUEST.has_key('title'):
        title = request.REQUEST['title']
        # FIXME: talks.get(title) doesn't work...
            #        TODO: switch to talks.multiget
            #        TODO: can we do talks.get_partial_match ?
        talk =  list(talks.get_range(row_count=1))
        results = "\n".join(json.dumps({"speakers" : t[1][title]['speakers'],
                                        "title" : title, 
                                        "abstract" : t[1][title]['abstract'], 
                                        "time" : t[1][title]['time'], 
                                        "track" : t[1][title]['track'], 
                                        "interests" : t[1][title]['interests']}) for t in talk) 
    # Display all talks
    else:
        results = json.dumps(list(talks.get_range()))
        
    return HttpResponse(results,mimetype='text/plain')
   
def stats(request):
    results = "Statistics here"
    return HttpResponse(results, mimetype='text/plain')

def interests(request):
    # TODO: factor into model or read from file and use urls.py
    interests = ["new tech", "activism", "radio", "lockpicking", "crypto", "privacy", "ethics", "telephones",
    "social engineering", "hacker spaces", "hardware hacking", "nostalgia", "communities",
    "science", "government", "network security", "malicious software", "pen testing", "web",
    "niche hacks", "media"]

    return HttpResponse(json.dumps(interests), mimetype='text/plain')

def default(request):
    return HttpResponseRedirect("http://amd.hope.net/openamd_api_1.1.1.html")

#def testing(request):
     # NOTE: this is bad, just make more indices and then intersect them
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

