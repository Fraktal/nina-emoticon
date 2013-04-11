#! /usr/bin/python

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
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

#mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweetDB']


#group by tweet_text_emoticon from mongo
reducer = Code("""
                   function(obj, prev){
                     prev.count++;
                   }
                   """)
tweet_smiley_mongo = db.tweets.group(key={"tweet_text_smiley":1}, condition={}, initial={"count": 0}, 
                                             reduce=reducer)

tweet_smiley = ' '.join([str(json.dumps(tweet["tweet_text_smiley"])) for tweet in tweet_smiley_mongo])

print tweet_smiley

f_smiley = open("smiley.txt", "wb") 
pickle.dump(tweet_smiley, f_smiley)
f_smiley.close()

word_smiley = {} 

words_gen_smiley = "".join(str((word.strip(punctuation).lower() for line in open('smiley.txt') 
                                             for word in line.split())))

f = open("smiley_text.txt", "wb") 
pickle.dump(words_gen_smiley, f)
f.close()

test = str(open('smiley_text.txt', 'rb').readlines())

tag_smiley = make_tags(get_tag_counts(tweet_smiley), maxsize=90)

create_tag_image(tag_smiley, 'smiley_emoticon.png', size=(900, 600), fontname='Philosopher',
                 background=(32, 35, 105, 255))

#word cloud image
#webbrowser.open('smiley_emoticon.png') 