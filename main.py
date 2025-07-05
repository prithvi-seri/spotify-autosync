import requests, json

from auth import get_access_token
from config import USER_ID_FILE, SPOTIFY_API_BASE_URL

from storage import Storage

ACCESS_TOKEN = get_access_token()
HEADERS = {
  'Authorization': f'{ACCESS_TOKEN["token_type"]} {ACCESS_TOKEN["access_token"]}'
}

storage = Storage(USER_ID_FILE)

def handle_response(response_object):
  if 'application/json' not in response_object.headers.get('content-type', ''):
    print(f'Status Code {response_object.status_code}: {response_object.reason}')
    return
	
  response = response_object.json()
  if 'error' in response:
    print(json.dumps(response, indent=2))
    return
	
  return response

# Gets user id from API if not in storage file
def get_user_id() -> str:
  user_id = storage.retrieve()

  if not user_id:
    response = handle_response(requests.get(f'{SPOTIFY_API_BASE_URL}/me', headers=HEADERS))
    user_id = response['id']
    storage.store(user_id)
  
  return user_id

def get_liked_songs() -> list[str]:
  response_object = requests.get(f'{SPOTIFY_API_BASE_URL}/me/tracks', headers=HEADERS)
  response = handle_response(response_object)
  return [track['id'] for track in response]
  
def get_user_playlists():
  response = requests.get(f'{SPOTIFY_API_BASE_URL}/users/{get_user_id()}/playlists', headers=HEADERS)
  Storage('output.json').store(json.dumps(handle_response(response)))

get_user_playlists()