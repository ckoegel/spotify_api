
audio_features_list = [
    'danceability',
    'energy',
    'loudness',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'valence'
]

# global maximum playlist averages across all playlists
global_playlist_maxes = {
    'popularity': 0,
    'duration_ms': 0,
    'danceability': 0,
    'energy': 0,
    'loudness': -60,
    'speechiness': 0,
    'acousticness': 0,
    'instrumentalness': 0,
    'valence': 0,
}

# global minimum playlist averages across all playlists
global_playlist_mins = {
    'popularity': 101,
    'duration_ms': 300000,
    'danceability': 1.1,
    'energy': 1.1,
    'loudness': 10,
    'speechiness': 1.1,
    'acousticness': 1.1,
    'instrumentalness': 1.1,
    'valence': 1.1,
}

# global averages across all playlists
library_averages = {
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