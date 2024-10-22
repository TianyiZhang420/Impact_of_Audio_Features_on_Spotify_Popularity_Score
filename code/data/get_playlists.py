import requests


def get_playlists(query, access_token, limit=10):
    """
    Fetches a list of playlist IDs from the Spotify API based on a search query.

    Parameters:
    - query (str): The search term used to find playlists.
    - access_token (str): The Spotify API access token required for authorization.
    - limit (int): The number of playlists to return (default is 10).

    Returns:
    - playlists_id (list): A list of playlist IDs that match the search query.
    """

    search_url = (
        f"https://api.spotify.com/v1/search?q={query}&type=playlist&limit={limit}"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(search_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        playlists_data = response.json()
    else:
        raise Exception(
            f"Failed to search playlists: {response.status_code}, {response.text}"
        )

    # Initialize an empty list to store playlist IDs
    playlists_id = []

    # Extract playlist IDs from the response and add them to the list
    for playlist in playlists_data["playlists"]["items"]:
        playlist_id = playlist["id"]
        playlists_id.append(playlist_id)

    return playlists_id
