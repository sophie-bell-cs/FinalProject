"""
Name: Sophia Bell
CS230: Section 4
Data: Boston AirBNB data
URL:

Description:
This program allows users to pick an AirBNB based off room type, neighborhood, price, and length of stay preferences.
It allows user to see how close their chosen AirBNB is to the airport and how far away the closest bus stop is. Finally,
it shows users data about AirBNBs in Boston, showing information about different neighborhoods, prices, listing amounts,
and reviews.
"""
import streamlit as st
from PIL import Image


#Home Page set up, provide information about site's capabilities
st.title('AirBNB Boston')
st.divider()
st.write("Discover the perfect place to stay in one of Boston's vibrant neighborhoods! Whether you're looking for cozy accommodations near historic landmarks, trendy spots close to the city's nightlife, or family-friendly options in peaceful surroundings, AirBNB Boston has got you covered.")
bostonPic = Image.open('external/Boston_ONS_Neighborhoods.svg.png')
st.image(bostonPic, use_container_width= True)  #[ST4]
st.write("Find an accomodation that fits your needs in greater Boston! Whether you're searching for an entire home, a stylish apartment, or a comfortable private room, we've got what you're looking for.")
apartmentPic = Image.open('external/images.jpeg')
st.image(apartmentPic, use_container_width= True)
st.write("Traveling to get here? Want to explore? We'll help you out! Find distances from Boston Logan Airport and nearby bus stations.")

#Navigation to page to search for an AirBNB
st.page_link('pages/Search.py')



