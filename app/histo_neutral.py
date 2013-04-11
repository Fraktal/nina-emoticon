#! /usr/bin/python

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



#mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweetDB']


#group by tweet_text_emoticon from mongo
reducer = Code("""
                   function(obj, prev){
                     prev.count++;
                   }
                   """)
tweet_neutral_mongo = db.tweets.group(key={"tweet_text_neutral":1}, condition={}, initial={"count": 0}, 
	                                         reduce=reducer)




#saving tweet_text_emoticon to pickle file to be used in word cloud and histogram
tweet_neutral = ' '.join([str(json.dumps(tweet["tweet_text_neutral"])) for tweet in tweet_neutral_mongo])

f_neutral = open("neutral_histo.pickle", "wb") 
pickle.dump(tweet_neutral, f_neutral)
f_neutral.close()



#sorting tweet_text for top 200 most frequent words             
N = 2000
word_neutral = {} 

words_gen_neutral = (word.strip(punctuation).lower() for line in open('neutral_histo.pickle') 
                                                    for word in line.split())

for word in words_gen_neutral:
    word_neutral[word] = word_neutral.get(word, 0) + 1

top_words_neutral = sorted(word_neutral.iteritems(), key=itemgetter(1), reverse=True)[:N]

freq_words_neutral = ' '.join([str(word) for word in top_words_neutral])
freq_word_neutral = open("neutral_freqDist.csv", "wb") 
pickle.dump(freq_words_neutral, freq_word_neutral)
freq_word_neutral.close() 


                                                  
#creating x and y variables for histogram
npopular = 200
total = len(set(word_neutral))
print total
x = []
y = range(npopular)
for pair in range(npopular):
    x = x + [top_words_neutral[pair][1]]
    print top_words_neutral[pair] 
   


#matplotlib histogram plot
fig = plt.figure()
fig.patch.set_facecolor('darkslategrey')
#fig.patch.set_alpha(0.8)


ax = fig.add_subplot(111)
ax.patch.set_facecolor('#625858')
#ax.patch.set_alpha(0.5), 

plt.loglog(x,y, 'ro', color = 'g', basey=10) #linewidth = 5.0,
plt.xlim([10**1, 10**4]) # put line 1/x in the plot to show match

#plt.plot(x, y, linewidth=5.0, color='y', fillstyle = 'right')
#plt.xlim([0, 1000])

#plt.hist(x, bins=200, range = (0,500), color = 'yellow', histtype = 'stepfilled')
plt.xlabel('Frequency of Occurence')
plt.ylabel('Number of Words at Each Frequency')
plt.title('NEUTRAL :|')
plt.show()