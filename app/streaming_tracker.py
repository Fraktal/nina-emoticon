from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
from pymongo import Connection 
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
       #readable date for tweets
       date = status.created_at.date().strftime("20%y/%m/%d")        
       
       #pickle the BSON data into JSON
       data = json.loads(jsonpickle.encode(status))
       print data
       
       #store the whole tweet object
       db.tweets.save({"Date": date, "tweet": data})

       """ possible way to store by emoticon
       
       if(regex = smiley):
          db.tweets.save({"smiley": ":)", "Date": date, "tweet": data})
       elif(regex = sad):
          db.tweets.save({"sad": ":(", "Date": date, "tweet": data})
       else(regex = neutral):
          db.tweets.save({"neutral": ":|", "Date": date, "tweet": data}) 


       """

    #error handling
    def on_error(self, error):
        print error 
    
     


if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
    stream = Stream(auth, listener)    
    stream.filter(track=[':)', ':(', ':|'])
      