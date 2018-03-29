import tweepy
import config
import json
from multiprocessing.dummy import Pool as ThreadPool
import time
import datetime

from pymongo import MongoClient

auth = tweepy.OAuthHandler("SZSAHKgh0jec0flBIzyZIk0F8", "635fsZ8EdtGskPNJaMU4eCxzUx6bwguUB6NZbjJVyUem8HdVqe")
auth.set_access_token("1331394793-RmnlgxDsvVyeXNe5hA182w0AnmfoEEpQdIZNHSV", "GGgbfTJuogLQPhHNWbsfCeOhwlps7C80Q7J1FcQxQ7wvU")

api = tweepy.API(auth)
trends = ["Oscars","WinterOlympics2018","UCL","DACA","Bitcoin","Hurricane Irma","LasVegasShooting","FloridaShooting"]

client = MongoClient()
db = client.GeoTweets
tweet_coll = db.geotweetsCollection

def limit_handled(cursor):
    print "Came here"
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print "Received Rate Limit Error. Sleeping for 15 minutes , Inside tweets call " + str(datetime.datetime.now()+datetime.timedelta(0,900))
            time.sleep(15 * 60)
        except tweepy.TweepError:
            print "Received Rate Limit Error. Sleeping for 15 minutes , Inside tweets call " + str(datetime.datetime.now()+datetime.timedelta(0,900))
            time.sleep(15 * 60)

# def trends_place(woeid):
#     try:
#         tplace=api.trends_place(woeid)
#         for trend in tplace[0]["trends"]:
#             for status in limit_handled(tweepy.Cursor(api.search, q=trend["name"]).items()):
#                 print json.dumps(status._json)
#                 tweet_coll.insert_one(json.loads(json.dumps(status._json)))
#         print "Finished querying tweets"
#     except tweepy.RateLimitError:
#         print "Received Rate Limit Error. Sleeping for 15 minutes " + str(datetime.datetime.now()+datetime.timedelta(0,900))
#         time.sleep(15 * 60)
#         trends_place(woeid)

def tweets(trend):
    try:
        for status in limit_handled(tweepy.Cursor(api.search, q=trend).items()):
            twt = status.user.location
            if twt != "":
                print twt +"-->" + trend
                #print status.entities.get('hashtags')
                status._id = status.id
                del status.id
                tweet_coll.insert_one(json.loads(json.dumps(status._json)))
        print "Finished querying tweets"
    except tweepy.RateLimitError:
        print "Received Rate Limit Error. Sleeping for 15 minutes " + str(
            datetime.datetime.now() + datetime.timedelta(0, 900))
        time.sleep(15 * 60)

# world_trends = api.trends_available()
# for trends in world_trends:
#     wtrends.add(trends["woeid"])

if __name__ == '__main__':
    pool = ThreadPool(len(trends))
    pool.map(tweets,trends)


# https://twitter.com/statuses/ID should work.
# it will redirect to the needed status.
