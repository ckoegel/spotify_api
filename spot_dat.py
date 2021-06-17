import requests
import json
import math
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_info import *

scope_lib = "user-library-read"
scope_playlist = "playlist-read-private"

my_pl_cnt = 0

# global maximum playlist averages across all playlists
global_max_length = 0
global_max_pop = 0
global_duration = 0
global_max_avg_dance = 0
global_max_avg_energ = 0
global_max_avg_loud = -60
global_max_avg_speech = 0
global_max_avg_acous = 0
global_max_avg_instr = 0
global_max_avg_valen = 0
global_max_avg_pop = 0
global_max_avg_length = 0

# global minimum playlist averages across all playlists
global_min_avg_dance = 1.1
global_min_avg_energ = 1.1
global_min_avg_loud = 10
global_min_avg_speech = 1.1
global_min_avg_acous = 1.1
global_min_avg_instr = 1.1
global_min_avg_valen = 1.1
global_min_avg_pop = 101
global_min_avg_length = 300000

# global averages across all playlists
global_avg_dance = 0
global_avg_energ = 0
global_avg_loud = 0
global_avg_speech = 0
global_avg_acous = 0
global_avg_instr = 0
global_avg_valen = 0
global_avg_pop = 0
global_length = 0

# global maximum song values
global_max_length = 0
global_max_pop = 0
global_max_dance = 0
global_max_energ = 0
global_max_loud = -60
global_max_speech = 0
global_max_acous = 0
global_max_instr = 0
global_max_valen = 0

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


# auth token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = cl_id, client_secret = cl_sec, redirect_uri = red_uri, scope=scope_playlist))

res_playlists = sp.current_user_playlists() # get list of playlists

