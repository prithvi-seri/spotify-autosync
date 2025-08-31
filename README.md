# Spotify New Music Automation

Automates organization of new music in Spotify.

When a user likes a song, the scipt adds it to "main", "new" and current month's playlists. Once a song has been in new for 30 days, it is removed from the playlist (to keep the new playlist up to date).

## Setup
1. Install poetry: \
    `pipx install poetry`
2. Install dependencies: \
   `poetry install`
3. Set up an app in the Spotify developer dashboard by following [these instructions](https://developer.spotify.com/documentation/web-api) and store your `CLIENT_ID` and `CLIENT_SECRET` in a .env file in the root directory
4. To run the script locally, switch to the `local` branch and run `poetry run py -m spotify_automation.main`. The first time you will be sent to a page to authorize access to your Spotify account.

`main` is configured to be run as a Lambda function on AWS (using SSM Parameter Store to store credentials)
