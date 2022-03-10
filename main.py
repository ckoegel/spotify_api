import os
import math
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from objects import *

scope_lib = "user-library-read"
scope_playlist = "playlist-read-private"
my_pl_cnt = 0
global_length = 0
global_maximum_playlist_names = {}
global_minimum_playlist_names = {}
global_maximum_song_names = {}
global_maximum_song_artists = {}

def parse_time(time_ms) :   # parses a time duration in ms into a h:m:s string
    time_s = time_ms / 1000
    time_min = time_s / 60
    time_sec = time_s % 60
    
    if time_s > 3599 :
        time_hour = time_s / 3600
        time_min = time_s % 3600 / 60
        time_min_sec = str(math.trunc(time_hour)) + ":" + "{0:0>2}".format(str(math.trunc(time_min))) + ":" + "{0:0>2}".format(str(round(time_sec)))
    else :
        time_min_sec = str(math.trunc(time_min)) + ":" + "{0:0>2}".format(str(round(time_sec)))
    
    return time_min_sec

def update_audio_feature(audio_feature, audio_features) :
    if audio_features[audio_feature] > song_maximums[audio_feature]:
        song_maximums[audio_feature] = audio_features[audio_feature]
        song_info = sp.track(audio_features['id'])
        global_maximum_song_names[audio_feature] = song_info['name']
        global_maximum_song_artists[audio_feature] = song_info['artists'][0]['name']

# auth token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = os.environ.get('SPOTIFY_ID'), client_secret = os.environ.get('SPOTIFY_SECRET'), redirect_uri = os.environ.get('REDIRECT_URI'), scope=scope_playlist))

res_playlists = sp.current_user_playlists() # get list of playlists

