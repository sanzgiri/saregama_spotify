import sys
import os
import subprocess
import json
import spotipy
import spotipy.util as util
import pandas as pd

''' get album id from artist & album
'''

### Get Token from https://developer.spotify.com/console/get-search-item/
### Note this only lasts for a few hours
token = "XXX"

def get_album_id_from_artist_album(artist, album):

    artist = artist.strip()
    album = album.strip()

    artist = artist.replace(" ", "%20")
    album = album.replace(" ", "%20")

    cmd = """
curl -s -X \
    "GET" "https://api.spotify.com/v1/search?q=album%3A{0}%20artist%3A{1}&type=album" -H \
    "Accept: application/json" -H \
    "Content-Type: application/json" -H \
    "Authorization: Bearer {2}"
""".format(album, artist, token)

    result = os.popen(cmd).read()
    result = subprocess.check_output(cmd, shell=True)
    result2 = json.loads(result)

    items = result2['albums']['items']
    if (len(items) > 0):
        return items[0]['id']
    else:
        return None


def get_album_id_from_album(album):

    album = album.strip()
    album = album.replace(" ", "%20")

    cmd = """
curl -s -X \
    "GET" "https://api.spotify.com/v1/search?q=album%3A{0}&type=album" -H \
    "Accept: application/json" -H \
    "Content-Type: application/json" -H \
    "Authorization: Bearer {1}"
""".format(album, token)

    result = os.popen(cmd).read()
    result = subprocess.check_output(cmd, shell=True)
    result2 = json.loads(result)

    items = result2['albums']['items']
    if (len(items) > 0):
        return items[0]['id']
    else:
        return None



if __name__ == '__main__':

    if len(sys.argv) < 4:
        print(('Usage: {0} username playlist filename overwrite'.format(sys.argv[0])))
    else:
        username = sys.argv[1]
        plname = sys.argv[2]
        filename = sys.argv[3]
        overwrite = int(sys.argv[4])

        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(username,scope)
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

            df = pd.read_csv(filename, header=None, names=['artist','album'])
            df = df.drop_duplicates()
            df = df.sort_values(by='artist')
            print("Unique Albums = ", len(df))

            albumidlist = []
            found = 0

            for i in range(len(df)):
        
                artist = df.artist.iloc[i]
                album = df.album.iloc[i]

                album_id = get_album_id_from_artist_album(artist, album)
                if album_id:
                    albumidlist.append(album_id)
                    found += 1
                else:
                    print("Can't find: ", artist, album)

            unique_albums = list(set(albumidlist))

            print("Total albums found = ", found)
            print("Unique albums found = ", len(unique_albums))

            for album in unique_albums:
                tracklist = []
                results = sp.album_tracks(album)
                tracks = results['items']

                for j in range(len(tracks)):
                    tracklist.append(tracks[j]['id'])

                print("Appending from album {0}: {1} tracks".format(album, len(tracks)))
                sp.user_playlist_add_tracks(username, playlist_id, tracklist)
