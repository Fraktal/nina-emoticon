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
from numpy.random import normal
import matplotlib.pyplot as plt
from numpy.random import normal
import numpy as np


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

tweet_sad_mongo = db.tweets.group(key={"tweet_text_sad":1}, condition={}, initial={"count": 0}, 
                                        reduce=reducer)

tweet_neutral_mongo = db.tweets.group(key={"tweet_text_neutral":1}, condition={}, initial={"count": 0}, 
                                            reduce=reducer)


#saving tweet_text_emoticon to pickle file to be used in word cloud and histogram
tweet_smiley = ' '.join([str(json.dumps(tweet["tweet_text_smiley"])) for tweet in tweet_smiley_mongo])
tweet_sad = ' '.join([str(json.dumps(tweet["tweet_text_sad"])) for tweet in tweet_sad_mongo])
tweet_neutral = ' '.join([str(json.dumps(tweet["tweet_text_neutral"])) for tweet in tweet_neutral_mongo])

f_smiley = open("smiley.pickle", "wb") 
pickle.dump(tweet_smiley, f_smiley)
f_smiley.close()

f_sad = open("sad.pickle", "wb") 
pickle.dump(tweet_sad, f_sad)
f_sad.close()

f_neutral = open("neutral.pickle", "wb") 
pickle.dump(tweet_neutral, f_neutral)
f_neutral.close()
#print tweet_smiley	 


#sorting tweet_text for top 200 most frequent words
N = 200
word_smiley = {} 
word_sad = {} 
word_neutral = {} 

words_gen_smiley = (word.strip(punctuation).lower() for line in open('smiley.pickle') 
                                             for word in line.split())

words_gen_sad = (word.strip(punctuation).lower() for line in open('sad.pickle') 
                                             for word in line.split())

words_gen_neutral = (word.strip(punctuation).lower() for line in open('neutral.pickle') 
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

for word in top_words_smiley:
	word 
     

for word in top_words_sad:
    word  

for word in top_words_neutral:
    word          

#saving sorted words into a pickle file containing words and frequency of occurence 
import csv
hist_smile= open("hist_smiley.csv", "wb")
wtr= csv.writer(hist_smile)
for word in top_words_smiley :
    aRow= [ word, top_words_smiley]
    wtr.writerow( aRow )
hist_smile.close()

with open('hist_smiley.csv') as f:
  v = np.loadtxt(f, delimiter=",", dtype='float', comments="#", skiprows=1, usecols=None)

v_hist = np.ravel(v)   # 'flatten' v
fig = plt.figure()
ax1 = fig.add_subplot(111)

n, bins, patches = ax1.hist(v_hist, bins=50, normed=1, facecolor='green')
plt.show()  

#gaussian_numbers = normal(size=1000)
#plt.hist(x, bins=10, normed=True, cumulative=True)
#plt.title("Frequency Distribution of Words")
#plt.xlabel("Words")
#plt.ylabel("Frequency")
#plt.show()