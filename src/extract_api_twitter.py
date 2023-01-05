from datetime import datetime, timedelta
from dotenv import find_dotenv, load_dotenv
import requests
import json
from os import getenv
from os.path import join
from pathlib import Path

load_dotenv(find_dotenv())

timestamp_format = '%Y-%m-%dT%H:%M:%S.00Z'

end_time = datetime.now().strftime(timestamp_format)
start_time = (datetime.now() + timedelta(-1)).date().strftime(timestamp_format)
query = "datascience"

fields = json.load(open(join(Path(__file__).parents[0], 'fields.json')))

tweet_fields = f'tweet.fields={",".join(fields["tweet_fields"])}'
user_fields = f'expansions=author_id&user.fields={",".join(fields["user_fields"])}'

url_raw = f'https://api.twitter.com/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}'

bearer_token = getenv("BEARER_TOKEN")
headers = {"Authorization": f'Bearer {bearer_token}'}
response = requests.request("GET", url_raw, headers=headers)

json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))

while 'next_token' in json_response.get('meta', {}):
  next_token = json_response['meta']['next_token']
  url = f'{url_raw}&next_token={next_token}'
  response = requests.request("GET", url, headers=headers)
  json_response = response.json()
  print(json.dumps(json_response, indent=4, sort_keys=True))