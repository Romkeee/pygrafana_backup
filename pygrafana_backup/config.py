import os

SERVER = os.environ['SERVER']
API_KEY = os.environ['API_KEY']
HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
