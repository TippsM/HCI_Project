import time

from pyarrow import nulls

import main_functions
import spotify_Methods
import streamlit as st

from spotify_Methods import get_token

st.sidebar.title("🎵Recommendation🎵")
st.sidebar.subheader("♪ Get Some Recommendations Based on Artists ♪")

st.title("Welcome to Spotify Music Helper!")
st.subheader("Let's Get Started!")

with st.form("Choose an artist",clear_on_submit=True):
    artist = st.text_input("Enter the name of an Artist!",value="")

    submit = st.form_submit_button()


if submit:
    if artist.strip() == "":
        st.warning("Please Enter an Artist!")
    else:

        token = spotify_Methods.get_token()
        artist_id = spotify_Methods.getArtistID(artist,token)
        message = spotify_Methods.getRecommendation(artist_id,token)
        main_functions.save_to_file(message, 'recommendations.json')
        st.sidebar.info("Enjoy Recommendations Below!")
        st.sidebar.markdown("---")

        for song in message:
            col1, col2 = st.columns([1,2])
            with col1:
                st.sidebar.image(song[3], width=300)
            with col2:
                st.sidebar.subheader(song[0])
                st.sidebar.write(f"""*{song[1]}*""")
                st.sidebar.markdown(f"[Listen on Spotify]({song[2]})")

            st.sidebar.markdown("---")