from pymongo import MongoClient
import urllib
import os
import requests
import datetime
from email.utils import parsedate_tz, mktime_tz
import hashtag_split as sh

tweet_ids = []
english_words = sh.english_word_list()

def convert_twitter_date_to_datetime(twitter_created_at):
    timestamp = mktime_tz(parsedate_tz(twitter_created_at))
    return str(datetime.datetime.fromtimestamp(timestamp))


def insert_record(db, tweet):
    try:
        # Create new record
        id = tweet['id']
        tweet_txt = tweet['text']
        cleaned_text = sh.parse_sentence(tweet_txt, english_words)
        tweet_url = tweet['extended_entities']['media'][0]['media_url']
        timestamp = convert_twitter_date_to_datetime(tweet['created_at'])
        username = tweet['user']['screen_name']
        db.cleanedTweets.insert({"tweet_id": int(tweet['id']), "username": username, "text": tweet_txt, "processed_text": cleaned_text, "image_url": tweet_url, "created_ts": timestamp})
    except Exception as e:
        print e

def process_all_tweet_files():
    client = MongoClient()
    db1 = client.TweetsDB
    filteredColl1 = db1.imageTweets3
    filteredColl2 = db1.imageTweets4
    tweets1 = filteredColl1.find(no_cursor_timeout=True)

    dup_count = 0
    try:
        for tweet in tweets1:
            if tweet['id'] in tweet_ids:
                dup_count = dup_count+1
                print dup_count
                continue
            else:
                tweet_ids.append(tweet['id'])
                insert_record(db1, tweet)
        tweets1.close()
        tweets2 = filteredColl2.find(no_cursor_timeout=True)
        for tweet2 in tweets2:
            if tweet2['id'] in tweet_ids:
                dup_count = dup_count + 1
                print dup_count
                continue
            else:
                tweet_ids.append(tweet2['id'])
                insert_record(db1, tweet2)
        tweets2.close()
    except Exception as e:
        print tweet['id']
        print e
    print "Total dup count"
    print dup_count

if __name__ == '__main__':
    process_all_tweet_files()