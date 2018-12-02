# shows artist info for a URN or URL

import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
import sys
import os

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

credentials = oauth2.SpotifyClientCredentials(
        client_id=os.environ['SPOTIPY_CLIENT_ID'],
        client_secret=os.environ['SPOTIPY_CLIENT_SECRET'])

token = credentials.get_access_token()

sp = spotipy.Spotify(token)

if len(sys.argv) > 1:
    urn = get_artist(sys.argv[1])['uri']
else:
    urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

response = sp.artist_top_tracks(urn)

for track in response['tracks']:
    print(track['name'])
