from dotenv import load_dotenv
from os import getenv
from base64 import b64encode
from datetime import datetime, timezone, timedelta
from pathlib import Path
import requests
import json
import webbrowser

from storage import Storage
from config import (
	SPOTIFY_ACCOUNTS_BASE_URL,
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

storage = Storage(TOKEN_FILE)

def handle_response(response_object: requests.Response) -> dict | None:
	if 'application/json' not in response_object.headers.get('content-type', ''):
		print(f'Status Code {response_object.status_code}: {response_object.reason}')
		return
	
	response = response_object.json()
	if 'error' in response:
		print(json.dumps(response, indent=2))
		return
	
	store_token(response)
	return response

def get_auth_code() -> str:
	scopes = ['playlist-read-private', 'playlist-modify-public', 'user-library-read']
	url = (SPOTIFY_ACCOUNTS_BASE_URL
		+ '/authorize?'
		+ f'client_id={CLIENT_ID}'
		+ '&response_type=code'
		+ f'&redirect_uri={REDIRECT_URI}'
		+ f'&scope={'%20'.join(scopes)}'
	)
	webbrowser.open(url)
	return url
	# User must follow link and allow access to Spotify; authorization code
	# will be in redirect URL and must be added to .env as AUTH_CODE

def get_access_token_with_auth_code(auth_code: str):
	body = {
		'grant_type': 'authorization_code',
		'code': auth_code,
		'redirect_uri': REDIRECT_URI
	}
	response = requests.post(f'{SPOTIFY_ACCOUNTS_BASE_URL}/api/token', data=body, headers=AUTH_HEADERS)
	return handle_response(response)

def refresh_access_token():
	token = retrieve_token()
	body = {
		'grant_type': 'refresh_token',
		'refresh_token': token['refresh_token']
	}
	response = requests.post(f'{SPOTIFY_ACCOUNTS_BASE_URL}/api/token', data=body, headers=AUTH_HEADERS)
	return handle_response(response)

def store_token(token: dict):
	# Add expiration time when storing token to check whether new token should be fetched
	expires_at = datetime.now(timezone.utc) + timedelta(token['expires_in'])
	token['expires_at'] = expires_at.isoformat()

	# Ensure refresh token is always stored, even if not given in Spotify response
	if 'refresh_token' not in token:
		old_token = retrieve_token()
		token['refresh_token'] = old_token['refresh_token']

	storage.store(token)

def retrieve_token() -> dict:
		return json.loads(storage.get())
	
def get_access_token() -> dict:
	token = retrieve_token()
	expires_at = datetime.fromisoformat(token['expires_at'])
	if expires_at < datetime.now(timezone.utc) + timedelta(60):
		return refresh_access_token()
	return token
