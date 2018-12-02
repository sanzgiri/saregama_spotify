import sys
import re
import spotipy
import spotipy.util as util

''' shows the albums and tracks for a given artist.
'''

def get_track_id(name):
    results = sp.search(q='track:' + name, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        return items[0]['id']
    else:
        return None

if __name__ == '__main__':

    if len(sys.argv) < 5:
        print(('Usage: {0} username playlist filename overwrite'.format(sys.argv[0])))
    else:
        username = sys.argv[1]
        plname = sys.argv[2]
        filename = sys.argv[3]
        overwrite = int(sys.argv[4])

        notfoundfile = 'notfound_' + filename
        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(username,scope)

        if token:
            sp = spotipy.Spotify(auth=token)
            playlists = sp.user_playlists(username)

            for playlist in playlists['items']:
                if (playlist['name'] == plname):
                    playlist_id = playlist['id']

                    if (overwrite == 1):
                        print("Playlist exists, deleting: ", playlist_id)
                        sp.user_playlist_unfollow(username, playlist_id)
                        print("Creating new playlist:")
                        sp.user_playlist_create(username, plname, True)
                        playlists = sp.user_playlists(username)
                        for playlist in playlists['items']:
                            if (playlist['name'] == plname):
                                playlist_id = playlist['id']
                    else:
                        print("Reusing: ", playlist_id)

                    break

            with open(filename, 'r') as f:

                trackidlist = []
                notfoundtracks = []
                found = 1

                for line in f:
                    name = line.strip()
                    track_id = get_track_id(name)
                    if track_id:
                        print("Found ", name, track_id)
                        trackidlist.append(track_id)
                        found += 1
                    else:
                        print("Can't find track: ", name)
                        notfoundtracks.append(name)
                    if (found % 100 == 0):
                        sp.user_playlist_add_tracks(username, playlist_id, trackidlist)
                        trackidlist = []

            print("Total tracks found = ", found)

            with open(notfoundfile, 'w') as f:
                for t in notfoundtracks:
                    f.write(t + '\n')
