from kafka import KafkaConsumer
import boto3


client= boto3.resource("s3",aws_access_key_id="AKIA2EINJWAAFEPCTRAN", aws_secret_access_key="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")

consumer = KafkaConsumer('finalproject', bootstrap_servers=['localhost:9092'])

s3_file_name = "s://e88-finalproject-bucket\TwitterData\Tweet.csv"


for message in consumer:
    values = message.value.decode('utf-8')
    with open(s3_file_name, 'w') as f:
        print(message.value)
        f.write(f"{values}\n")
