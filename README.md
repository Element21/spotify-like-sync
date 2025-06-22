# spotify-like-sync
Copy a Spotify user’s liked songs to Last.fm

# Setup
Run `pip install -r requirements.txt` to install the required Python modules.

Spotify and Last.fm API application credentials must be created in order to pull liked songs from Spotify and sync them to last.fm’s Loved Tracks.

## Spotify
[Click here](https://developer.spotify.com/dashboard/), sign in with your Spotify credentials and click ‘Create an app’. Once you’ve created an application, go the settings and add `http://localhost:1337` to the redirect URIs whitelist.

## Last.fm
[Click here](https://www.last.fm/api/account/create) to get API credentials to access last.fm.
[View all lastfm keys!](https://www.last.fm/api/accounts)

# Troubleshooting
- If you get an `INVALID_CLIENT: Invalid redirect URI` error when trying to authenticate with last.fm then you have not set the correct redirect URI on the developer dashboard.
