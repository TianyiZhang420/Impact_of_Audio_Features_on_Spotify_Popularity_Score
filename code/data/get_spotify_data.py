from get_playlists import get_playlists
from get_tracks import get_multiple_playlists_tracks, get_tracks_audio_features
import requests
import base64
from dotenv import load_dotenv
import os
import csv
import pandas as pd


def get_access_token(client_id, client_secret):
    """
    Retrieves the access token from Spotify using the Client Credentials Flow.

    Parameters:
    - client_id (str): Your Spotify application's client ID.
    - client_secret (str): Your Spotify application's client secret.

    Returns:
    - access_token (str): The Spotify access token.

    Raises:
    - Exception: If the request fails or the token cannot be retrieved.
    """

    # Spotify authentication URL for retrieving the token
    auth_url = "https://accounts.spotify.com/api/token"
    # Encode client_id and client_secret to base64
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(
        "utf-8"
    )

    headers = {
        "Authorization": f"Basic {auth_header}",
    }

    data = {"grant_type": "client_credentials"}

    # Make the POST request to get the access token
    response = requests.post(auth_url, headers=headers, data=data)

    # Check if the request is successful (status code 200)
    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"]
    else:
        raise Exception(
            f"Failed to get access token: {response.status_code}, {response.text}"
        )


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from the .env file

    # Retrieve Spotify client credentials from environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # Get an access token
    access_token = get_access_token(client_id, client_secret)

    # Search for playlists related to the query 'English songs' retrieve their IDs
    query = "English songs"
    playlists_id = get_playlists(query, access_token, 50)  # Retrieve their IDs

    # Fetch all tracks information from the retrieved playlists and collect tracks' IDs
    all_tracks_info = get_multiple_playlists_tracks(access_token, playlists_id)
    all_tracks_id = []
    for track in all_tracks_info:
        all_tracks_id.append(track["id"])

    # Retrieve audio features for the tracks using their IDs
    all_tracks_features = get_tracks_audio_features(all_tracks_id, access_token)

    # Update the track info with the corresponding audio features
    for i in range(0, len(all_tracks_info)):
        try:
            print(all_tracks_info[i])
        except IndexError:
            break  # Exit the loop if the index is out of range

        if all_tracks_features[i] is not None:
            all_tracks_info[i].update(all_tracks_features[i])
        else:
            all_tracks_info.remove(
                all_tracks_info[i]
            )  # Remove track if features are missing

    # Define the directory for storing the CSV output
    current_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(current_dir, "..", "..", "artifacts")

    # Define the path to the CSV file
    CSV_PATH = os.path.join(artifacts_dir, "spotify_data.csv")

    # Create the directory if it doesn't exist
    os.makedirs(artifacts_dir, exist_ok=True)

    # Write the collected track information to a CSV file
    with open(CSV_PATH, "w", newline="") as csvfile:
        fieldnames = all_tracks_info[0].keys()

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for track in all_tracks_info:
            writer.writerow(track)

    df = pd.read_csv(CSV_PATH)

    df.dropna(inplace=True)  # Drop nan values
    df = df.drop_duplicates()  # Remove duplicates
    df = df.drop(columns=["duration (ms)"])  # Remove the duplicated column

    df.to_csv(CSV_PATH, index=False)  # Store the new data in the original file
