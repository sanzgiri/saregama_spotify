import sys
import os
import subprocess
import json
import spotipy
import spotipy.util as util

### List of spotify genres
### GET https://api.spotify.com/v1/recommendations/available-genre-seeds

"""
{
  "genres": [
    "acoustic",
    "afrobeat",
    "alt-rock",
    "alternative",
    "ambient",
    "anime",
    "black-metal",
    "bluegrass",
    "blues",
    "bossanova",
    "brazil",
    "breakbeat",
    "british",
    "cantopop",
    "chicago-house",
    "children",
    "chill",
    "classical",
    "club",
    "comedy",
    "country",
    "dance",
    "dancehall",
    "death-metal",
    "deep-house",
    "detroit-techno",
    "disco",
    "disney",
    "drum-and-bass",
    "dub",
    "dubstep",
    "edm",
    "electro",
    "electronic",
    "emo",
    "folk",
    "forro",
    "french",
    "funk",
    "garage",
    "german",
    "gospel",
    "goth",
    "grindcore",
    "groove",
    "grunge",
    "guitar",
    "happy",
    "hard-rock",
    "hardcore",
    "hardstyle",
    "heavy-metal",
    "hip-hop",
    "holidays",
    "honky-tonk",
    "house",
    "idm",
    "indian",
    "indie",
    "indie-pop",
    "industrial",
    "iranian",
    "j-dance",
    "j-idol",
    "j-pop",
    "j-rock",
    "jazz",
    "k-pop",
    "kids",
    "latin",
    "latino",
    "malay",
    "mandopop",
    "metal",
    "metal-misc",
    "metalcore",
    "minimal-techno",
    "movies",
    "mpb",
    "new-age",
    "new-release",
    "opera",
    "pagode",
    "party",
    "philippines-opm",
    "piano",
    "pop",
    "pop-film",
    "post-dubstep",
    "power-pop",
    "progressive-house",
    "psych-rock",
    "punk",
    "punk-rock",
    "r-n-b",
    "rainy-day",
    "reggae",
    "reggaeton",
    "road-trip",
    "rock",
    "rock-n-roll",
    "rockabilly",
    "romance",
    "sad",
    "salsa",
    "samba",
    "sertanejo",
    "show-tunes",
    "singer-songwriter",
    "ska",
    "sleep",
    "songwriter",
    "soul",
    "soundtracks",
    "spanish",
    "study",
    "summer",
    "swedish",
    "synth-pop",
    "tango",
    "techno",
    "trance",
    "trip-hop",
    "turkish",
    "work-out",
    "world-music"
  ]
}
"""

### Get Token from https://developer.spotify.com/console/get-search-item/
### Note this only lasts for a few hours
token = "XXX"
limit = 10
market = "US"

"""
query params (0 is low, 1 is high, can use min_, max_, target_)
acousticness: 0.0 to 1.0 
danceability: 0.0 to 1.0
energy: 0.0 to 1.0
imstrumentalness: 0.0 to 1.0 (>0.5 is instrumental)
key: 0 to 6?
liveness: 0.0 to 1.0 (>0.8 strong likelihood of live)
loudness: -60 to 0
mode: 1 (major), 0 (minor)
popularity: 0-100
speechiness: 0.0 to 1.0 (>0.66 only spoken words, 0.33=0.66 music & speech, <0.33 non-speech music)
tempo: bpm (range is 50-210)
time_signature
valence: 0.0 to 1.0 (sad to happy)
"""



def get_tracks(genre, query):

    cmd = """
curl -s -X \
    "GET" "https://api.spotify.com/v1/recommendations?limit={0}&market={1}&seed_genres={2}&{3}" -H \
    "Accept: application/json" -H \
    "Content-Type: application/json" -H \
    "Authorization: Bearer {4}"
""".format(limit, market, genre, query, token)

    result = os.popen(cmd).read()
    result = subprocess.check_output(cmd, shell=True)
    result2 = json.loads(result)

    num_tracks = len(result2['tracks'])
    print "Found {0} tracks".format(num_tracks)

    if num_tracks > 0:
        tracklist = []
        for i in range(num_tracks):
            album = result2['tracks'][i]['album']['name']
            track = result2['tracks'][i]['name']
            artist = result2['tracks'][i]['artists'][0]['name']
            id = result2['tracks'][i]['id']
            print album, artist, track, id
            tracklist.append(id)
        return tracklist
    else:
        return None


if __name__ == '__main__':

    if len(sys.argv) < 5:
        print(('Usage: {0} username playlist overwrite genre query'.format(sys.argv[0])))
    else:
        username = sys.argv[1]
        plname = sys.argv[2]
        overwrite = int(sys.argv[3])
        genre = sys.argv[4]
        query = sys.argv[5]

        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(username, scope)
        found_playlist = False

        if token:
            sp = spotipy.Spotify(auth=token)

            playlists = sp.user_playlists(username)

            for playlist in playlists['items']:
                if (playlist['name'] == plname):
                    playlist_id = playlist['id']
                    found_playlist = True
                    if (overwrite == 1):
                        print("Playlist exists, deleting: ", playlist_id)
                        sp.user_playlist_unfollow(username, playlist_id)
                        print("Recreating new playlist:")
                        sp.user_playlist_create(username, plname, True)
                        playlists = sp.user_playlists(username)
                        for playlist in playlists['items']:
                            if (playlist['name'] == plname):
                                playlist_id = playlist['id']
                    else:
                        print("Reusing existing playlist: ", playlist_id)
                    break

            if (found_playlist == False):
                print("Creating new playlist:")
                sp.user_playlist_create(username, plname, True)
                playlists = sp.user_playlists(username)
                for playlist in playlists['items']:
                    if (playlist['name'] == plname):
                        playlist_id = playlist['id']
                        break



            tracklist = get_tracks(genre, query)
            sp.user_playlist_add_tracks(username, playlist_id, tracklist)
            print "Playlist created!"