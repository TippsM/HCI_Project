import json
import requests
from dotenv import load_dotenv
import os
import base64
from requests import post, get


#-----------------------------------------------------------------------------
# load/get API data
#-----------------------------------------------------------------------------

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("client_secret")

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

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

api_key = get_token()

#-----------------------------------------------------------------------------

def getArtistID(name, token):

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }

    params = (
        ('q', name),
        ('type', 'artist'),
    )

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params).json()

    for i in response["artists"]["items"]:
        try:
            if "id" in i:
                return i["id"]
        except ValueError:
            print ("This artist is available")

#-----------------------------------------------------------------------------

def getRecommendation(artist_id,token):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }

    params = (
        ('market', 'US'),
        ('seed_artists', artist_id),

    )

    response = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=params).json()
    lst=[]
    for i in response["tracks"]:
        song=(i["name"],i["album"]["artists"][0]["name"],i["external_urls"]["spotify"],i["album"]["images"][0]["url"])
        lst.append(song)
    return lst


#-----------------------------------------------------------------------------


def getToptracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    country = {"market": "US"}
    result = get(url, headers=headers, params=country)
    json_result = result.json()
    return json_result.get("tracks")

#-----------------------------------------------------------------------------

def geArtistData(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    country = {"market": "US"}
    result = get(url, headers=headers, params=country)
    return result.json()
