import numpy as np
import streamlit as st
import pandas as pd
import pydeck as pdk


#read files, convert to format that is easily accesible with no errors, via pandas, cleaning, and creating lists
airbnb_df = pd.read_csv("/Users/sophiebell/PycharmProjects/pythonProject/FinalProject/external/listings.csv",
                        index_col='name')
airbnb_df = airbnb_df[airbnb_df['availability_365'] != None]
neighborhood_df = pd.read_csv('/Users/sophiebell/PycharmProjects/pythonProject/FinalProject/external/neighbourhoods.csv')
neighborhood_series = neighborhood_df['neighbourhood']
neighborhood_list = [neighborhood_df.iloc[i, 1] for i in range(len(neighborhood_df))] #[PY4] A list comprehension
neighborhood_list.insert(0, 'Show All') #add the option to view AirBNBs in all neighborhoods

#set up page to get information from user selections and filter data accordingly
st.title('AirBNB Boston')
st.header('Find the right AirBNB for you.')
st.divider()

#first filter: by neighborhood
neighborhood = st.selectbox('Explore Neighborhoods', neighborhood_list)
airbnbFilterA = airbnb_df[airbnb_df['neighbourhood'] == neighborhood] #[ST1]
if neighborhood == "Show All":
    useData = airbnb_df
else:
    useData = airbnbFilterA

#second filter: room type
st.write("How much space do you need to make your stay perfect? Whether it’s a cozy private room or an entire house, let us know so we can help you find your ideal fit!")
roomType = st.radio("I'm looking for a(n)...", useData['room_type'].unique()) #[ST2]
#[DA4] Filter data by one condition
airbnbFilterB = useData[useData['room_type'] == roomType]

#third filter: stay length
st.write("Some hosts may have a minimum stay requirement for their listings. How many nights would you like to rent for?")
#[DA5] Filter data by two or more conditions
# minimum value for slider is the host's minimum stay requirement, maximum value for slider is the AirBNB's days available
nights = st.slider("Drag slider to desired length of stay (nights).", min(airbnbFilterB['minimum_nights']),
                   max(airbnbFilterB['availability_365']), )  # [ST3]
airbnbFilterC = airbnbFilterB[(airbnbFilterB['minimum_nights'] <= nights) & (airbnbFilterB['availability_365'] >= nights)]

#create pydeck map
#learned from source 4
hover_tooltip = {'html':f"<b>Name:</b> {airbnbFilterC.index[0]}", "style": {'backgroundColor': 'white', "color": 'black'}}
deckMap = pdk.Deck(initial_view_state = pdk.ViewState(latitude = np.mean(airbnbFilterC['latitude']),
                                                      longitude=np.mean(airbnbFilterC['longitude']), zoom=15, pitch=0),
                   layers=[pdk.Layer('ScatterplotLayer', data = airbnbFilterC, get_position=['longitude', 'latitude'],
                                     get_radius=18, get_fill_color = '[255,0,0]', pickable=True)], tooltip = hover_tooltip)

#show map with AirBNBs that meet the filter requirements as points, display number that matches criteria
st.pydeck_chart(deckMap)
st.write(len(airbnbFilterC), 'results')

#get final selection from user of AirBNB
st.divider()
st.subheader('Are you ready? Its time to choose your AirBNB! Select your choice.')
#display options for sort attributes for better usability, event though clicking on dataframe column headers will sort
sortType = st.radio('Sort Results:', ['Price, Ascending', 'Price, Descending', 'Alphabetical'])
#[DA2 Sort data in ascending or descending order]
if sortType == 'Price, Ascending':
    airbnbFilterC = airbnbFilterC.sort_values(by='price', ascending=True)
elif sortType == 'Price, Descending':
    airbnbFilterC = airbnbFilterC.sort_values(by='price', ascending=False)
elif sortType == 'Alphabetical':
    airbnbFilterC = airbnbFilterC.sort_values(by='name', ascending=True)

#create oppportunity for user to interact with dataframe to get selection information
#[DA9] Add a new column
airbnbFilterC['Select'] = False #set default value to not selected, found from source 1
st.write("Choose the AirBNB you wish to stay at:")
userChoice = st.data_editor(airbnbFilterC[['price', 'Select']], use_container_width=True)
airbnbFilterC.update(userChoice) #update dataframe based on selection to access later
selected = airbnbFilterC[airbnbFilterC['Select'] == True]

#checks only one AirBNB is selected, then writes the unique ID of the airBNB into a text file to use on a different page
if len(selected) == 1:
    choice = open('/Users/sophiebell/PycharmProjects/pythonProject/FinalProject/external/chosenAirBNB.txt', 'w')
    selectedID = selected.iloc[0]['id']
    selectedName = selected.index[0]
    choice.write(f"{selectedID}")
    st.subheader(f'Congratulations! You found your match at: {selectedName}.')
    choice.close()
    st.balloons()
else:
    st.write("Please choose ONE AirBNB.")

#source 1: https://discuss.streamlit.io/t/how-to-select-single-or-multiple-rows-in-st-dataframe-and-return-the-selected-data/54897






