import pylast
import spotipy
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from spotipy.oauth2 import SpotifyOAuth

spotify_client_id = inquirer.text(message="Spotify client id:").execute()
spotify_client_secret = inquirer.text(message="Spotify client secret:").execute()
lastfm_client_id = inquirer.text(message="Last.fm client id:").execute()
lastfm_client_secret = inquirer.text(message="Last.fm client secret:").execute()
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
        redirect_uri="http://localhost:1337",
    )
)

liked_songs = {"artist": [], "track": [], "length": 0}


def get_user_liked_songs(
    spotifyApiClient=sp,
    output_dict=liked_songs,
    limit=1,
    offset=0,  # User will somtimes have an odd number of liked songs, so we can only request 1 at a time so we dont go over the playlist length
):
    "Returns a dictionary with keys (artist, track) of a spotify users liked songs"
    current_user_saved_tracks = spotifyApiClient.current_user_saved_tracks(
        limit=limit, offset=offset
    )
    current_user_saved_tracks_len = current_user_saved_tracks["total"]
    output_dict["length"] = current_user_saved_tracks_len

    while offset <= current_user_saved_tracks_len:
        for item in current_user_saved_tracks["items"]:
            track = item["track"]
            output_dict["artist"].append(track["artists"][0]["name"])
            output_dict["track"].append(track["name"])
        print(
            f"Spotify: {offset}/{current_user_saved_tracks_len}, {round((offset / current_user_saved_tracks_len)*100, 2)}%"
        )
        offset += limit
        return get_user_liked_songs(
            spotifyApiClient=sp, output_dict=liked_songs, limit=limit, offset=offset
        )  # Recurse until we have the whole like songs playlist
    return output_dict


spotify_liked = get_user_liked_songs()

lastfm_track = 0

# Like all songs in spotify playlist on last.fm
for idx, spotify_artist in enumerate(spotify_liked["artist"]):
    spotify_track = spotify_liked["track"][idx]
    track = lfm.get_track(artist=spotify_artist, title=spotify_track)
    track.love()
    print(
        f"Last.fm: {lastfm_track + 1}/{spotify_liked['length']}, {round((lastfm_track + 1 / spotify_liked['length'])*100, 2)}%"
    )
    lastfm_track += 1
