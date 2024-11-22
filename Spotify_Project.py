import pandas as pd
import plotly.express as px
import main_functions
import streamlit as st
import spotify_Methods

st.sidebar.title("🎵Recommendations🎵")
st.sidebar.write( "Start searching to get suggestion...")

st.header("🎵Explore your Favourite Artist🎵")
st.subheader("Let's Get Started!")


with st.form("Choose an artist",clear_on_submit=True):
    artist = st.text_input("Enter the name of the artist")
    recommendation_amount = st.number_input("Enter the amount of recommendations you would like (Between 1-10)",step=1)
    submit = st.form_submit_button()

if artist != "":

    token = spotify_Methods.get_token()
    artist_id = spotify_Methods.getArtistID(artist,token)
    message = spotify_Methods.getRecommendation(artist_id,token)
    st.sidebar.info("Enjoy Recommendations Below!")
    st.sidebar.markdown("---")

    for i, song in enumerate(message):
        if i >= recommendation_amount:  # Stop when the index reaches the amount
            break
        st.sidebar.image(song[3], use_container_width=True)
        st.sidebar.subheader(song[1])
        st.sidebar.markdown(f"[{song[0]}]({song[2]})")
        st.sidebar.markdown("---")

    artist_id = spotify_Methods.getArtistID(artist, token)
    artist_data = spotify_Methods.geArtistData(token,artist_id)
    st.title(artist_data['name'])
    genres = ', '.join(map(str, artist_data['genres']))
    st.write("Genres: ", genres.title())
    st.write("Followers: ", artist_data['followers']['total'])
    st.write("Popularity: ", artist_data['popularity'])

    best_tracks, charts, map = st.tabs(['Best Songs', 'Charts', 'Map'])

    with best_tracks:
        st.header("🎵Best Songs🎵")
        message2 = spotify_Methods.getToptracks(token, artist_id)
        tracks = message2[0:9]

        for row in range(3):
            cols = st.columns(3)
            for col_index, col in enumerate(cols):
                item_index = row * 3 + col_index
                if item_index < len(tracks):
                    album = tracks[item_index]
                    with col:
                        st.image(album['album']['images'][0]['url'], use_container_width=True)
                        st.write(album['name'])

    with charts:
        name_popularity = [{"name": track["name"], "popularity": track["popularity"]} for track in message2]
        df = pd.DataFrame(name_popularity)
        col1, col2 = st.columns(2)
        with col1:
            chart_type = st.selectbox(label="Select the type of chart", options=["Line chart", "Bar chart", "Table"])
        with col2:
            color_picked = st.color_picker("Choose the color", "#1ed760")

        if chart_type == "Line chart":
            line = px.line(df, x=df['name'], y=df['popularity'])
            line.update_traces(line_color=color_picked)
            st.plotly_chart(line)
        elif chart_type == "Bar chart":
            bar = px.bar(df, x="name", y="popularity")
            bar.update_traces(marker_color= color_picked)
            st.plotly_chart(bar)
        else:
            parsed_data = []
            for track in message2:
                parsed_data.append({
                    "Song Name": track["name"],
                    "Artist": ", ".join(artist["name"] for artist in track["artists"]),
                    "Album": track["album"]["name"],
                    "Release Date": track["album"]["release_date"],
                    "Popularity": track["popularity"],
                    "Explicit": "Yes" if track["explicit"] else "No"
                })
            df = pd.DataFrame(parsed_data)
            data_length = st.slider(label="Pick a length for the table", min_value=0, max_value=9, value=9)
            df_new = df[0:data_length]
            st.dataframe(df_new)

    with map:
        st.subheader("🎵Nearest Event of " + artist_data["name"] + "🎵")
        mapView = st.checkbox("Show Map")

        if mapView:

            coordinates = main_functions.getArtistCoordinates(artist)
            main_functions.map_creator(coordinates[0], coordinates[1])
else:
    st.error("🚨Please Enter an Artist🚨")
