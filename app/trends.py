# -*- coding: utf-8 -*-

import os
import sys
import datetime 
from datetime import timedelta
import time
import json
import twitter 
from time import strftime

t = twitter.Twitter(domain='api.twitter.com', api_version='1')

if not os.path.isdir('data/trends_data'):
        os.makedirs('data/trends_data')

while True:
    
    fname = "trends"
    dtstr = str(datetime.datetime.now())
    dtstr = dtstr.replace(' ','_') 
    dtstr = dtstr.split('.')
    fn = "%s_%s.txt"%(fname,dtstr[0])

    trends = json.dumps(t.trends._(1)(), indent=1)

    f = open(os.path.join(os.getcwd(), 'data', 'trends_data', fn), 'w')
    f.write(trends)
    f.close()

    update_time = (datetime.datetime.now() + datetime.timedelta(hours=+1)).strftime("%H:%M:%S")

    print >> sys.stderr, "file created: ", f.name
    print >> sys.stderr, "Next update: ", update_time

    time.sleep(3600) # 1 hour between captures