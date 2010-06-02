# encoding: utf-8 
""" Sample Cassandra Client """

import pycassa
import time, pprint, math, json

def dist(a,b):
    return float(a[0])*float(b[0]) + float(a[1])*float(b[1])

def true_time(x):
    end_of_days = time.mktime((2012,12,31,0,0,0,0,0,0))
    return time.asctime(time.localtime((end_of_days*1e6-int(x))/1e6))

def main():
    client = pycassa.connect()
    
    keyspace = "HOPE2008" 
    timestamp = time.time() 
    
    lh = pycassa.ColumnFamily(client, keyspace, 'LocationHistory',super=True)
        
    # Last users seen
    lastseen = lh.get_range(row_count=1).next()[1]
    for user in lastseen:
        print(user,lastseen[user])

    # Closest agent to user "x"
    user2loc = {}
    for r in lastseen:
        user2loc[r] = (lastseen[r]['x'],lastseen[r]['y'])
    print min(user2loc,key=lambda x : dist(user2loc["user7"],user2loc[x]))

    # Last 10 places user "x" was
    last_10 =  list(lh.get_range(row_count=10))
    for r in last_10:
        print("user7 was %s at %s" % (r[1]['user7'], true_time(r[0])))

if __name__ == '__main__':
  main()
