# list of audio features
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
song_maximums = {
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
