import sys
import random
import time

import pycassa

# gaussian random movement
# biased movement towards subset of people
# biased movement towards subset of places

agents = 20
rounds = 1e5

regions = []

lower_bounds = 0
upper_bounds = 50

names = ["Jacob","Emma","Michael","Isabella","Ethan","Emily","Joshua",
         "Madison","Daniel","Ava","Alexander","Olivia","Anthony",
         "Sophia","William","Abigail","Christopher","Elizabeth",
         "Matthew","Chloe"]

end_of_days = time.mktime((2012,12,31,0,0,0,0,0,0))

def main():
    client = pycassa.connect()

    lh = pycassa.ColumnFamily(client, 'HOPE2008', 'LocationHistory',super=True)
    un = pycassa.ColumnFamily(client, 'HOPE2008', 'Users')
        
    locations = [lower_bounds]*agents*2
        
    print "Start %s" % time.time()
    for i in xrange(rounds):
        key = {}
        locations = [x+random.gauss(0,1) for x in locations]
        for i,l in enumerate(locations):
            if l > upper_bounds:
                locations[i] = 2*upper_bounds-l
            if l < lower_bounds:
                locations[i] = 2*lower_bounds-l
        for x in range(agents):
            user = "user"+str(x)
            key[user] = {'x' : str(locations[2*x]),
                         'y' : str(locations[2*x+1])}           
        lh.insert(str(int(end_of_days*1e6-time.time()*1e6)),key)

    print "End %s" % time.time()

    for x in range(agents):
        user = "user"+str(x)
        un.insert(user,{ "name" : names[x%agents]})

if __name__ == '__main__':
    main()
