import requests
import json
from kafka import KafkaProducer
import time

API_KEY = 'b7794dccfdaf4091a827673b3122bbe2'
NEWS_URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

producer = KafkaProducer(bootstrap_servers='localhost:9092', api_version=(0,11,5), value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def fetch_news():
    response = requests.get(NEWS_URL)
    articles = response.json().get('articles', [])
    return [article['title'] for article in articles if article['title']]

while True:
    headlines = fetch_news()
    for title in headlines:
        producer.send('news-topic', {'title': title})
        print(f"Sent: {title}")
    time.sleep(60) 