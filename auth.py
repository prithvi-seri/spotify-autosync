from dotenv import load_dotenv
from os import getenv
from base64 import b64encode
import requests
import json

from config import (
	SPOTIFY_BASE_URL,
	REDIRECT_URI,
	TOKEN_FILE
)

load_dotenv()
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')

AUTH_HEADERS = {
	'Content-Type': 'application/x-www-form-urlencoded',
	'Authorization': f'Basic {b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}'
}

def handle_response(response_object: requests.Response) -> dict | None:
	if 'application-json' not in response_object.headers.get('content-type'):
		print(f'Status Code {response_object.status_code}: {response_object.reason}')
		return
	
	response = response_object.json()
	if 'error' not in response:
		store_tokens(response)
		return response['access_token']
	print(json.dumps(response, indent=2))

def get_auth_code() -> str:
	scopes = ['playlist-read-private', 'playlist-modify-public', 'user-library-read']
	url = (SPOTIFY_BASE_URL
		+ '/authorize?'
		+ f'client_id={CLIENT_ID}'
		+ '&response_type=code'
		+ f'&redirect_uri={REDIRECT_URI}'
		+ f'&scope={'%20'.join(scopes)}'
	)
	print(url)
	return url
	# User must follow link and allow access to Spotify; authorization code
	# will be in redirect URL and must be added to .env as AUTH_CODE

def get_access_token():
	body = {
		'grant_type': 'authorization_code',
		'code': getenv('AUTH_CODE'),
		'redirect_uri': REDIRECT_URI
	}
	response = requests.post(f'{SPOTIFY_BASE_URL}/api/token', data=body, headers=AUTH_HEADERS).json()
	return handle_response(response)

def refresh_access_token():
	tokens = retrieve_tokens()
	body = {
		'grant_type': 'refresh_token',
		'refresh_token': tokens['refresh_token']
	}
	response = requests.post(f'{SPOTIFY_BASE_URL}/api/token', data=body, headers=AUTH_HEADERS)
	return handle_response(response)

def store_tokens(tokens: dict):
	with open(TOKEN_FILE, 'w') as token_file:
		json.dump(tokens, token_file, indent=2)

def retrieve_tokens() -> dict:
	with open(TOKEN_FILE, 'r') as token_file:
		return json.load(token_file)