import streamlit as st
import pandas as pd
import math

#declare variables for distance calculations
EARTH_RADIUS = 3958.8
DEGREE_RADIAN = math.pi/180
AIRPORT_LONGITUDE = -71.010025
AIRPORT_LATITUDE = 42.3656

#function to calculate the distance between two places given their longitudes and latitudes
def findDistance(airbnbLong, airbnbLat, transitLong, transitLat):
    #converts to radians
    airbnbLong = airbnbLong * DEGREE_RADIAN
    airbnbLat = airbnbLat * DEGREE_RADIAN
    transitLong = transitLong * DEGREE_RADIAN
    transitLat = transitLat * DEGREE_RADIAN
    #finds difference between coordinates
    dlon = transitLong - airbnbLong
    dlat = transitLat - airbnbLat
    #uses equation from ChatGPT to manipulate variables to find distance
    a = math.sin(dlat / 2) ** 2 + math.cos(airbnbLat) * math.cos(transitLat) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS*c

#reads files, converts to format that is easily accesible with no errors, via pandas, cleaning, indexing, and creating lists
airbnb_df = pd.read_csv('/Users/sophiebell/PycharmProjects/pythonProject/FinalProject/external/listings.csv', index_col = 'name')
airbnb_df = airbnb_df[airbnb_df['availability_365'] != None]
neighborhood_df = pd.read_csv('/Users/sophiebell/PycharmProjects/pythonProject/FinalProject/external/neighbourhoods.csv')
neighborhood_list = neighborhood_df['neighbourhood']
busStops_df = pd.read_csv('FinalProject/external/PATI_Bus_Stops.csv', index_col ='Stop_Name')
#reads file containing chosen AirBNB ID, stores as an integer
placeID = open('/Users/sophiebell/PycharmProjects/pythonProject/FinalProject/external/chosenAirBNB.txt', 'r')
placeID = placeID.readline().strip()
placeID = int(placeID)

#page set up
st.title('AirBNB Boston')
st.header("Discover the closest bus stop to your Airbnb for hassle-free travel around Boston! Or, flying in? Check out how "
          "close you are to Boston Logan Airport for a smooth arrival.")
st.divider()

#checks if user has chosen an AirBNB yet, then finds the closes transport station to it
if placeID in airbnb_df['id'].values:
    #finds longitude and latitude of airBNB using ID
    placeLong = airbnb_df[airbnb_df['id'] == placeID]['longitude']
    placeLat = airbnb_df.loc[airbnb_df['id'] == placeID]['latitude']
    #determines whether user wants to find the distance to a bus stop or airport
    transport = st.selectbox("Which transportation method are you using?", ['Bus', 'Airport'])
    if transport == "Airport":
        milesA = findDistance(float(placeLong), float(placeLat), AIRPORT_LONGITUDE, AIRPORT_LATITUDE)
        st.subheader(f"The Boston Logan Airport is {round(milesA,2)} miles away from your AirBNB.")
    elif transport == "Bus":
        closest = 1000
        for index, row in busStops_df.iterrows(): #[DA8] Iterate through rows of a DataFrame with iterrows()
            #here, 8 and 9 are indexes to the columns with longitude and latitude data for each bus stop
            stopLong = float(row[7])
            stopLat = float(row[8])
            milesB = findDistance(placeLong, placeLat, stopLong, stopLat)
            if milesB < closest: #stores value of the distance between the stop only if its less than others that were found
                closest = milesB
                closestStop = index
        st.subheader(f"The closest bus stop to your AirBNB is {closestStop}. It is {round(closest, 2)} miles away.")
else:
    st.error('You have not selected an AirBNB to find transportation to.')

