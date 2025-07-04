from dotenv import load_dotenv
from os import getenv

load_dotenv()

def get_auth_code():
	client_id = getenv('CLIENT_ID')
	redirect_uri = 'https://github.com/prithvi-seri'
	scopes = ['playlist-read-private', 'playlist-modify-public', 'user-library-read']
	url = ('https://accounts.spotify.com/authorize?'
		+ f'client_id={client_id}'
		+ '&response_type=code'
		+ f'&redirect_uri={redirect_uri}'
		+ f'&scopes={'%20'.join(scopes)}'
	)
	print(url)
	# User must follow link and allow access to Spotify; authorization code will be in redirect URL
