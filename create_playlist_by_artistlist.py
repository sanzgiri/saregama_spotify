import sys
import re
import spotipy
import spotipy.util as util

''' shows the albums and tracks for a given artist.
'''

def get_artist_urn(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]['uri']
    else:
        return None

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print(('Usage: {0} username playlist filename'.format(sys.argv[0])))
    else:
        username = sys.argv[1]
        plname = sys.argv[2]
        filename = sys.argv[3]

        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(username,scope)

        if token:
            sp = spotipy.Spotify(auth=token)
            playlists = sp.user_playlists(username)

            for playlist in playlists['items']:
                if (playlist['name'] == plname):
                    playlist_id = playlist['id']
                    print("Playlist exists, deleting: ", playlist_id)
                    sp.user_playlist_unfollow(username, playlist_id)
                    break

            print("Creating playlist:")
            sp.user_playlist_create(username, plname, True)
            playlists = sp.user_playlists(username)
            for playlist in playlists['items']:
                if (playlist['name'] == plname):
                    playlist_id = playlist['id']
                    print("Using: ", playlist_id)


            f = open(filename, 'r')
            for line in f:
                name = line.strip()

#               print line
#                m = re.search('(.*) - (.*)', line)
#                name = m.group(1)
#                track = m.group(2)
#                n = re.match('(\w+) \(?\w+', track)
#                track = n.group(1)

                artist_urn = get_artist_urn(name)
                if artist_urn:
                    print("Found ", name)
                    artist_tracks = []
                    response = sp.artist_top_tracks(artist_urn, country='US')
                    for track in response['tracks']:
                        track_id = track['id']
                        artist_tracks.append(track_id)
                    if (len(artist_tracks) > 0):
                        sp.user_playlist_add_tracks(username, playlist_id, artist_tracks)
                    else:
                        print "No tracks for " + name
                        print(track['name'])
                else:
                    print "Can't find artist " + name
