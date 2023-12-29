from dotenv import load_dotenv
import os
import json

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# get plants info from json file
with open('plants.json') as f:
    data = json.load(f)
    plants = data['plants']

with open('config.json') as f:
    config = json.load(f)
