# Spotify New Music Automation

Automates organization of new music in Spotify.

When a user adds song to a specific playlist ("new"), add it to "main" playlist and current month's playlist. Once a song has been in new for 30 days, it is removed from the playlist (to keep new up to date).

## Setup
1. Install poetry: \
    `pipx install poetry`
2. Install dependencies: \
   `poetry install`
3. Set up an app in the Spotify developer dashboard by following [these instructions](https://developer.spotify.com/documentation/web-api) and store your `CLIENT_ID` and `CLIENT_SECRET` in a .env file in the root directory
4. Run `main.py`. The first time you will be sent to a page to authorize access to your Spotify account.
