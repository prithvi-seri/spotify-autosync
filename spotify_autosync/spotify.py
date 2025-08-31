import requests, json

from .auth import get_access_token
from .config import SPOTIFY_API_BASE_URL, NEW_MUSIC_PLAYLISTS

from .storage import store, retrieve

ACCESS_TOKEN, TOKEN_TYPE = get_access_token()
if not ACCESS_TOKEN:
    raise RuntimeError("ACCESS_TOKEN is missing or invalid. Aborting module execution.")
GET_HEADERS = {
  'Authorization': f'{TOKEN_TYPE} {ACCESS_TOKEN}'
}
POST_HEADERS = {
  'Authorization': f'{TOKEN_TYPE} {ACCESS_TOKEN}',
  'Content-Type': 'application/json'
}

def _handle_response(response_object) -> dict | None:
  if 'application/json' not in response_object.headers.get('content-type', ''):
    print(f'Status Code {response_object.status_code}: {response_object.reason}')
    return
	
  response = response_object.json()
  if 'error' in response:
    print(json.dumps(response, indent=2))
    return
	
  return response

# Gets user id from API if not in storage
def get_user_id() -> str | None:
  user_id = retrieve('user_id')
  if not user_id:
    response = _handle_response(requests.get(f'{SPOTIFY_API_BASE_URL}/me', headers=GET_HEADERS))
    user_id = response['id']
    store('user_id', user_id)
  return user_id

def get_liked_songs() -> list[str] | None:
  response_object = requests.get(f'{SPOTIFY_API_BASE_URL}/me/tracks', headers=GET_HEADERS)
  response = _handle_response(response_object)
  return response['items'] if response else None

def get_playlists() -> dict[str, set]:
  # get playlists
  response_object = requests.get(f'{SPOTIFY_API_BASE_URL}/me/playlists', headers=GET_HEADERS)
  response = _handle_response(response_object)
  if not response:
    return
  
  # get tracks in each playlist
  playlists = {}
  for playlist_object in response['items']:
    if playlist_object['name'] not in NEW_MUSIC_PLAYLISTS:
      continue  # Only get tracks for playlists being updated
    playlist_id = playlist_object['id']
    total_tracks = playlist_object['tracks']['total']
    params = {
      'offset': max(0, total_tracks - 20),
      'fields': 'items(track.id)'
    }
    response_object = requests.get(f'{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}/tracks', headers=GET_HEADERS, params=params)
    response = _handle_response(response_object)
    track_ids = {track_object['track']['id'] for track_object in response['items']}
    playlists[playlist_object['name']] = {
      'id': playlist_id,
      'tracks': track_ids
    }
  
  return playlists

def create_playlist(name: str) -> str:
  user_id = get_user_id()
  body = { 'name': name }
  response = requests.post(f'{SPOTIFY_API_BASE_URL}/users/{user_id}/playlists', headers=POST_HEADERS, json=body)
  playlist = _handle_response(response)
  if playlist: return playlist['id']
  

def add_to_playlist(playlist_id: str, song_ids: list[str]):
  uris = [f'spotify:track:{song_id}' for song_id in song_ids]
  body = { 'uris': uris }
  response = requests.post(f'{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}/tracks', headers=POST_HEADERS, json=body)
  _handle_response(response)
