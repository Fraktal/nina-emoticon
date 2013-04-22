#! /usr/bin/python

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
tweet_smiley_mongo = db.tweets.group(key={"tweet_text_smiley":1, "location_smiley":1}, condition={}, 
                                           initial={"count": 0}, reduce=reducer)

tweet_sad_mongo = db.tweets.group(key={"tweet_text_sad":1, "location_sad":1}, condition={}, 
                                        initial={"count": 0}, reduce=reducer)

tweet_neutral_mongo = db.tweets.group(key={"tweet_text_neutral":1, "location_neutral":1}, condition={},
                                            initial={"count": 0},reduce=reducer)



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

fname ="sad"
tweet_sad = ' '.join([str(json.dumps(tweet["tweet_text_sad"], tweet["location_sad"])) 
                          for tweet in tweet_sad_mongo])
dtstr = str(datetime.now())
dtstr = dtstr.replace(' ','_')
dtstr = dtstr.split('.')
fn = "%s_%s.txt"%(fname,dtstr[0])
f = open(fn,"wb")
pickle.dump(tweet_sad,f)
f.close()

fname ="neutral"
tweet_neutral = ' '.join([str(json.dumps(tweet["tweet_text_neutral"], tweet["location_neutral"])) 
                              for tweet in tweet_neutral_mongo])
dtstr = str(datetime.now())
dtstr = dtstr.replace(' ','_')
dtstr = dtstr.split('.')
fn = "%s_%s.txt"%(fname,dtstr[0])
f = open(fn,"wb")
pickle.dump(tweet_neutral,f)
f.close()



#file for sorting top words
f_smiley = open("smiley.txt", "wb") 
pickle.dump(tweet_smiley, f_smiley)
f_smiley.close()

f_sad = open("sad.txt", "wb") 
pickle.dump(tweet_sad, f_sad)
f_sad.close()

f_neutral = open("neutral.txt", "wb") 
pickle.dump(tweet_neutral, f_neutral)
f_neutral.close()



#sorting tweet_text for top N most frequent words             
N = 2000
word_smiley = {} 
word_sad = {}
word_neutral = {}

words_gen_smiley = (word.strip(punctuation).lower() for line in open('smiley.txt') 
                                                    for word in line.split())

words_gen_sad = (word.strip(punctuation).lower() for line in open('sad.txt') 
                                                    for word in line.split())

words_gen_neutral = (word.strip(punctuation).lower() for line in open('neutral.txt') 
                                                    for word in line.split())

for word in words_gen_smiley:
    word_smiley[word] = word_smiley.get(word, 0) + 1

for word in words_gen_sad:
    word_sad[word] = word_sad.get(word, 0) + 1

for word in words_gen_neutral:
    word_neutral[word] = word_neutral.get(word, 0) + 1        

top_words_smiley = sorted(word_smiley.iteritems(), key=itemgetter(1), reverse=True)[:N]

top_words_sad = sorted(word_sad.iteritems(), key=itemgetter(1), reverse=True)[:N]

top_words_neutral = sorted(word_neutral.iteritems(), key=itemgetter(1), reverse=True)[:N]



#saving frequent words by curent time and date
fname ="freq_words_smiley"
freq_word_smiley = ' '.join([str(word) for word in top_words_smiley])
dtstr = str(datetime.now())
dtstr = dtstr.replace(' ','_')
dtstr = dtstr.split('.')
fn = "%s_%s.csv"%(fname,dtstr[0])
f = open(fn,"wb")
pickle.dump(freq_word_smiley,f)
f.close()

fname ="freq_words_sad"
freq_word_sad = ' '.join([str(word) for word in top_words_sad])
dtstr = str(datetime.now())
dtstr = dtstr.replace(' ','_')
dtstr = dtstr.split('.')
fn = "%s_%s.csv"%(fname,dtstr[0])
f = open(fn,"wb")
pickle.dump(freq_word_sad,f)
f.close()

fname ="freq_words_neutral"
freq_word_neutral = ' '.join([str(word) for word in top_words_neutral])
dtstr = str(datetime.now())
dtstr = dtstr.replace(' ','_')
dtstr = dtstr.split('.')
fn = "%s_%s.csv"%(fname,dtstr[0])
f = open(fn,"wb")
pickle.dump(freq_word_neutral,f)
f.close()