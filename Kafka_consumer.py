from kafka import KafkaConsumer
import boto3
import json

with open('config.json') as json_file:
    data = json.load(json_file)

client= boto3.resource("s3", aws_access_key_id=data['AWS_ACCESS_KEY_ID'], aws_secret_access_key= data['AWS_SECRET_ACCESS_KEY'])
elon_musk_recent_tweets_with_sentiment_bucket = 'elon-musk-recent-tweets-with-sentiment-bucket-1'
client.create_bucket(Bucket=elon_musk_recent_tweets_with_sentiment_bucket)
consumer = KafkaConsumer('finalproject', bootstrap_servers=['localhost:9092'])

s3_file_name = "elon_musk_recent_20000_tweet_data_with_sentiment_analysis.csv"


for message in consumer:
    values = message.value.decode('utf-8')
    with open(s3_file_name, 'w') as f:
        print(message.value)
        f.write(f"{values}\n")

boto3.client('s3').upload_file(elon_musk_recent_with_sentiment_analysis, elon_musk_recent_tweets_with_sentiment_bucket,
                               'elon_musk_recent_20000_tweet_data_with_sentiment_analysis.csv')
