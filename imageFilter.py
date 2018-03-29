from pymongo import MongoClient
import urllib
import os
import requests
from PIL import Image
from resizeimage import resizeimage


client = MongoClient()
db1 = client.TweetsDB
db2 = client.GeoTweets
filteredColl = db1.imageTweets3
filteredColl2 = db1.imageTweets4
tweet_coll = db1.tweetsCollection
tweet_coll2 = db2.geotweetsCollection

tweets = tweet_coll.find()
tweets2 = tweet_coll2.find()

m_url = []
tweet_ids = []
count =0
size = 400, 400
for tweet in tweets:
    try:
        for media in tweet['extended_entities']['media']:
            if media['media_url'] in m_url or tweet['id_str'] in tweet_ids:
               print "Duplicate"
            else:
                m_url.append(media['media_url'])
                tweet_ids.append(tweet['id_str'])
                url = media['media_url']
                r = requests.get(url, allow_redirects=True)
                if r.status_code == 404 or r.status_code == 403:
                    continue
                else:
                    open('/Users/madhav/Desktop/Images_final/'+tweet['id_str']+'.jpg', 'wb').write(r.content)
                    #img = Image.open('/Users/madhav/Desktop/Images_final/'+tweet['id_str']+'.jpg')
                    #img.thumbnail(size, Image.ANTIALIAS)
                    #img.save('/Users/madhav/Desktop/Processed_Images/'+tweet["id_str"], "JPEG")
                    filteredColl.insert_one(tweet)
                    print media['media_url']
                    count = count + 1
    except Exception as e:
        print e

print "count = ", count
