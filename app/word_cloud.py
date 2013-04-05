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
	#print " %s [%d]" % (word, frequency)
    word  

for word in top_words_sad:
    word  

for word in top_words_neutral:
    word          


#saving sorted words into a pickle file containing words and frequency of occurence 
freq_words_smiley= ' '.join([str(word) for word in top_words_smiley])
freq_word_smiley = open("smiley_word.pickle", "ab") 
pickle.dump(freq_words_smiley, freq_word_smiley)
freq_word_smiley.close()

freq_words_sad= ' '.join([str(word) for word in top_words_sad])
freq_word_sad = open("sad_word.pickle", "ab") 
pickle.dump(freq_words_sad, freq_word_sad)
freq_word_sad.close()

freq_words_neutral= ' '.join([str(word) for word in top_words_neutral])
freq_word_neutral = open("neutral_word.pickle", "ab") 
pickle.dump(freq_words_neutral, freq_word_neutral)
freq_word_smiley.close()
#print freq_words


#build word cloud     
happy_words = pickle.load(open('smiley_word.pickle', "rb"))
words_happy = happy_words.split()
happy_list_smiley = words_happy 
s = "".join(sorted(happy_list_smiley))
content_happy = str(s)[:1480]

sad_words = pickle.load(open('sad_word.pickle', "rb"))
words_sad = sad_words.split()
sad_list_sad = words_sad 
t = "".join(sorted(sad_list_sad))
content_sad = str(t)[:1480]

neutral_words = pickle.load(open('neutral_word.pickle', "rb"))
words_neutral = neutral_words.split()
neutral_list_neutral = words_neutral 
u = "".join(sorted(neutral_list_neutral))
content_neutral = str(u)[:1250]
print content_happy
print content_sad
print content_neutral
 
tag_smiley = make_tags(get_tag_counts(content_happy), maxsize=90)

tag_sad = make_tags(get_tag_counts(content_sad), maxsize=90)

tag_neutral = make_tags(get_tag_counts(content_neutral), maxsize=90)

create_tag_image(tag_smiley, 'smiley_emoticon.png', size=(900, 600), fontname='Philosopher',
                 background=(32, 35, 105, 255))

create_tag_image(tag_sad, 'sad_emoticon.png', size=(900, 600), fontname='Philosopher',
                 background=(32, 35, 105, 255))

create_tag_image(tag_neutral, 'neutral_emoticon.png', size=(900, 600), fontname='Philosopher',
                 background=(32, 35, 105, 255))

#word cloud image
webbrowser.open('smiley_emoticon.png') 
webbrowser.open('sad_emoticon.png') 
webbrowser.open('neutral_emoticon.png') 