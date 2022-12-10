"""
The goal of this document is to apply sentiment anlysis on tweet data
We will be leveraging AWS Comprehend for sentiment analysis
"""

import io
import os
import boto3
import pandas as pd


print("Searching for the Recent Tweet Data")
recent_tweets_file_path = './elon_musk_recent_tweets/elon_musk_recent_2000_tweet_data.csv'
if os.path.exists(recent_tweets_file_path):
    print("Recent Tweet Data is found in local computer at the following file path: {}".format(recent_tweets_file_path))
    elon_musk_recent_tweets = pd.read_csv(recent_tweets_file_path)
    print("Head of elon_musk_recent_tweets: ", elon_musk_recent_tweets.head())
else:
    print("Recent Tweet Data is NOT found on the local computer, fetching it from s3")
    #Fetch Data from the s3 bucekt and load it into a Pandas Data Frame Object
    s3_client = boto3.client('s3')
    bucket_name = 'elon-musk-recent-tweets-2'
    file_name = 'elon_musk_recent_2000_tweet_data.csv'
    obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    elon_musk_recent_tweets = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')
    print("Head of elon_musk_recent_tweets: ", elon_musk_recent_tweets.head())

#Initialize the AWS Comprehend Client for analysis
client = boto3.client('comprehend')

#We start by reading in a CSV file of elon_musks most recent tweets
# elon_musk_recent_tweets = pd.read_csv('./elon_musk_recent_tweets/elon_musk_recent_20000_tweet_data.csv')

#Initialize fields that we will want to populate with our analysis
rows, cols = elon_musk_recent_tweets.shape
elon_musk_recent_tweets['sentiment'] = 'initial sentiment'
elon_musk_recent_tweets['positive_sentiment_score'] = 0.0
elon_musk_recent_tweets['negative_sentiment_score'] = 0.0

#Pass each tweet to the AWS Comprehend API for sentiment analysis
count = 0
for row_idx in range(rows):
    tweet_text = elon_musk_recent_tweets['text'][row_idx]
    sentiment_analysis = client.detect_sentiment(Text=tweet_text, LanguageCode='en')
    #Extract Relevant fields from AWS Comprehend Sentiment Analysis
    sentiment = sentiment_analysis['Sentiment']
    positive_sentiment_score = sentiment_analysis['SentimentScore']['Positive']
    negative_sentiment_score = sentiment_analysis['SentimentScore']['Negative']
    elon_musk_recent_tweets['sentiment'][row_idx] = sentiment
    elon_musk_recent_tweets['positive_sentiment_score'][row_idx] = positive_sentiment_score
    elon_musk_recent_tweets['negative_sentiment_score'][row_idx] = negative_sentiment_score
    print("Tweet Text Number {} has been passed through Sentiment Analysis".format(count))
    count += 1

print(elon_musk_recent_tweets.head())
elon_musk_recent_with_sentiment_analysis = 'elon_musk_recent_20000_tweet_data_with_sentiment_analysis.csv'
elon_musk_recent_tweets.to_csv(elon_musk_recent_with_sentiment_analysis)

#Upload Sentiment Analysis Data to s3
s3_client = boto3.client('s3')
elon_musk_recent_tweets_with_sentiment_bucket = 'elon-musk-recent-tweets-with-sentiment-bucket-1'
s3_client.create_bucket(Bucket=elon_musk_recent_tweets_with_sentiment_bucket)
boto3.client('s3').upload_file(elon_musk_recent_with_sentiment_analysis, elon_musk_recent_tweets_with_sentiment_bucket, 'elon_musk_recent_2000_tweet_data_with_sentiment_analysis.csv')



