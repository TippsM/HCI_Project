import json

import requests
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import main_functions
import streamlit as st

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

def getRecommendation(artist_id,token,target_popularity,target_danceability,target_energy,target_instrumentalness):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }

    params = (
        ('market', 'US'),
        ('seed_artists', artist_id),
        ('target_popularity', target_popularity),
        ('target_danceability',target_danceability),
        ('target_energy',target_energy),
        ('target_instrumentalness',target_instrumentalness)
    )

    response = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=params).json()
    lst=[]
    for i in response["tracks"]:
        song=(i["name"],i["album"]["artists"][0]["name"],i["external_urls"]["spotify"],i["album"]["images"][0]["url"])
        lst.append(song)
    return lst


def get_artist_top_tracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    country = {"market": "US"}
    result = get(url, headers=headers, params=country)
    json_result = result.json()
    return json_result.get("tracks", [])



st.title("🎵Recomenda🎵")
st.header("Unleash your Playlist Potential")
st.subheader("Explore personalized music recommendations and uncover new tracks tailored to your taste with the power of the Spotify API ♪")

with st.form("Choose an artist",clear_on_submit=True):
    artist = st.text_input("Enter the name of the artist",value="")
    with st.expander("Want to customize your recommendations?"):
        popularity = st.slider("Adjust the popularity:", min_value=0, max_value=100, step=1, value=50)
        danceability = st.slider("Adjust the danceability:", min_value=0.0, max_value=1.0, step=0.1, value = 0.5)
        energy = st.slider("Adjust the energy:", min_value=0.0, max_value=1.0, step=0.01, value = 0.5)
        instrumentalness = st.slider("Adjust the instrumentalness:", min_value=0.0, max_value=1.0, step=0.01, value = 0.5)
    submit = st.form_submit_button()

if submit:
    token = api_key
    artist_id = getArtistID(artist,token)
    message=getRecommendation(artist_id,token,popularity,danceability,energy,instrumentalness)
    st.markdown("---")
    for song in message:
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(song[3], width=300)
        with col2:
            st.subheader(song[0])
            st.write(f"""*{song[1]}*""")
            st.markdown(f"[Listen on Spotify]({song[2]})")
        st.markdown("---")