for idx, playlist in enumerate(res_playlists['items']) : # for each playlist on account
    pl_name = playlist['name']
    tracks = playlist['tracks']
    num_songs = tracks['total']
    owner = playlist['owner']
    pl_id = playlist['id']
    
    sum_dance = 0
    sum_energ = 0
    sum_loud = 0
    sum_speech = 0
    sum_acous = 0
    sum_instr = 0
    sum_valen = 0
    sum_length = 0
    max_length = 0
    sum_pop = 0
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
                sum_pop += track_info['popularity']
                
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
                    
                    sum_dance += audio_feats[ind]['danceability']
                    if audio_feats[ind]['danceability'] > global_max_dance: # find maximum song danceability
                        global_max_dance = audio_feats[ind]['danceability']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_dance_song = song_info['name']
                        global_max_dance_art = song_info['artists'][0]['name']
                    
                    sum_energ += audio_feats[ind]['energy']
                    if audio_feats[ind]['energy'] > global_max_energ: # find maximum song energy
                        global_max_energ = audio_feats[ind]['energy']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_energ_song = song_info['name']
                        global_max_energ_art = song_info['artists'][0]['name']
                    
                    sum_loud += audio_feats[ind]['loudness']
                    if audio_feats[ind]['loudness'] > global_max_loud: # find maximum song loudness
                        global_max_loud = audio_feats[ind]['loudness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_loud_song = song_info['name']
                        global_max_loud_art = song_info['artists'][0]['name']
                    
                    sum_speech += audio_feats[ind]['speechiness']
                    if audio_feats[ind]['speechiness'] > global_max_speech: # find maximum song speechiness
                        global_max_speech = audio_feats[ind]['speechiness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_speech_song = song_info['name']
                        global_max_speech_art = song_info['artists'][0]['name']
                    
                    sum_acous += audio_feats[ind]['acousticness']
                    if audio_feats[ind]['acousticness'] > global_max_acous: # find maximum song acousticness
                        global_max_acous = audio_feats[ind]['acousticness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_acous_song = song_info['name']
                        global_max_acous_art = song_info['artists'][0]['name']
                    
                    sum_instr += audio_feats[ind]['instrumentalness']
                    if audio_feats[ind]['instrumentalness'] > global_max_instr: # find maximum song instrumentalness
                        global_max_instr = audio_feats[ind]['instrumentalness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_instr_song = song_info['name']
                        global_max_instr_art = song_info['artists'][0]['name']
                    
                    sum_valen += audio_feats[ind]['valence']
                    if audio_feats[ind]['valence'] > global_max_valen: # find maximum song valence(happiness)
                        global_max_valen = audio_feats[ind]['valence']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_valen_song = song_info['name']
                        global_max_valen_art = song_info['artists'][0]['name']
                    
                    sum_length += audio_feats[ind]['duration_ms']
                
                track_uris = [] # reset list of uris since max that can be requested at once is 100
            
            
            if tracklist['next'] : # if another page of tracks exists
                tracklist = sp.next(tracklist)
            else :
                audio_feats = sp.audio_features(tracks = track_uris)
                
                for ind, song in enumerate(audio_feats) : # does the same as above but for a page of less than 100 songs
                    
                    sum_dance += audio_feats[ind]['danceability']
                    if audio_feats[ind]['danceability'] > global_max_dance:
                        global_max_dance = audio_feats[ind]['danceability']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_dance_song = song_info['name']
                        global_max_dance_art = song_info['artists'][0]['name']
                    
                    sum_energ += audio_feats[ind]['energy']
                    if audio_feats[ind]['energy'] > global_max_energ:
                        global_max_energ = audio_feats[ind]['energy']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_energ_song = song_info['name']
                        global_max_energ_art = song_info['artists'][0]['name']
                    
                    sum_loud += audio_feats[ind]['loudness']
                    if audio_feats[ind]['loudness'] > global_max_loud:
                        global_max_loud = audio_feats[ind]['loudness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_loud_song = song_info['name']
                        global_max_loud_art = song_info['artists'][0]['name']
                    
                    sum_speech += audio_feats[ind]['speechiness']
                    if audio_feats[ind]['speechiness'] > global_max_speech:
                        global_max_speech = audio_feats[ind]['speechiness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_speech_song = song_info['name']
                        global_max_speech_art = song_info['artists'][0]['name']
                    
                    sum_acous += audio_feats[ind]['acousticness']
                    if audio_feats[ind]['acousticness'] > global_max_acous:
                        global_max_acous = audio_feats[ind]['acousticness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_acous_song = song_info['name']
                        global_max_acous_art = song_info['artists'][0]['name']
                    
                    sum_instr += audio_feats[ind]['instrumentalness']
                    if audio_feats[ind]['instrumentalness'] > global_max_instr:
                        global_max_instr = audio_feats[ind]['instrumentalness']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_instr_song = song_info['name']
                        global_max_instr_art = song_info['artists'][0]['name']
                    
                    sum_valen += audio_feats[ind]['valence']
                    if audio_feats[ind]['valence'] > global_max_valen:
                        global_max_valen = audio_feats[ind]['valence']
                        song_info = sp.track(audio_feats[ind]['id'])
                        global_max_valen_song = song_info['name']
                        global_max_valen_art = song_info['artists'][0]['name']
                    
                    sum_length += audio_feats[ind]['duration_ms']
                
                track_uris = []
                break      
        
        # calculate averages for playlists and add to global total
        avg_dance = sum_dance / num_songs
        global_avg_dance += avg_dance
        
        avg_energ = sum_energ / num_songs
        global_avg_energ += avg_energ
        
        avg_loud = sum_loud / num_songs
        global_avg_loud += avg_loud
        
        avg_speech = sum_speech / num_songs
        global_avg_speech += avg_speech
        
        avg_acous = sum_acous / num_songs
        global_avg_acous += avg_acous
        
        avg_instr = sum_instr / num_songs
        global_avg_instr += avg_instr
        
        avg_valen = sum_valen / num_songs
        global_avg_valen += avg_valen
        
        avg_pop = sum_pop / num_songs
        global_avg_pop += avg_pop
        
        avg_length = sum_length / num_songs
        global_length += sum_length
        
        if max_length > global_max_length: # find maximum length song across all playlists
            global_max_length = max_length
            global_long_song = long_song
            global_max_long_art = long_song_art
        
        if max_pop > global_max_pop: # find maximum popularity song across all playlists
            global_max_pop = max_pop
            global_max_pop_song = pop_song
            global_max_pop_art = pop_song_art
        
        # playlist maximums
        
        if avg_length > global_max_avg_length: # find maximum average song length across all playlists
            global_max_avg_length = avg_length
            global_max_avg_length_pl = pl_name
        
        if avg_dance > global_max_avg_dance: # find maximum average danceability across all playlists
            global_max_avg_dance = avg_dance
            global_max_avg_dance_pl = pl_name
        
        if avg_energ > global_max_avg_energ: # find maximum average energy across all playlists
            global_max_avg_energ = avg_energ
            global_max_avg_energ_pl = pl_name
            
        if avg_loud > global_max_avg_loud: # find maximum average loudness across all playlists
            global_max_avg_loud = avg_loud
            global_max_avg_loud_pl = pl_name
        
        if avg_speech > global_max_avg_speech: # find maximum average speechiness across all playlists
            global_max_avg_speech = avg_speech
            global_max_avg_speech_pl = pl_name
        
        if avg_acous > global_max_avg_acous: # find maximum average acousticness across all playlists
            global_max_avg_acous = avg_acous
            global_max_avg_acous_pl = pl_name
        
        if avg_instr > global_max_avg_instr: # find maximum average instrumentalness across all playlists
            global_max_avg_instr = avg_instr
            global_max_avg_instr_pl = pl_name
        
        if avg_valen > global_max_avg_valen: # find maximum average valence across all playlists
            global_max_avg_valen = avg_valen
            global_max_avg_valen_pl = pl_name
            
        if avg_pop > global_max_avg_pop: # find maximum average popularity across all playlists
            global_max_avg_pop = avg_pop
            global_max_avg_pop_pl = pl_name
        
        # playlist minimums
        
        if avg_length < global_min_avg_length: # find minimum average song length across all playlists
            global_min_avg_length = avg_length
            global_min_avg_length_pl = pl_name
        
        if avg_dance < global_min_avg_dance:
            global_min_avg_dance = avg_dance
            global_min_avg_dance_pl = pl_name
        
        if avg_energ < global_min_avg_energ:
            global_min_avg_energ = avg_energ
            global_min_avg_energ_pl = pl_name
            
        if avg_loud < global_min_avg_loud:
            global_min_avg_loud = avg_loud
            global_min_avg_loud_pl = pl_name
        
        if avg_speech < global_min_avg_speech:
            global_min_avg_speech = avg_speech
            global_min_avg_speech_pl = pl_name
        
        if avg_acous < global_min_avg_acous:
            global_min_avg_acous = avg_acous
            global_min_avg_acous_pl = pl_name
        
        if avg_instr < global_min_avg_instr:
            global_min_avg_instr = avg_instr
            global_min_avg_instr_pl = pl_name
        
        if avg_valen < global_min_avg_valen:
            global_min_avg_valen = avg_valen
            global_min_avg_valen_pl = pl_name
            
        if avg_pop < global_min_avg_pop:
            global_min_avg_pop = avg_pop
            global_min_avg_pop_pl = pl_name
        
        fixed_name = "{0:<18}".format(pl_name)
        fixed_num_songs = "{0:>3}".format(str(num_songs))
        print(pl_name)
        print("Songs: %d" % (num_songs))
        print("%.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %s" % (avg_dance, avg_energ, avg_loud, avg_speech, avg_acous, avg_instr, avg_valen, avg_pop, parse_time(avg_length)))
        print("Most Popular Song: %s (%d)" % (pop_song, max_pop))
        print("Longest Song: %s (%s)" % (long_song, parse_time(max_length)))
        print("Playlist Duration: %s" % (parse_time(sum_length)))
        print("")
        
global_avg_dance /= my_pl_cnt
global_avg_energ /= my_pl_cnt
global_avg_loud /= my_pl_cnt
global_avg_speech /= my_pl_cnt
global_avg_acous /= my_pl_cnt
global_avg_instr /= my_pl_cnt
global_avg_valen /= my_pl_cnt
global_avg_pop /= my_pl_cnt
    
print("Playlist Stats: \n---------------")
print("Highs:")
print("Most Danceable Playlist: %s (%.5f)" % (global_max_avg_dance_pl, global_max_avg_dance))
print("Most Energetic Playlist: %s (%.5f)" % (global_max_avg_energ_pl, global_max_avg_energ))
print("Loudest Playlist: %s (%.5fdB)" % (global_max_avg_loud_pl, global_max_avg_loud))
print("Most Speechful Playlist: %s (%.5f)" % (global_max_avg_speech_pl, global_max_avg_speech))
print("Most Acoustic Playlist: %s (%.5f)" % (global_max_avg_acous_pl, global_max_avg_acous))
print("Most Instrumental Playlist: %s (%.5f)" % (global_max_avg_instr_pl, global_max_avg_instr))
print("Happiest Playlist: %s (%.5f)" % (global_max_avg_valen_pl, global_max_avg_valen))
print("Most Popular Playlist: %s (%.5f)" % (global_max_avg_pop_pl, global_max_avg_pop))
print("Playlist with Longest Average Song Length %s (%s)\n" % (global_max_avg_length_pl, parse_time(global_max_avg_length)))
print("Lows:")
print("Least Danceable Playlist: %s (%.5f)" % (global_min_avg_dance_pl, global_min_avg_dance))
print("Least Energetic Playlist: %s (%.5f)" % (global_min_avg_energ_pl, global_min_avg_energ))
print("Quietest Playlist: %s (%.5fdB)" % (global_min_avg_loud_pl, global_min_avg_loud))
print("Least Speechful Playlist: %s (%.5f)" % (global_min_avg_speech_pl, global_min_avg_speech))
print("Least Acoustic Playlist: %s (%.5f)" % (global_min_avg_acous_pl, global_min_avg_acous))
print("Least Instrumental Playlist: %s (%.5f)" % (global_min_avg_instr_pl, global_min_avg_instr))
print("Saddest Playlist: %s (%.5f)" % (global_min_avg_valen_pl, global_min_avg_valen))
print("Least Popular Playlist: %s (%.5f)" % (global_min_avg_pop_pl, global_min_avg_pop))
print("Playlist with Shortest Average Song Length %s (%s)\n" % (global_min_avg_length_pl, parse_time(global_min_avg_length)))
print("Totals")
print("Average Danceability: %.5f" % (global_avg_dance))
print("Average Energy: %.5f" % (global_avg_energ))
print("Average Loudness: %.5fdB" % (global_avg_loud))
print("Average Speechfulness: %.5f" % (global_avg_speech))
print("Average Acousticness: %.5f" % (global_avg_acous))
print("Average Instrumentalness: %.5f" % (global_avg_instr))
print("Overall Happiness: %.5f" % (global_avg_valen))
print("Overall Popularity: %.5f" % (global_avg_pop))
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
   
   
   
   
   
   
   
    