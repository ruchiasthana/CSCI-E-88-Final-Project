import tweepy
from kafka import KafkaProducer
from json import dumps
import json

with open('config.json') as json_file:
    data = json.load(json_file)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda K: dumps(K).encode('utf-8'))


bearer_token = data['BEARER_TOKEN']
client = tweepy.Client(bearer_token)

elon_musk_november_tweets_query = '#elonmusk -is:retweet lang:en'
elon_musk_november_tweets = tweepy.Paginator(
    client.search_recent_tweets,
    query=elon_musk_november_tweets_query,
    tweet_fields=['context_annotations', 'created_at'],
    max_results=100).flatten(limit=20000)

for tweet in elon_musk_november_tweets:
    producer.send('finalproject', tweet.text)





