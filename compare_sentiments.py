from pymongo import MongoClient
import pandas as pd
from vaderSentiment import vader


TESTING = False
tweet_ids = []

def pymongo_connection():
    """
    helper function to connect to database
    :return: mysql connection
    """
    client = MongoClient()
    return client


def pull_all_original_tweets():
    """
    Hardcoded SQL query to pull all originally selected tweets
    :return original_tweets: pandas dataframe of original tweets
    """
    # open database connection
    client = pymongo_connection()
    db = client.TweetsDB
    tweet_coll = db.cleanedTweets

    # pull record id, username and image url from all downloaded tweets
    original_tweets = tweet_coll.find()
    client.close()
    all_tweets = pd.DataFrame(list(original_tweets))
    return all_tweets


def return_sentiment_category(score, threshhold):
    """
    Used to determine
    :param score: numeric: value calculated from specific method
    :param threshhold: cutoff value below which sentiment = 0
    :return integer:  -1 (negative), 0 (neutral), 1 (positive)
    """
    if score <= -threshhold:
        return -1
    elif score >= threshhold:
        return 1
    else:
        return 0


def calculate_vader(tweet):
    """
    Calculate sentimenet using VADER code
    :param tweet: tokenizable string
    :return integer: -1 (negative), 0 (neutral), 1 (positive)
    """
    sentiment = vader.sentiment(tweet)['compound']
    return return_sentiment_category(sentiment, 0.1)


def load_afinn_dictionary(sentiment_file_location, splitter='\t'):
    """
    Creates a sentiment dictionary based on a text file
    dictionary needs to be lines of term and sentiment score
    :param sentiment_file_location: string with location of sentiment data
    :param splitter: text of character to split on = default is tab
    :return sentiment_dictionary: dictionary
    """
    sentiment_file = open(sentiment_file_location)
    sentiment_dictionary = {}
    for line in sentiment_file:
        term, score = line.split(splitter)
        sentiment_dictionary[term] = float(score)
    sentiment_file.close()
    return sentiment_dictionary


def calculate_simple_sentiment(tweet, sentiment_dict):
    """
    calculate sentiment using AFINN lexicon
    :param tweet: string
    :param sentiment_dict: Dictionary with +/- sentiment scores
    :return:
    """
    tokens = tweet.split()
    sentiment = 0
    for word in tokens:
        if word in sentiment_dict:
            sentiment += sentiment_dict[word]
    return return_sentiment_category(sentiment, 1)


def load_huliu_dict(file_location):
    sentiment_dictionary = {}
    negative_words = open(file_location + 'negative-words.txt')
    for line in negative_words:
        if line[0] != ';' and len(line) > 0:
            sentiment_dictionary[line.strip()] = -1
    negative_words.close()

    positive_words = open(file_location + 'positive-words.txt')
    for line in positive_words:
        if line[0] != ';' and len(line) > 0:
            sentiment_dictionary[line.strip()] = 1
    positive_words.close()

    return sentiment_dictionary


def figure_tweet_stats(result_matrix):
    corr_df = result_matrix.corr()
    print(corr_df)
    corr_df.to_csv('text_sentiment_correlation.txt', sep=' ', index=True,
                   header=True, float_format='%.3f')
    return corr_df


def update_database(sentiment_df):
    """
    Updates database to indicate tweet sentiment and whether certainty
    tweet_sentiment: -1 = negative, 0 = neutral, 1 = positive
    unclear_sentiment: 0 = clear, 1 = unclear
    :param sentiment_df: Pandas dataframe with sentiment details
    :return:
    """
    connection = pymongo_connection()
    db = connection.TweetsDB
    sentimentTweets = db.tweetSentimentFinal

    for i in range(len(sentiment_df.index)):
        """ith connection.cursor() as cursor:
            tweet = sentiment_df.ix[i, :]
            sql = 'UPDATE Original_tweets SET tweet_sentiment = %s, ' \
                  'unclear_sentiment = %s WHERE tweet_id = %s'
            clarity = int(not tweet['consistent'])
            sentiment = int(tweet['sentiment'])
            cursor.execute(sql,
                           (sentiment, clarity, int(tweet['tweet_id'])))
            connection.commit()"""
        tweet = sentiment_df.ix[i, :]
        clarity = int(not tweet['consistent'])
        sentiment = int(tweet['sentiment'])
        sentimentTweets.insert(
            {"tweet_id": int(tweet['tweet_id']), "username": tweet['username'], "text": tweet['text'], "processed_text": tweet['processed_text'],
             "image_url": tweet['image_url'], "created_ts": tweet['created_ts'], "sentiment": sentiment, "unclear_sentiment": clarity})
        #sentimentTweets.update_one({"tweet_id": int(tweet['id'])},  {$set : {"sentiment": sentiment}})
    connection.close()


def calculate_sentiments():
    """
    Loops through Tweets in database, calculates sentiment 3 ways and
    updates database with value
    :return:
    """
    # 1. get tweet data into a dataframe
    tweet_df = pull_all_original_tweets()
    # 2. Calculate vader sentiment
    #tweet_df['vader'] = tweet_df['processed_text'].apply(calculate_vader)
    tweet_df['vader'] = tweet_df['processed_text'].apply(calculate_vader)
    # 3. Calculate AFINN sentiment (simple word value count)
    afinn_dict = load_afinn_dictionary('AFINN-111.txt')
    tweet_df['afinn'] = \
        tweet_df['processed_text'].apply(lambda x:
                                         calculate_simple_sentiment(x,
                                                                    afinn_dict))
    # 4. Calculate using Hu/Liu simple +/- word count
    hu_liu_dict = load_huliu_dict('hu_liu/opinion-lexicon-English/')
    tweet_df['huliu'] = \
        tweet_df['processed_text'].apply(
                lambda x: calculate_simple_sentiment(x, hu_liu_dict))

    # 5. identify values with consistent sentiment ratings
    tweet_df['consistent'] = tweet_df.apply(lambda x:
                                            x['vader'] ==
                                            x['afinn'] ==
                                            x['huliu'], axis=1)
    # I think it's better to ascribe Vader sentiment irrespective of consistency
    # tweet_df['sentiment'] = np.where(tweet_df['consistent'] == True,
    #                                  tweet_df['vader'], 99)
    tweet_df['sentiment'] = tweet_df['vader']
    print('Positive sentiment: ' + str(sum(tweet_df['sentiment'] == 1)))
    print('Negative sentiment: ' + str(sum(tweet_df['sentiment'] == -1)))
    print('Neutral sentiment: ' + str(sum(tweet_df['sentiment'] == 0)))
    print('\nCorrelation stats:')
    figure_tweet_stats(tweet_df[['vader', 'afinn', 'huliu']])

    # 6. Update database with sentiment & consistency values
    print('\nupdating database...')
    update_database(tweet_df)


if __name__ == '__main__':
    calculate_sentiments()