import json
import streamlit as st

import requests

#--------------------------------------------------------------------------------------

def read_from_file(file_name):
    with open(file_name,"r") as read_file:
        data=json.load(read_file)
        print("You successfully read from {}.".format(file_name))
    return data

def save_to_file(data,file_name):
    with open(file_name,"w") as write_file:
        json.dump(data,write_file,indent=2)
        print("You successfully saved to {}.".format(file_name))

#--------------------------------------------------------------------------------------

# map creator
#@st.cache_data
def map_creator(latitude, longitude):
    from streamlit_folium import folium_static
    import folium

    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)

#--------------------------------------------------------------------------------------

def getArtistCoordinates(artist_name):

    ticketmaster = st.secrets["TICKET_MASTER"]

    url = f"https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        'keyword': artist_name,
        'apikey': ticketmaster,
    }

    response = requests.get(url, params=params)

    data = response.json()
    events = data.get('_embedded', {}).get('events',[])

    if not events:
        return

    venue = events[0].get('_embedded', {}).get('venues', [])[0]
    
    if not venue:
        return
    
    location = venue.get('location').get('latitude'), venue.get('location').get('longitude')

    save_to_file(location, "artistCoordinates.json")

    return location


#--------------------------------------------------------------------------------------

