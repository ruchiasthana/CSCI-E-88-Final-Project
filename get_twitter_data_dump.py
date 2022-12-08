"""
The objective of this file is to call the Twitter API and get a dump of Tweets over a given time period
"""
import os
import boto3
import tweepy
import pandas as pd


"""
Below is basic credentials for accessing the Twitter API: 

API Key: F58ZzwAG8D2y582kHGwiTEXqi
API Key Secret: o5n0ASypriKMmWSdOrvkeU25dfKLTrBIw789jK7LQTEdIMkCkf
Bearer Token: AAAAAAAAAAAAAAAAAAAAAPh8jwEAAAAA5FLMueSNftI3RHF0rZPXSKdo0dc%3DEyX313BYU98GdqPWNG3grnxhhX2AkjGE2N8efR1RXZYT1H4WZq
"""

bearer_token = "AAAAAAAAAAAAAAAAAAAAAPh8jwEAAAAA5FLMueSNftI3RHF0rZPXSKdo0dc%3DEyX313BYU98GdqPWNG3grnxhhX2AkjGE2N8efR1RXZYT1H4WZq"
client = tweepy.Client(bearer_token)
s3 = boto3.resource('s3')

elon_musk_recent_tweets_bucket = 'elon-musk-recent-tweets'
path_to_elon_musk_recent_tweets = '/Users/rasthana/Desktop/CSCI-E-88-Final-Project/elon_musk_recent_tweets'
file_for_elon_musk_recent_tweets = path_to_elon_musk_recent_tweets + '/' + 'elon_musk_recent_2000_tweet_data.csv'
if os.path.exists(path_to_elon_musk_recent_tweets):
    print('A path to Elon Musk Recent Tweets already exists!')
    print('Here is its path: ', path_to_elon_musk_recent_tweets)
    if s3.Bucket(elon_musk_recent_tweets_bucket) in s3.buckets.all():
        print('Recent Tweet data already exists in s3')
    else:
        print('Recent Tweet data does NOT exist in s3')
        print('Uploading Recent Tweet data to an s3 bucket')
        s3.create_bucket(Bucket=elon_musk_recent_tweets_bucket)
        boto3.client('s3').upload_file(file_for_elon_musk_recent_tweets, elon_musk_recent_tweets_bucket, 'elon_musk_recent_2000_tweet_data.csv')
        print('Completed uploading data to the elon_musk_recent_tweets bucket')
else:
    print('A path to Elon Musk Recent Tweets does NOT exist!')
    print('We will pull tweet data and save it to s3')
    elon_musk_november_tweets_query = '#elonmusk -is:retweet lang:en'
    elon_musk_november_tweets = tweepy.Paginator(
        client.search_recent_tweets,
        query=elon_musk_november_tweets_query,
        tweet_fields=['context_annotations', 'created_at'],
        max_results=100).flatten(limit=2000)

    count = 0
    elon_musk_november_tweet_data = []
    for tweet in elon_musk_november_tweets:
        tweet_data = [tweet.created_at, tweet.text]
        elon_musk_november_tweet_data.append(tweet_data)
        count += 1

    print("We collected data from {} tweets".format(count))
    elon_musk_november_tweet_data_frame = pd.DataFrame(elon_musk_november_tweet_data, columns = ['created_at', 'text'])
    print("Data Frame for Elon Musk's Recent Tweets", elon_musk_november_tweet_data_frame.head())
    elon_musk_november_tweet_data_frame.to_csv("elon_musk_recent_2000_tweet_data.csv")
    s3.create_bucket(Bucket=elon_musk_recent_tweets_bucket)
    boto3.resource('s3').upload_file(file_for_elon_musk_recent_tweets, elon_musk_recent_tweets_bucket, 'elon_musk_recent_2000_tweet_data.csv')

