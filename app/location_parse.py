# Extract geo coordinates from search results

import sys, time
import webbrowser 
import pymongo
from pymongo import Connection  
from bson import BSON
from bson.json_util import dumps
from bson import Code
from bson.son import SON
import json
import cPickle as pickle
import simplejson
from string import punctuation
from operator import itemgetter
import operator, time, string
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import nltk
from datetime import datetime

#mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweetDB']


#group by tweet_text_emoticon from mongo
reducer = Code("""
                   function(obj, prev){
                     prev.count++;
                   }
                   """)
tweet_smiley_mongo = db.tweets.group(key={"tweet_text_smiley":1, "location_smiley":1}, 
                                          condition={}, initial={"count": 0}, reduce=reducer)

tweet_smiley = ' '.join([str(json.dumps(tweet["tweet_text_smiley"], tweet["location_smiley"])) 
                             for tweet in tweet_smiley_mongo])

print tweet['location_smiley']

#saving tweet_text_emoticon to text file to be used in word cloud and graphs
fname ="smiley"
tweet_smiley = ' '.join([str(json.dumps(tweet["tweet_text_smiley"], tweet["location_smiley"])) 
                             for tweet in tweet_smiley_mongo])
dtstr = str(datetime.now())
dtstr = dtstr.replace(' ','_')
dtstr = dtstr.split('.')
fn = "%s_%s.txt"%(fname,dtstr[0])
f = open(fn,"wb")
pickle.dump(tweet_smiley,f)
f.close()

tweets = []

for line in tweet_smiley:
  try: 
    tweets.append(json.loads(fn))
  except:
    pass


# Extract geocoordinates from tweets in search results

coords =  [ tweet['location_smiley']['geo'] for tweet in tweets if tweet['location_smiley'] is not None ]

print coords