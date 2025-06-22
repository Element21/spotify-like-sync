import pylast
import spotipy
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from spotipy.oauth2 import SpotifyOAuth

spotify_client_id = inquirer.text(message="Spotify client ID:").execute()
spotify_client_secret = inquirer.text(message="Spotify client secret:").execute()
lastfm_client_id = inquirer.text(message="Last.fm API key:").execute()
lastfm_client_secret = inquirer.text(message="Last.fm shared secret:").execute()
lastfm_username = inquirer.text(message="Last.fm username:").execute()
lastfm_password = pylast.md5(inquirer.text(message="Last.fm password:").execute())

lfm = pylast.LastFMNetwork(
    api_key=lastfm_client_id,
    api_secret=lastfm_client_secret,
    username=lastfm_username,
    password_hash=lastfm_password,
)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-library-read",
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri="http://127.0.0.1:1337",
    )
)

liked_songs = {"artist": [], "track": [], "length": 0}


def get_user_liked_songs(
    spotifyApiClient=sp,
    output_dict=liked_songs,
    limit=50,  # Max 50: https://developer.spotify.com/documentation/web-api/reference/get-users-saved-tracks
):
    "Returns a dictionary with keys (artist, track) of a spotify users liked songs"
    offset = 0
    while True:
        current_user_saved_tracks = spotifyApiClient.current_user_saved_tracks(
            limit=limit, offset=offset
        )
        current_user_saved_tracks_len = current_user_saved_tracks["total"]
        output_dict["length"] = current_user_saved_tracks_len

        if not current_user_saved_tracks["items"]:
            break  # No more songs

        for item in current_user_saved_tracks["items"]:
            track = item["track"]
            output_dict["artist"].append(track["artists"][0]["name"])
            output_dict["track"].append(track["name"])

        processed_count = len(output_dict["artist"])
        percentage = (
            round((processed_count / current_user_saved_tracks_len) * 100, 2)
            if current_user_saved_tracks_len > 0
            else None
        )
        print(
            f"Spotify: {processed_count}/{current_user_saved_tracks_len}, {percentage}%"
        )

        offset += limit

    return output_dict


spotify_liked = get_user_liked_songs()

# Like all songs in spotify playlist on last.fm
for idx, spotify_artist in enumerate(spotify_liked["artist"]):
    spotify_track = spotify_liked["track"][idx]
    try:
        track = lfm.get_track(artist=spotify_artist, title=spotify_track)
        track.love()
        print(
            f"Last.fm: {idx + 1}/{spotify_liked['length']}, {round(((idx + 1) / spotify_liked['length']) * 100, 2)}%"
        )
    except pylast.WSError as e:
        print(
            f"Could not find '{spotify_track}' by '{spotify_artist}' on Last.fm. Skipping. Error: {e}"
        )
