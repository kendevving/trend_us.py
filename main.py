import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_spotify_client():
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_top_tracks(country_code='US', limit=10):
    spotify = get_spotify_client()
    results = spotify.playlist_tracks(f"spotifycharts:{country_code}:daily", limit=limit)
    tracks = results['items']

    top_tracks = []
    for track in tracks:
        track_info = track['track']
        top_tracks.append({
            'name': track_info['name'],
            'artist': track_info['artists'][0]['name'],
            'popularity': track_info['popularity']
        })

    return top_tracks

def identify_trends(previous_top_tracks, current_top_tracks):
    new_trends = []

    for current_track in current_top_tracks:
        track_name = current_track['name']
        artist_name = current_track['artist']

        # Check if the track is new in the current top tracks
        if all(track['name'] != track_name or track['artist'] != artist_name for track in previous_top_tracks):
            new_trends.append({
                'name': track_name,
                'artist': artist_name,
                'popularity': current_track['popularity']
            })

    return new_trends

def main():
    # Example: Get top tracks for the United States
    country_code = 'US'
    current_top_tracks = get_top_tracks(country_code)

    # You can save the current top tracks to compare with future trends
    previous_top_tracks = current_top_tracks.copy()

    # Identify new trends based on the comparison with previous top tracks
    new_trends = identify_trends(previous_top_tracks, current_top_tracks)

    # Print the new trends
    print(f"New Trends in {country_code}:\n")
    for trend in new_trends:
        print(f"{trend['name']} by {trend['artist']} - Popularity: {trend['popularity']}")

if __name__ == "__main__":
    main()
