import pymongo
from pymongo import MongoClient
from pymongo import Connection 
from pymongo.errors import ConnectionFailure
connection = MongoClient()



def main():
    try:
        c = Connection(host = "localhost", port = 27017)
    except ConnectionFailure, e:
        sys.stderr.write("could not connect to MongoDB: %s" % e)
        sys.exit(1)
    dbh = connection['tweetDB']
    assert dbh.connection == c
    tweet_data = {"date": "test", "tweet": "test2"}
    dbh.tweets.insert(tweet_data, safe = True)
    print "Saved ==> : %s" %tweet_data    

if __name__ == '__main__':
    main()    