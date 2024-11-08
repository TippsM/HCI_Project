import json

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import main_functions

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("client_secret")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers,data=data)
    json_result = json.loads(result.content)

    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_artist_top_tracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    country = {"market": "US"}
    result = get(url, headers=headers, params=country)
    json_result = result.json()
    return json_result.get("tracks", [])

def save_top_tracks_to_file(tracks, filename="top_tracks.json"):
    with open(filename, "w") as file:
        json.dump({"top_tracks": tracks}, file, indent=4)
    print(f"Top tracks saved to {filename}")

artist_id = "246dkjvS1zLTtiykXe5h60"
api_key = get_token()
top_tracks = get_artist_top_tracks(api_key, artist_id)
save_top_tracks_to_file(top_tracks)
