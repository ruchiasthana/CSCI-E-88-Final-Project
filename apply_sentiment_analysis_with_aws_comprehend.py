"""
The goal of this document is to apply sentiment anlysis on tweet data
We will be leveraging AWS Comprehend for sentiment analysis
"""

import boto3
import pandas as pd


#Initialize the AWS Comprehend Client for analysis
client = boto3.client('comprehend')

#We start by reading in a CSV file of elon_musks most recent tweets
elon_musk_recent_tweets = pd.read_csv('./elon_musk_recent_tweets/elon_musk_recent_2000_tweet_data.csv')

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

print(elon_musk_recent_tweets)
elon_musk_recent_tweets.to_csv("elon_musk_recent_2000_tweet_data_with_sentiment_analysis.csv")


