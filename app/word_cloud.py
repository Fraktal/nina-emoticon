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



#Mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweetDB']


#grouping tweet_text from mongo
reducer = Code("""
                   function(obj, prev){
                     prev.count++;
                   }
                   """)
tweets = db.tweets.group(key={"tweet_text":1}, condition={}, initial={"count": 0}, reduce=reducer)


#saving to pickle file to be used in word cloud
tweets = ' '.join([str(json.dumps(tweet["tweet_text"])) for tweet in tweets])
f = open("smiley.pickle", "wb") 
pickle.dump(tweets, f)
f.close()
#print tweets	 


#sorting tweet_text for top 200 most frequent words
N = 200
words = {}

words_gen = (word.strip(punctuation).lower() for line in open('smiley.pickle') 
                                             for word in line.split())
                                          
for word in words_gen:
    words[word] = words.get(word, 0) + 1

top_words = sorted(words.iteritems(), key=itemgetter(1), reverse=True)[:N]

for word, frequency in top_words:
	#print " %s [%d]" % (word, frequency)
    print word


#saving sorted words into a pickle file to build word cloud 
freq_word = open("cloud.pickle", "wb") 
pickle.dump(word, freq_word)
f.close()   

contents = pickle.load(open('cloud.pickle', "rb")) 


#build word cloud
tags = make_tags(get_tag_counts(contents), maxsize=80)

create_tag_image(tags, 'tweet_data_smiley.png', size=(900, 600), fontname='Lobster')


#word cloud image
webbrowser.open('tweet_data_smiley.png') 