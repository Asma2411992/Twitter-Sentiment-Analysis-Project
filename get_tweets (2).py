#!usr/local/bin/python
#-*-coding:utf-8-*-

import os
import sys
import tweepy,sqlite3
reload(sys)
sys.setdefaultencoding("utf8")
# SQLITE3 DATABASE SCHEMA
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR,"tweets.db")

conn = sqlite3.connect(db_path)
c = conn.cursor()

#create a table, (Run this once and comment it out)
#c.execute('''CREATE TABLE tweets(tweet_id text,tweets text,query text)''')

 
class Key(object):
    consumer_key = "DZIuMH50lGBb7X4weqTzK6kF2"
    consumer_secret = "CfRzahNRUSEpZODCgyeskaAQLAoMgCQEHXlqtW8KLqkSn7qsO6"
    access_token = "834550483893284864-BiuMnl3w57f6FWInQQtW5POnYhufYo8"
    access_token_secret = "Y4JJjLH9v7SNCNxZCM50ogldT0v5T99hVXEKJ7AXujnq3"

#insert data into table
def insert_into_database(tweet_data):
    c.execute('insert into tweets(tweet_id,tweets,query) values (?,?,?)',(tweet_data[0].decode('utf-8'),tweet_data[1].decode('utf-8'),tweet_data[2].decode("utf-8")))
    

def getTweets(key,query):
    # Authentication of the Keys to Use Twitter API
    tweet_list = []
    try:
        auth_handle = tweepy.OAuthHandler(key.consumer_key,key.consumer_secret)
        auth_handle.set_access_token(key.access_token,key.access_token_secret)
        api_handle = tweepy.API(auth_handle)
        print ("Authentication Success!!\n")
        # Authentication completed
        
        # search query tags (list of one or mutiple queries) using tweepy Cursor
        # clean the query tags eg football,election becomes football OR election
        tweet_query = query.replace(","," OR ")
        # For search we can set lang, geocode, since etc
        tweet_pages = tweepy.Cursor(api_handle.search,q=tweet_query,
                count = 100, result_type = "recent", include_entities = True,
                ).pages()

        for tweets in tweet_pages:
            for tweet in tweets:
                # insert tweet id and tweet data for now
                insert_into_database((str(tweet.id),tweet.text.replace("\n"," "),query))
    except tweepy.error.RateLimitError:
        print ("Rate Limit reached!!")
    except tweepy.error.TweepError:
        print ("Keys Expired!!")

key = Key()
query = raw_input("Enter query/ies eg: football,election : ")
getTweets(key,query)
data = c.execute("select * from tweets")
print data.fetchall()

###save added data to database
c.close()
conn.commit()
### input python get_tweets.py football,
