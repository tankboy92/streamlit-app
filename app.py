import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

# Path to your CSV file
DATA_URL = (
    "/Users/idrissatankari/Documents/Pycharm/Motor_Vehicle_Collisions_-_Crashes_20240821.csv"
)

# Title and markdown description
st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a Streamlit dashboard that can be used to analyze motor vehicle collisions in NY")

# Function to load data
@st.cache_data(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[["CRASH DATE", "CRASH TIME"]])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash date_crash time': 'date/time'}, inplace=True)
    return data

# Load 100,000 rows of data
data = load_data(100000)

# Check the column names to ensure they're correct
st.write("Columns in the dataset:", data.columns.tolist())

# Slider for filtering injured persons
st.header("Where are the most people injured in NY?")
injured_people = st.slider("Number of Persons Injured in Vehicle Collisions", 0, 19)
filtered_data = data.query("`number of persons injured` >= @injured_people")[['latitude', 'longitude']].dropna(how="any")

# Display map with filtered data
st.map(filtered_data)

# Slider for filtering by hour
st.header("How many collisions occur during a given time of day")
hour = st.slider("Hour to look at", 0, 23)

# Filter the data by the selected hour
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle Collisions Between %i:00 and %i:00" % (hour, (hour + 1) % 24))

# Determine the midpoint for the map's initial view
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

# Display the map using PyDeck
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data[['date/time', 'latitude', 'longitude']],
            get_position=['longitude', 'latitude'],
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
        ),
    ],
))

# Subheader for the breakdown
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))

# Filter the data based on the selected hour
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]

# Create a histogram of the 'minute' from the filtered data
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]

# Convert the histogram data to a DataFrame for visualization
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})

# Create the bar chart using Plotly Express
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)

# Display the chart in Streamlit
st.write(fig)

st.header("Top 5 dangerous streets by affected type")
select = st.st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists','Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query(''))



# Checkbox to show raw data
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
