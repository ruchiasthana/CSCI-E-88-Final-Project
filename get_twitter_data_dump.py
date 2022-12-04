"""
The objective of this file is to call the Twitter API and get a dump of Tweets over a given time period
"""

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