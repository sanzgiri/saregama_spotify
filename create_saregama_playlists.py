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
        print(('Usage: {0} username playlist filename overwrite reprocess'.format(sys.argv[0])))
    else:
        username = sys.argv[1]
        plname = sys.argv[2]
        filename = sys.argv[3]
        overwrite = int(sys.argv[4])
        reprocess = int(sys.argv[5])

        notfoundfile = 'notfound_' + plname + '.txt'
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

            with open(filename, 'r') as f:

                trackidlist = []
                notfoundtracks = []
                found = 0

                for line in f:
                    line = line.strip()
                    if (reprocess == 1):
                        name = line
                    else:
                        m = re.search('^(\d+. )(.*)', line)
                        name = m.group(2)

                    track_id = get_track_id(name)
                    if track_id:
                        print("Found ", name, track_id)
                        trackidlist.append(track_id)
                        found += 1
                    else:
                        print("Can't find track: ", name)
                        notfoundtracks.append(name)

            print("Total tracks found = ", found)
            print("Total tracks not found = ", len(notfoundtracks))

            if (found > 0):
                nchunks = int(found / 100) + 1
                for k in range(nchunks):
                    trackid_chunk = trackidlist[k * 100: k * 100 + 100]
                    sp.user_playlist_add_tracks(username, playlist_id, trackid_chunk)


            with open(notfoundfile, 'w') as f:
                for t in notfoundtracks:
                    f.write(t + '\n')
