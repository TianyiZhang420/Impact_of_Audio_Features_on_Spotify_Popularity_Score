import requests
import time


def get_multiple_playlists_tracks(access_token, playlist_ids):
    """
    Fetches track information from multiple playlists using the Spotify API.

    Parameters:
    - access_token (str): The Spotify API access token.
    - playlist_ids (list): A list of playlist IDs to retrieve tracks from.

    Returns:
    - all_tracks_info (list): A list of dictionaries containing track details.
    """

    all_tracks_info = []  # Store all tracks info

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    for playlist_id in playlist_ids:
        playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        params = {
            "limit": 100,  # Retrieve up to 100 tracks per page
        }

        while playlist_url:
            response = requests.get(playlist_url, headers=headers, params=params)

            if response.status_code != 200:
                raise Exception(
                    f"Failed to get playlist tracks for playlist {playlist_id}: {response.status_code}, {response.text}"
                )

            data = response.json()

            # Loop through all items in the current page of results
            for item in data["items"]:
                track = item["track"]

                # Skip tracks that have None values in key fields
                if (
                    track is None
                    or track.get("id") is None
                    or track.get("name") is None
                    or not track.get("artists")
                    or track[  # Check if artists list exists and is non-empty
                        "artists"
                    ][0].get("name")
                    is None
                    # or track.get('release_date') is None
                    or track.get("duration_ms") is None
                    or track.get("popularity") is None
                    or track.get("preview_url") is None
                ):
                    continue  # Skip this track if any of the fields is None

                # If all required data is present, create track_info dictionary
                track_info = {
                    "id": track["id"],
                    "name": track["name"],
                    "release date": track["album"]["release_date"],
                    "artists": track["artists"][0]["name"],
                    "duration (ms)": track["duration_ms"],
                    "popularity": track["popularity"],
                    "preview url": track["preview_url"],
                }

                # Add track_info to all_tracks_info list
                all_tracks_info.append(track_info)

            # Check if there is a next page (pagination)
            playlist_url = data["next"]

            # Add a delay to prevent rate-limiting
            time.sleep(5)

    return all_tracks_info


def get_tracks_audio_features(track_ids, access_token, retries=3):
    """
    Fetch audio features for multiple tracks from Spotify API in batches of 50.

    Parameters:
    - track_ids (list): List of track IDs.
    - access_token (str): Spotify access token.
    - retries (int): Number of retries for each request in case of server errors.

    Returns:
    - all_audio_features (list): Audio feature data for the tracks.
    """

    batch_size = 50
    all_audio_features = []

    # Process track IDs in batches of 50
    for i in range(0, len(track_ids), batch_size):
        batch_ids = track_ids[i : i + batch_size]
        ids = ",".join(batch_ids)
        url = f"https://api.spotify.com/v1/audio-features?ids={ids}"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        # Retry logic in case of server errors
        for attempt in range(retries):
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "audio_features" in data:
                    all_audio_features.extend(data["audio_features"])
                break
            elif response.status_code >= 500:
                print(f"Server error {response.status_code}, retrying in 5 seconds...")
                time.sleep(5)  # Wait before retrying
            else:
                raise Exception(
                    f"Failed to get audio features: {response.status_code}, {response.text}"
                )

    return all_audio_features
