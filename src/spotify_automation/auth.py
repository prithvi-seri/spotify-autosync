from dotenv import load_dotenv
from os import getenv
from base64 import b64encode
from datetime import datetime, timezone, timedelta
import requests
import json
import webbrowser

from storage import store, retrieve
from config import (
	SPOTIFY_ACCOUNTS_BASE_URL,
	REDIRECT_URI
)

load_dotenv()
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')

AUTH_HEADERS = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': f'Basic {b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}'
}

def _handle_response(response_object: requests.Response) -> str | None:
	if 'application/json' not in response_object.headers.get('content-type', ''):
		print(f'Status Code {response_object.status_code}: {response_object.reason}')
		return
	
	response = response_object.json()
	if 'error' in response:
		print(json.dumps(response, indent=2))
		return
	
	_store_token(response)
	return response['access_token']

def _get_auth_code() -> str:
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

def _get_access_token_with_auth_code(auth_code: str) -> str | None:
	body = {
		'grant_type': 'authorization_code',
		'code': auth_code,
		'redirect_uri': REDIRECT_URI
	}
	response = requests.post(f'{SPOTIFY_ACCOUNTS_BASE_URL}/api/token', data=body, headers=AUTH_HEADERS)
	return _handle_response(response)

def _refresh_access_token() -> str | None:
	token = retrieve('token')
	body = {
		'grant_type': 'refresh_token',
		'refresh_token': token['refresh_token']
	}
	response = requests.post(f'{SPOTIFY_ACCOUNTS_BASE_URL}/api/token', data=body, headers=AUTH_HEADERS)
	return _handle_response(response)

def _store_token(token: dict) -> int:
	# Add expiration time when storing token to check whether new token should be fetched
	expires_at = datetime.now(timezone.utc) + timedelta(seconds=token['expires_in'])
	token['expires_at'] = expires_at.isoformat()

	# Ensure refresh token is always stored, even if not given in Spotify response
	if 'refresh_token' not in token:
		old_token = retrieve('token')
		token['refresh_token'] = old_token['refresh_token']

	return store('token', token)

def setup() -> str | None:
	_get_auth_code()
	auth_code = input('Paste code from URL:\n>> ')
	return _get_access_token_with_auth_code(auth_code)

def get_access_token() -> str:
	token = retrieve('token')
	expires_at = datetime.fromisoformat(token['expires_at'])
	if expires_at < datetime.now(timezone.utc) + timedelta(seconds=60):
		return _refresh_access_token()
	return token['access_token']
