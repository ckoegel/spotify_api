import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from utils import *
from objects import *

scope_lib = "user-library-read"
scope_playlist = "playlist-read-private"
my_pl_cnt = 0
global_length = 0
global_maximum_playlist_names = {}
global_minimum_playlist_names = {}

# auth token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = os.environ.get('SPOTIFY_ID'), client_secret = os.environ.get('SPOTIFY_SECRET'), redirect_uri = os.environ.get('REDIRECT_URI'), scope=scope_playlist))

res_playlists = sp.current_user_playlists() # get list of playlists

for idx, playlist in enumerate(res_playlists['items']) : # for each playlist on account
    pl_name = playlist['name']
    tracks = playlist['tracks']
    num_songs = tracks['total']
    owner = playlist['owner']
    pl_id = playlist['id']
    
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
    max_length = 0
    max_pop = 0
    long_song = ""
    pop_song = ""
    track_uris = []
    
    if owner['id'] == "ckoegel1006" :  # do for only playlists created by me
        res_pl = sp.playlist(pl_id)
        tracklist = res_pl['tracks']
        my_pl_cnt += 1
        while 1:
            for cnt, track in enumerate(tracklist['items']) :
                track_info = track['track'] #get name, length, and popularity from here
                track_uris.append(track_info['id'])
                playlist_sums['popularity'] += track_info['popularity']
                
                if track_info['popularity'] > max_pop : # find maximum popularity value per playlist
                    max_pop = track_info['popularity']
                    pop_song = track_info['name']
                    pop_song_art = track_info['artists'][0]['name']
                
                if track_info['duration_ms'] > max_length : # find maximum song length per playlist
                    max_length = track_info['duration_ms']
                    long_song = track_info['name']
                    long_song_art = track_info['artists'][0]['name']

            if cnt == 99 : # for dealing with paginated results if playlist has over 100 songs
                audio_feats = sp.audio_features(tracks = track_uris) # get "audio features" for a group of tracks
        
                for ind, song in enumerate(audio_feats) : # for each songs features
                    
                    playlist_sums['danceability'] += audio_feats[ind]['danceability']
                    if audio_feats[ind]['danceability'] > global_max_dance: # find maximum song danceability
                        global_max_dance = audio_feats[ind]['danceability']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_dance_song = song_info['name']
                        global_max_dance_art = song_info['artists'][0]['name']
                    
                    playlist_sums['energy'] += audio_feats[ind]['energy']
                    if audio_feats[ind]['energy'] > global_max_energ: # find maximum song energy
                        global_max_energ = audio_feats[ind]['energy']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_energ_song = song_info['name']
                        global_max_energ_art = song_info['artists'][0]['name']
                    
                    playlist_sums['loudness'] += audio_feats[ind]['loudness']
                    if audio_feats[ind]['loudness'] > global_max_loud: # find maximum song loudness
                        global_max_loud = audio_feats[ind]['loudness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_loud_song = song_info['name']
                        global_max_loud_art = song_info['artists'][0]['name']
                    
                    playlist_sums['speechiness'] += audio_feats[ind]['speechiness']
                    if audio_feats[ind]['speechiness'] > global_max_speech: # find maximum song speechiness
                        global_max_speech = audio_feats[ind]['speechiness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_speech_song = song_info['name']
                        global_max_speech_art = song_info['artists'][0]['name']
                    
                    playlist_sums['acousticness'] += audio_feats[ind]['acousticness']
                    if audio_feats[ind]['acousticness'] > global_max_acous: # find maximum song acousticness
                        global_max_acous = audio_feats[ind]['acousticness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_acous_song = song_info['name']
                        global_max_acous_art = song_info['artists'][0]['name']
                    
                    playlist_sums['instrumentalness'] += audio_feats[ind]['instrumentalness']
                    if audio_feats[ind]['instrumentalness'] > global_max_instr: # find maximum song instrumentalness
                        global_max_instr = audio_feats[ind]['instrumentalness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_instr_song = song_info['name']
                        global_max_instr_art = song_info['artists'][0]['name']
                    
                    playlist_sums['valence'] += audio_feats[ind]['valence']
                    if audio_feats[ind]['valence'] > global_max_valen: # find maximum song valence(happiness)
                        global_max_valen = audio_feats[ind]['valence']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_valen_song = song_info['name']
                        global_max_valen_art = song_info['artists'][0]['name']
                    
                    playlist_sums['duration_ms'] += audio_feats[ind]['duration_ms']
                
                track_uris = [] # reset list of uris since max that can be requested at once is 100
            
            
            if tracklist['next'] : # if another page of tracks exists
                tracklist = sp.next(tracklist)
            else :
                audio_feats = sp.audio_features(tracks = track_uris)
                
                for ind, song in enumerate(audio_feats) : # does the same as above but for a page of less than 100 songs
                    
                    playlist_sums['danceability'] += audio_feats[ind]['danceability']
                    if audio_feats[ind]['danceability'] > global_max_dance:
                        global_max_dance = audio_feats[ind]['danceability']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_dance_song = song_info['name']
                        global_max_dance_art = song_info['artists'][0]['name']
                    
                    playlist_sums['energy'] += audio_feats[ind]['energy']
                    if audio_feats[ind]['energy'] > global_max_energ:
                        global_max_energ = audio_feats[ind]['energy']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_energ_song = song_info['name']
                        global_max_energ_art = song_info['artists'][0]['name']
                    
                    playlist_sums['loudness'] += audio_feats[ind]['loudness']
                    if audio_feats[ind]['loudness'] > global_max_loud:
                        global_max_loud = audio_feats[ind]['loudness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_loud_song = song_info['name']
                        global_max_loud_art = song_info['artists'][0]['name']
                    
                    playlist_sums['speechiness'] += audio_feats[ind]['speechiness']
                    if audio_feats[ind]['speechiness'] > global_max_speech:
                        global_max_speech = audio_feats[ind]['speechiness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_speech_song = song_info['name']
                        global_max_speech_art = song_info['artists'][0]['name']
                    
                    playlist_sums['acousticness'] += audio_feats[ind]['acousticness']
                    if audio_feats[ind]['acousticness'] > global_max_acous:
                        global_max_acous = audio_feats[ind]['acousticness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_acous_song = song_info['name']
                        global_max_acous_art = song_info['artists'][0]['name']
                    
                    playlist_sums['instrumentalness'] += audio_feats[ind]['instrumentalness']
                    if audio_feats[ind]['instrumentalness'] > global_max_instr:
                        global_max_instr = audio_feats[ind]['instrumentalness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_instr_song = song_info['name']
                        global_max_instr_art = song_info['artists'][0]['name']
                    
                    playlist_sums['valence'] += audio_feats[ind]['valence']
                    if audio_feats[ind]['valence'] > global_max_valen:
                        global_max_valen = audio_feats[ind]['valence']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_valen_song = song_info['name']
                        global_max_valen_art = song_info['artists'][0]['name']
                    
                    playlist_sums['duration_ms'] += audio_feats[ind]['duration_ms']
                
                track_uris = []
                break      
        
        # calculate averages for playlists and add to global total
        playlist_averages = {}
        for audio_feature in playlist_sums.keys():
            playlist_averages[audio_feature] = playlist_sums[audio_feature] / num_songs
            library_averages[audio_feature] += playlist_averages[audio_feature]
        
        global_length += playlist_sums['duration_ms']
        
        if max_length > global_max_length: # find maximum length song across all playlists
            global_max_length = max_length
            global_long_song = long_song
            global_max_long_art = long_song_art
        
        if max_pop > global_max_pop: # find maximum popularity song across all playlists
            global_max_pop = max_pop
            global_max_pop_song = pop_song
            global_max_pop_art = pop_song_art
        
        # find playlist with the highest average values for audio features
        
        for audio_feature in playlist_averages.keys():
            if playlist_averages[audio_feature] > global_playlist_maxes[audio_feature]:
                global_playlist_maxes[audio_feature] = playlist_averages[audio_feature]
                global_maximum_playlist_names[audio_feature] = pl_name
        
        # find playlist with the lowest average values for audio features

        for audio_feature in playlist_averages.keys():
            if playlist_averages[audio_feature] < global_playlist_mins[audio_feature]:
                global_playlist_mins[audio_feature] = playlist_averages[audio_feature]
                global_minimum_playlist_names[audio_feature] = pl_name

        # fixed_name = "{0:<18}".format(pl_name)
        # fixed_num_songs = "{0:>3}".format(str(num_songs))
        print(pl_name)
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
        print("Most Popular Song: %s (%d)" % (pop_song, max_pop))
        print("Longest Song: %s (%s)" % (long_song, parse_time(max_length)))
        print("Playlist Duration: %s" % (parse_time(playlist_sums['duration_ms'])))
        print("")
        
library_averages['popularity'] /= my_pl_cnt
library_averages['duration_ms'] /= my_pl_cnt
library_averages['danceability'] /= my_pl_cnt
library_averages['energy'] /= my_pl_cnt
library_averages['loudness'] /= my_pl_cnt
library_averages['speechiness'] /= my_pl_cnt
library_averages['acousticness'] /= my_pl_cnt
library_averages['instrumentalness'] /= my_pl_cnt
library_averages['valence'] /= my_pl_cnt
    
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
print("Most Danceable Song: %s by %s (%.5f)" % (global_max_dance_song, global_max_dance_art, global_max_dance))
print("Most Energetic Song: %s by %s (%.5f)" % (global_max_energ_song, global_max_energ_art, global_max_energ))
print("Loudest Song: %s by %s (%.5fdB)" % (global_max_loud_song, global_max_loud_art, global_max_loud))
print("Most Speechful Song: %s by %s (%.5f)" % (global_max_speech_song, global_max_speech_art, global_max_speech))
print("Most Acoustic Song: %s by %s (%.5f)" % (global_max_acous_song, global_max_acous_art, global_max_acous))
print("Most Instrumental Song: %s by %s (%.5f)" % (global_max_instr_song, global_max_instr_art, global_max_instr))
print("Happiest Song: %s by %s (%.5f)" % (global_max_valen_song, global_max_valen_art, global_max_valen))
print("Longest Song: %s by %s (%s)" % (global_long_song, global_max_long_art, parse_time(global_max_length)))
print("Most Popular Song : %s by %s (%d)" % (global_max_pop_song, global_max_pop_art, global_max_pop))