for idx, playlist in enumerate(res_playlists['items']) : # for each playlist on account
    playlist_name = playlist['name']
    tracks = playlist['tracks']
    num_songs = tracks['total']
    owner = playlist['owner']
    playlist_id = playlist['id']
    
    playlist_sums = {
        'popularity': 0,
        'duration_ms': 0,
        'danceability': 0,
        'energy': 0,
        'loudness': 0,
        'speechiness': 0,
        'acousticness': 0,
        'instrumentalness': 0,
        'valence': 0
    }
    maximum_song_length = 0
    maximum_song_popularity = 0
    track_uris = []
    
    if owner['id'] == "ckoegel1006" :  # do for only playlists created by me
        res_pl = sp.playlist(playlist_id)
        tracklist = res_pl['tracks']
        my_pl_cnt += 1
        while 1:
            for cnt, track in enumerate(tracklist['items']) :
                track_info = track['track'] #get name, length, and popularity from here
                track_uris.append(track_info['id'])
                playlist_sums['popularity'] += track_info['popularity']
                
                # find maximum popularity value per playlist
                if track_info['popularity'] > maximum_song_popularity :
                    maximum_song_popularity = track_info['popularity']
                    most_popular_song_name = track_info['name']
                    most_popular_song_artist = track_info['artists'][0]['name']
                
                # find maximum song length per playlist
                if track_info['duration_ms'] > maximum_song_length :
                    maximum_song_length = track_info['duration_ms']
                    longest_song_name = track_info['name']
                    longest_song_artist = track_info['artists'][0]['name']

            if cnt == 99 : # for dealing with paginated results if playlist has over 100 songs
                audio_feats = sp.audio_features(tracks = track_uris) # get "audio features" for a group of tracks
        
                for ind, song in enumerate(audio_feats) : # for each songs features
                    
                    # add to playlist sums and update min and max songs for each audio feature
                    for audio_feature in audio_features_list:
                        playlist_sums[audio_feature] += audio_feats[ind][audio_feature]
                        update_audio_feature(audio_feature, audio_feats[ind])
                    
                    playlist_sums['duration_ms'] += audio_feats[ind]['duration_ms']
                
                track_uris = [] # reset list of uris since max that can be requested at once is 100
            
            
            if tracklist['next'] : # if another page of tracks exists
                tracklist = sp.next(tracklist)
            else :
                audio_feats = sp.audio_features(tracks = track_uris)
                
                for ind, song in enumerate(audio_feats) : # does the same as above but for a page of less than 100 songs
                    
                    # add to playlist sums and update min and max songs for each audio feature
                    for audio_feature in audio_features_list:
                        playlist_sums[audio_feature] += audio_feats[ind][audio_feature]
                        update_audio_feature(audio_feature, audio_feats[ind])
                    
                    playlist_sums['duration_ms'] += audio_feats[ind]['duration_ms']
                
                track_uris = []
                break      
        
        # calculate averages for playlists and add to global total
        playlist_averages = {}
        for audio_feature in playlist_sums.keys():
            playlist_averages[audio_feature] = playlist_sums[audio_feature] / num_songs
            library_averages[audio_feature] += playlist_averages[audio_feature]
        
        global_length += playlist_sums['duration_ms']
        
        # find maximum length song across all playlists
        if maximum_song_length > song_maximums['duration_ms']:
            song_maximums['duration_ms'] = maximum_song_length
            global_maximum_song_names['duration_ms'] = longest_song_name
            global_maximum_song_artists['duration_ms'] = longest_song_artist
        
        # find maximum popularity song across all playlists
        if maximum_song_popularity > song_maximums['popularity']:
            song_maximums['popularity'] = maximum_song_popularity
            global_maximum_song_names['popularity'] = most_popular_song_name
            global_maximum_song_artists['popularity'] = most_popular_song_artist
        
        # find playlist with the highest average values for audio features
        for audio_feature in playlist_averages.keys():
            if playlist_averages[audio_feature] > global_playlist_maxes[audio_feature]:
                global_playlist_maxes[audio_feature] = playlist_averages[audio_feature]
                global_maximum_playlist_names[audio_feature] = playlist_name
        
        # find playlist with the lowest average values for audio features
        for audio_feature in playlist_averages.keys():
            if playlist_averages[audio_feature] < global_playlist_mins[audio_feature]:
                global_playlist_mins[audio_feature] = playlist_averages[audio_feature]
                global_minimum_playlist_names[audio_feature] = playlist_name

        # fixed_name = "{0:<18}".format(playlist_name)
        # fixed_num_songs = "{0:>3}".format(str(num_songs))
        print(playlist_name)
        print("Songs: %d" % (num_songs))
        print("%.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %s" % (
            playlist_averages['danceability'], 
            playlist_averages['energy'], 
            playlist_averages['loudness'], 
            playlist_averages['speechiness'], 
            playlist_averages['acousticness'], 
            playlist_averages['instrumentalness'], 
            playlist_averages['valence'], 
            playlist_averages['popularity'], 
            parse_time(playlist_averages['duration_ms'])))
        print("Most Popular Song: %s by %s (%d)" % (most_popular_song_name, most_popular_song_artist, maximum_song_popularity))
        print("Longest Song: %s by %s (%s)" % (longest_song_name, longest_song_artist, parse_time(maximum_song_length)))
        print("Playlist Duration: %s" % (parse_time(playlist_sums['duration_ms'])))
        print("")
        
for audio_feature in library_averages.keys():
    library_averages[audio_feature] /= my_pl_cnt
    
