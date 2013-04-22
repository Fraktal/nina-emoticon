#! /usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
from pymongo import Connection 
import sys
import credentials
import json
import jsonpickle
import re

#credentials for Twitter OAuth 
CONSUMER_KEY = credentials.CONSUMER_KEY
CONSUMER_SECRET = credentials.CONSUMER_SECRET
ACCESS_TOKEN = credentials.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET

#Mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweetDB']


class StdOutListener(StreamListener):
  
    #tweets and Mongo
    def on_status(self, status):  
      #print status.place
      try:

         #simplified and readable date for the tweets
         date = status.created_at.date().strftime("20%y/%m/%d")      

         #jsonpickle defines complex Python model objects and turns the objects into JSON 
         data = json.loads(jsonpickle.encode(status))
       
         #store the whole tweet object by emoticon
         if re.search('(:\))', status.text):
            db.tweets.save({"smiley": ":)", "date": date, "tweet": data, 
                            "tweet_text_smiley": status.text, "location_smiley": status.place})
            

         elif re.search('(:\()', status.text):
            db.tweets.save({"sad": ":(", "date": date, "tweet": data,
                            "tweet_text_sad": status.text, "location_sad": status.place})

         else:
            db.tweets.save({"neutral": ":|", "date": date, "tweet": data,
                            "tweet_text_neutral": status.text, "location_neautral": status.place}) 

      except ConnectionFailure, e:
          sys.stderr.write("could not connect to MongoDB: %s" % e)
          sys.exit(1)     
                

    #error handling
    def on_error(self, error):
        print error 


#count the number of tweets in mongo and print it
total_count = db.tweets.count()
smiley_count = db.tweets.find({"smiley": ":)"}).count()
sad_count = db.tweets.find({"sad": ":("}).count()
neutral_count = db.tweets.find({"neutral": ":|"}).count()

print
print "  ========================== Connected to Twitter Streaming API =========================  " 
print
print "Previous count in mongo: "
print
print "   Total tweets: ", total_count
print "   Smiley tweets: ", smiley_count
print "   Sad tweets: ", sad_count
print "   Neutral tweets: ", neutral_count
print
print "retrieving data......"

    
     
if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
    stream = Stream(auth, listener)    
    stream.filter(track=[':)', ':(', ':|'])
    
      