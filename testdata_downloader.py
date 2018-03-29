"""
Puts crowdflower data in MySQL and downloads transformed images
"""
from pymongo import MongoClient
import os
#from Python_code import sql_connect as mysql
import pandas as pd
import time
from PIL import Image
from io import BytesIO
import requests
import platform

FILE_PATH = '/Users/madhav/Desktop/TestData/'

def download_image(url, image_id):
    try:
        response = requests.get(url)
    except Exception as e:
        print e
        time.sleep(15*60)
        return 0
    if response.status_code == 404 or response.status_code == 403:
        return -1
    #img = Image.open(BytesIO(response.content))
    #img = img.resize((400, 400), Image.ANTIALIAS)
    filename = FILE_PATH + str(image_id) + '.jpg'
    open(filename, 'wb').write(response.content)
    response.close()
    return 1
    #img.save(filename)


def add_to_db(image_id, sentiment, unclear_sentiment, image_url):
    connection = MongoClient()
    db = connection.TweetsDB
    testColl = db.testData
    testColl.insert({"image_id": image_id, "sentiment": sentiment, "unclear_sentiment": unclear_sentiment, "image_url": image_url})
    #connection.commit()
    connection.close()


#curr_dir = os.getcwd()
#os.chdir(curr_dir[:-18] + 'Data/test_data')

cf_images = pd.read_csv('image-Sentiment-Polarity-DFE.csv')



for row in range(len(cf_images)):
    image_id = int(cf_images.at[row,'_unit_id'])
    sentiment = 1 \
        if 'positive' in \
           cf_images.at[row, 'which_of_these_sentiment_scores_does_the_above_image_fit_into_best'] \
        else -1
    unclear_sentiment = 0 \
        if cf_images.at[row, 'which_of_these_sentiment_scores_does_the_above_image_fit_into_best:confidence'] > .66 \
        else 1
    image_url = cf_images.at[row, 'imageurl']
    image_dld = download_image(image_url, image_id)
    if image_dld == 1:
        add_to_db(image_id, sentiment, unclear_sentiment, image_url)
    if image_dld == 0:
        download_image(image_url, image_id)
    if image_dld == -1:
        print image_url
        print image_id
        continue
    if row % 1000 == 0:
        print(row)