print("Playlist Stats: \n---------------")
print("Highs:")
print("Most Danceable Playlist: %s (%.5f)" % (global_maximum_playlist_names['danceability'], global_playlist_maxes['danceability']))
print("Most Energetic Playlist: %s (%.5f)" % (global_maximum_playlist_names['energy'], global_playlist_maxes['energy']))
print("Loudest Playlist: %s (%.5fdB)" % (global_maximum_playlist_names['loudness'], global_playlist_maxes['loudness']))
print("Most Speechful Playlist: %s (%.5f)" % (global_maximum_playlist_names['speechiness'], global_playlist_maxes['speechiness']))
print("Most Acoustic Playlist: %s (%.5f)" % (global_maximum_playlist_names['acousticness'], global_playlist_maxes['acousticness']))
print("Most Instrumental Playlist: %s (%.5f)" % (global_maximum_playlist_names['instrumentalness'], global_playlist_maxes['instrumentalness']))
print("Happiest Playlist: %s (%.5f)" % (global_maximum_playlist_names['valence'], global_playlist_maxes['valence']))
print("Most Popular Playlist: %s (%.5f)" % (global_maximum_playlist_names['popularity'], global_playlist_maxes['popularity']))
print("Playlist with Longest Average Song Length: %s (%s)\n" % (global_maximum_playlist_names['duration_ms'], parse_time(global_playlist_maxes['duration_ms'])))
print("Lows:")
print("Least Danceable Playlist: %s (%.5f)" % (global_minimum_playlist_names['danceability'], global_playlist_mins['danceability']))
print("Least Energetic Playlist: %s (%.5f)" % (global_minimum_playlist_names['energy'], global_playlist_mins['energy']))
print("Quietest Playlist: %s (%.5fdB)" % (global_minimum_playlist_names['loudness'], global_playlist_mins['loudness']))
print("Least Speechful Playlist: %s (%.5f)" % (global_minimum_playlist_names['speechiness'], global_playlist_mins['speechiness']))
print("Least Acoustic Playlist: %s (%.5f)" % (global_minimum_playlist_names['acousticness'], global_playlist_mins['acousticness']))
print("Least Instrumental Playlist: %s (%.5f)" % (global_minimum_playlist_names['instrumentalness'], global_playlist_mins['instrumentalness']))
print("Saddest Playlist: %s (%.5f)" % (global_minimum_playlist_names['valence'], global_playlist_mins['valence']))
print("Least Popular Playlist: %s (%.5f)" % (global_minimum_playlist_names['popularity'], global_playlist_mins['popularity']))
print("Playlist with Shortest Average Song Length: %s (%s)\n" % (global_minimum_playlist_names['duration_ms'], parse_time(global_playlist_mins['duration_ms'])))
print("Totals")
print("Average Danceability: %.5f" % (library_averages['danceability']))
print("Average Energy: %.5f" % (library_averages['energy']))
print("Average Loudness: %.5fdB" % (library_averages['loudness']))
print("Average Speechfulness: %.5f" % (library_averages['speechiness']))
print("Average Acousticness: %.5f" % (library_averages['acousticness']))
print("Average Instrumentalness: %.5f" % (library_averages['instrumentalness']))
print("Overall Happiness: %.5f" % (library_averages['valence']))
print("Overall Popularity: %.5f" % (library_averages['popularity']))
print("Average Song Length: %s" % (parse_time(library_averages['duration_ms'])))
print("Total Length of All Playlists: %s\n" % (parse_time(global_length)))

print("\nSong Stats:\n-----------")
print("Highs:")
print("Most Danceable Song: %s by %s (%.5f)" % (global_maximum_song_names['danceability'], global_maximum_song_artists['danceability'], song_maximums['danceability']))
print("Most Energetic Song: %s by %s (%.5f)" % (global_maximum_song_names['energy'], global_maximum_song_artists['energy'], song_maximums['energy']))
print("Loudest Song: %s by %s (%.5fdB)" % (global_maximum_song_names['loudness'], global_maximum_song_artists['loudness'], song_maximums['loudness']))
print("Most Speechful Song: %s by %s (%.5f)" % (global_maximum_song_names['speechiness'], global_maximum_song_artists['speechiness'], song_maximums['speechiness']))
print("Most Acoustic Song: %s by %s (%.5f)" % (global_maximum_song_names['acousticness'], global_maximum_song_artists['acousticness'], song_maximums['acousticness']))
print("Most Instrumental Song: %s by %s (%.5f)" % (global_maximum_song_names['instrumentalness'], global_maximum_song_artists['instrumentalness'], song_maximums['instrumentalness']))
print("Happiest Song: %s by %s (%.5f)" % (global_maximum_song_names['valence'], global_maximum_song_artists['valence'], song_maximums['valence']))
print("Longest Song: %s by %s (%s)" % (global_maximum_song_names['duration_ms'], global_maximum_song_artists['duration_ms'], parse_time(song_maximums['duration_ms'])))
print("Most Popular Song : %s by %s (%d)" % (global_maximum_song_names['popularity'], global_maximum_song_artists['popularity'], song_maximums['popularity']))
