
"""from skimage import io
from skimage.color import lab2rgb
from skimage import util"""
import numpy as np
from sklearn.decomposition import RandomizedPCA
import matplotlib.pyplot as plt
import pandas as pd
import pymongo.mongo_client
import platform
import json

SIZE = (400, 400)
TESTING = False

IMAGE_DIR = '/Users/madhav/Downloads/ImageData/Processed_Images/'


def img_to_3d_matrix(jsonObj, size):
    img = np.array(jsonObj)
    return img


def visualize_data(data, labels):
    pca = RandomizedPCA(n_components=2)
    reshaped = pca.fit_transform(data)
    df = pd.DataFrame({'x': reshaped[:,0], 'y': reshaped[:, 1],
                       'label': np.where(labels == 1, 'Positive',
                                         np.where(labels == 0, 'Neutral',
                                                  'Negative'))})
    colors = ['yellow', 'red', 'blue']
    for label, color in zip(df['label'].unique(), colors):
        mask = df['label'] == label
        plt.scatter(df[mask]['x'], df[mask]['y'], c=color, label=label)
    plt.legend()
    plt.title('PCA Decomposition of Image Data')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.show()
    # plt.savefig('PCA_plot.png')


def get_crowdflower(class_count=1000,
                    image_path='/Volumes/NeuralNet/crowdflower_images/',
                    size=(231,231)):
    data = []
    connection = pymongo.MongoClient()
    db = connection.TweetsDB
    tweetColl = db.testData
    positive = list(tweetColl.find({"unclear_sentiment": 0, "sentiment": 1}).limit(class_count))
    negative = list(tweetColl.find({"unclear_sentiment": 0, "sentiment": -1}).limit(class_count))
    neutFile = open("testSample.tsv", "w")
    combined = positive + negative
    for x in combined:
        neutFile.write(str(x['image_id'])+"\n")
    neutFile.close()
    for image in combined['image_id']:
        image = image_path + str(image) + '.jpg'
        img = img_to_3d_matrix(image, size)
        data.append(img)
    data = np.stack(data)
    return data, np.array(combined['sentiment'])


def get_data(class_count=1000, image_path=IMAGE_DIR,
             rand=True, size=(231, 231)):

    # 1. retreive list of images to process
    data = []
    connection = pymongo.MongoClient()
    db = connection.TweetsDB
    tweetColl = db.tweetSentimentFinal
    neutral = list(tweetColl.find({"unclear_sentiment": 0, "sentiment": 0}).limit(class_count))
    neutFile = open("tweetSample.tsv", "w")
    positive = list(tweetColl.find({"unclear_sentiment": 0, "sentiment": 1}).limit(class_count))
    negative = list(tweetColl.find({"unclear_sentiment": 0, "sentiment": -1}).limit(class_count))
    combined = neutral + positive + negative
    for x in combined:
        neutFile.write(str(x['tweet_id'])+"\n")
    neutFile.close()
    #exit(0)
    connection.close()
    if True:
    #with connection.cursor() as cursor:
        if rand:
            """sql = 'SELECT tweet_id, tweet_sentiment FROM Original_tweets ' \
                  'WHERE unclear_sentiment = 0 AND tweet_sentiment = '

            # Neutral sentiment
            cursor.execute(sql + '0')"""
            sub_results = pd.DataFrame(neutral)
            pct_keep = class_count / len(sub_results)
            np.random.seed(3112016)
            keep = np.random.uniform(0, 1, len(sub_results)) <= pct_keep
            results = sub_results[keep]

            # Positive sentiment
            #cursor.execute(sql + '1')
            sub_results = pd.DataFrame(positive)
            pct_keep = class_count / len(sub_results)
            np.random.seed(11032016)
            keep = np.random.uniform(0, 1, len(sub_results)) <= pct_keep
            results = results.append(sub_results[keep])

            # Negative sentiment
            #cursor.execute(sql + '-1')
            sub_results = pd.DataFrame(negative)
            pct_keep = class_count / len(sub_results)
            np.random.seed(1132016)
            keep = np.random.uniform(0, 1, len(sub_results)) <= pct_keep
            results = results.append(sub_results[keep])

        else:
            results = pd.DataFrame(neutral+positive+negative)
    connection.close()

    counter = 0
    imageFile = open('imageData.json', "r")
    #imageList = imageFile.read()
    imageData = json.load((imageFile))

    for image in imageData:
        #image = image_path + str(image) + '.jpg'
        try:
            key = image.keys()
            imageJSON = image[key[0]]
        except KeyError as e:
            counter = counter + 1
            print e
        img = img_to_3d_matrix(imageJSON, size)
        data.append(img)
    print counter
    data = np.stack(data)
    return data, np.array(results['sentiment'])


def test():
    data = []
    sentiments = np.array([-1] * 10 + [1] * 10 + [0] * 10)
    image_list = [691363804903559168, 691363809072648192, 691363947493007360,
                  691363989423575040, 691364035585912832, 691364060726579201,
                  691364178184048640, 691364241085829120, 691364333364875264,
                  691364580853977088,
                  691363813279531008, 691363838449573889, 691363842635464706,
                  691364014614519808, 691364060751745024, 691364169786990592,
                  691364186593595397, 691364236908445696, 691364316600274944,
                  691364392093364224,
                  691363767133851648, 691363779729182720, 691363779737681921,
                  691363809076711424, 691363813292122113, 691363825845682176,
                  691363851019927553, 691363851028320256, 691363863615270912,
                  691363867788759040]
    for image in image_list:
        image = IMAGE_DIR + str(image) + '.jpg'
        img = img_to_3d_matrix(image, (231, 231))
        data.append(img)
    data = np.array(data)

    return data, sentiments


def main(visualize=True):
    if TESTING:
        data, labels = test()
    else:
        data, labels = get_data()
        #data, labels = get_crowdflower()
        print(len(data))
        print(len(labels))
        print(data)
        print(labels)
    if visualize:
        visualize_data(data, labels)


if __name__ == '__main__':
    main(False)