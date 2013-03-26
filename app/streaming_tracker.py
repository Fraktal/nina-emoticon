from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
from pymongo import Connection 
import credentials
import simplejson as json
import re


#credentials for Twitter OAuth 
CONSUMER_KEY = credentials.CONSUMER_KEY
CONSUMER_SECRET = credentials.CONSUMER_SECRET
ACCESS_TOKEN = credentials.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET

#Mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['rad']


class StdOutListener(StreamListener):
  
    #tweets and Mongo
    def on_status(self, status):
       date = status.created_at.date().strftime("20%y/%m/%d") #readable date for tweets       
       print(date + ' Tweet: ' + status.text)

    buffer = ""
       
    def on_receive(status):
       buffer += data.strip()         
       if (data.endswith("\r\n")):
         if buffer:
           on_status(buffer)
           buffer = ""  
  
       #regex for each emoticon
       #smiley = re.finditer("'^:\))+$'", status.text)
       #sad = 
       #neutral =   
       
       #JSON and Mongo
       data = json.loads(status)
       tweet = json.dumps(dict(data))
       tweet_data = {"date": "date", "tweet": "tweet.text"}
       #save tweets: date and text
       db.what_up.save = (tweet_data)
    
    #error handling
    def on_error(self, error):
        print error 
    
     


if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
    stream = Stream(auth, listener)    
    stream.filter(track=[':)', ':(', ':|'])
      