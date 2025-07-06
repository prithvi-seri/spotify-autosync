from utils import monthly_playlist

# Spotify API
REDIRECT_URI = 'https://github.com/prithvi-seri'
SCOPES = ['playlist-read-private', 'playlist-read-collaborative', 'playlist-modify-public', 'user-library-read', ]
SPOTIFY_ACCOUNTS_BASE_URL = 'https://accounts.spotify.com'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

# Storage
STORAGE_FILEPATH = '.storage'

# Python
NEW_MUSIC_PLAYLISTS = ['new', 'main', monthly_playlist()]

