### README

```angular2html
### setup env variables for api creds
source spotify.sh

### show artist top 10 tracks
spotify show_artist_top_tracks.py <artist>

### show albums for artist
spotify show_artist_albums.py <artist>

### list playlists for user
spotify list_playlists.py <username>

### get playlists and tracks for user
spotify show_playlists.py <username>

### create new (public) playlist for user
spotify create_playlist.py <username> <playlist>

### create playlist by list of artists.txt
### if playlist exists it will be deleted
### filename should contain one artist per line
### playlist created will contain top 10 tracks for each artist
spotify create_playlist_by_artistlist.py <username> <playlist> <filename>

### create playlist by tracks
### filename is a list of track names to search
### this script assumes that playlist exists
### if overwrite = 1, existing playlist will be overwritten
### if overwrite = 0, tracks are appended
### not_found tracks are added to file notfound_<filename>

python create_playlist_by_tracks.py <username> <playlist> <filename> <overwrite>

### create saregama playlist
### filename is a list of track names to search
### this script assumes that playlist exists
### if overwrite = 1, existing playlist will be overwritten
### if overwrite = 0, tracks are appended
### not_found tracks are added to file notfound_<playlist>.txt
### if reprocess = 1, tracks from "notfound" file are reprocessed and appended to playlist (use with overwrite = 0)

python create_saregama_playlists.py <username> <playlist> <filename> <overwrite> <reprocess></reprocess>


```