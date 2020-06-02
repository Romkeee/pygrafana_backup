import os

SERVER = os.environ['SERVER']
API_KEY = os.environ['API_KEY']
HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
SSL_CHECK = False if os.environ.get('SSL_CHECK') is None else True
