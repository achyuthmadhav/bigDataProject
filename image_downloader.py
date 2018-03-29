from pymongo import MongoClient
import urllib
import os
import requests
from PIL import Image
from resizeimage import resizeimage

client = MongoClient()
db1 = client.TweetsDB
filteredColl = db1.imageTweets3
tweets = filteredColl.find()
count =0

for tweet in tweets:
    try:
        fd_img = open('/Users/madhav/Desktop/Images_final/'+tweet['id_str']+'.jpg', 'r')
        img = Image.open(fd_img)
        print img.filename
        img = resizeimage.resize_contain(img, [400, 400])
        img.save('/Users/madhav/Desktop/Processed_Images/'+tweet['id_str']+'.jpg', img.format)
        count = count + 1
        if count > 10:
            break;
        fd_img.close()
    except Exception as e:
        print e
