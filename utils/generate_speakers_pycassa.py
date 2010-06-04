import sys
import random
import time

import pycassa

names = ["Jacob","Emma","Michael","Isabella","Ethan","Emily","Joshua",
         "Madison","Daniel","Ava","Alexander","Olivia","Anthony",
         "Sophia","William","Abigail","Christopher","Elizabeth",
         "Matthew","Chloe"]
bios = ["fisherman", "whaler", "the chin", "solider", "sailor", "candlestickmaker",
	"butcher", "baker", "CHOPCHOP" ]

end_of_days = time.mktime((2012,12,31,0,0,0,0,0,0))

def main():
    client = pycassa.connect()

    sp = pycassa.ColumnFamily(client, 'HOPE2008', 'Speakers')
        
    print "Start %s" % time.time()

    for name in names:
    	sp.insert( name, { "bio" : bios[int(random.randint(0,len(bios)-1))] } )
    
    print "End %s" % time.time()

if __name__ == '__main__':
    main()
