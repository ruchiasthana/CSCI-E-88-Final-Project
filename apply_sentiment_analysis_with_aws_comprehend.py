"""
The goal of this document is to apply sentiment anlysis on tweet data
We will be leveraging AWS Comprehend for sentiment analysis
"""

import json
import boto3
import pandas as pd


#Initialize the AWS Comprehend Client for analysis
client = boto3.client('comprehend')

#We start by reading in a CSV file of elon_musks most recent tweets
elon_musk_recent_tweets = pd.read_csv('./elon_musk_recent_tweets/elon_musk_recent_2000_tweet_data.csv')
head = elon_musk_recent_tweets.head()
print("The head of this data file is: ", head )

#Then we pass each tweet to the AWS Comprehend API for sentiment analysis
count = 0
for tweet_text in elon_musk_recent_tweets['text']:
    sentiment_analysis = client.detect_sentiment(Text=tweet_text, LanguageCode='en')
    sentiment = sentiment_analysis['Sentiment']
    positive_sentiment_score = sentiment_analysis['SentimentScore']['Positive']
    negative_sentiment_score = sentiment_analysis['SentimentScore']['Negative']
    elon_musk_recent_tweets['sentiment'] = sentiment
    elon_musk_recent_tweets['positive_sentiment_score'] = positive_sentiment_score
    elon_musk_recent_tweets['negative_sentiment_score'] = negative_sentiment_score
    print("Tweet Text Number {}".format(count))
    count += 1

print(elon_musk_recent_tweets.head())
elon_musk_recent_tweets.to_csv("elon_musk_recent_2000_tweet_data_with_sentiment_analysis.csv")


