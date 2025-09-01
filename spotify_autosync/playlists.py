from datetime import datetime, timezone, timedelta
from dateutil.parser import isoparse

from .spotify import get_liked_songs, get_playlists, get_playlist_with_dates, add_to_playlist, delete_from_playlist, create_playlist
from .config import NEW_PLAYLIST, SYNCED_PLAYLISTS

PLAYLISTS = SYNCED_PLAYLISTS + [NEW_PLAYLIST]

def was_added_recently(time: datetime) -> bool:
  return datetime.now(timezone.utc) - isoparse(time) <= timedelta(hours=12)
  
def _add_missing_songs(song_id: str, playlists: dict[str, str | dict], new_songs: dict[str, list[str]]):
  for playlist in PLAYLISTS:
    # add if playlist doesn't exist (creation handled in add_to_playlist)
    if playlist not in playlists or song_id not in playlists[playlist]['tracks']:
      new_songs[playlist]['tracks'].append(song_id)

def _get_new_songs(liked_songs: list[str], playlists: dict[str, str | dict]) -> dict[str, list[str]]:
  new_songs = {playlist: {
    'id': playlists[playlist]['id'] if playlist in playlists else None,   # mark playlists to be created with id None
    'tracks': []
    } for playlist in PLAYLISTS
  }
  for song in liked_songs:
    if was_added_recently(song['added_at']):
      _add_missing_songs(song['track']['id'], playlists, new_songs)

  # reverse track lists (since liked songs are in reverse chronological order, but playlists should be in chronological order)
  new_songs = {playlist: {
    'id': new_songs[playlist]['id'],
    'tracks': new_songs[playlist]['tracks'][::-1]
    } for playlist in new_songs
  }
  return new_songs

def _add_new_songs(new_songs: dict[str, str | list[str] | None]):
  for playlist in new_songs:
    playlist_id = new_songs[playlist]['id']
    if not playlist_id:
      playlist_id = create_playlist(playlist)
    # empty list check to avoid bad api requests
    if new_songs[playlist]['tracks']: add_to_playlist(playlist_id, new_songs[playlist]['tracks'])

def trim_new_playlist(playlists: dict = None):
  if not playlists: playlists = get_playlists()
  new_playlist_id = playlists[NEW_PLAYLIST]['id']
  outdated = [track['track_id'] for track in get_playlist_with_dates(new_playlist_id) if datetime.now(timezone.utc) - isoparse(track['added_at']) > timedelta(days=30)]
  # empty list check to avoid bad api requests
  if outdated: delete_from_playlist(new_playlist_id, outdated)

def update_playlists():
  liked_songs = get_liked_songs()
  playlists = get_playlists()
  if not liked_songs or not playlists: return
  new_songs = _get_new_songs(liked_songs, playlists)
  _add_new_songs(new_songs)
