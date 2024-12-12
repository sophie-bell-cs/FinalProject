import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns #found from ChatGPT prompt: "packages that are easy to use to make data figures in python"

#read file, convert to format that is easily accesible with no errors, via cleaning, indexing, pandas, and creating lists
airbnb_df = pd.read_csv('external/listings.csv', index_col='name')
airbnb_df = airbnb_df[airbnb_df['availability_365'] != None]
neighborhood_df = pd.read_csv('external/neighbourhoods.csv')
neighborhood_series = neighborhood_df['neighbourhood']
neighborhood_list = [neighborhood_df.iloc[i, 1] for i in range(len(neighborhood_df))] #[PY4]


#function that, based on user input, creates a pivot table of stats for different aspects of an AirBNB listing based on location
def summaryStats(metrics, column='Price'):
    columnInfo = {  # identifies the actual column name from the more user-friendly displayed option,
        'Number of reviews': 'number_of_reviews',
        'Price': 'price',
        'Minimum length of stay': 'minimum_nights',
        'Number of days available': 'availability_365',
        'Last review': 'last_review', }  # [PY5] A dictionary where you write code to access its keys, values, or items
    columnName = columnInfo[column]
    statsWanted = []
    # Check which metrics the user has selected and calculate them
    if 'Mean' in metrics:
        statsWanted.append('=mean')
    if 'Minimum' in metrics:
        statsWanted.append('min')
    if 'Maximum' in metrics:
        statsWanted.append('max')
    pivotStats = airbnb_df.pivot_table(values = columnName, index="neighbourhood", aggfunc=statsWanted) #[DA3] Find Top largest or smallest values of a column
    return pivotStats

def additionalInfo(column): #[PY1] #calculates various stats that correspond to a given column in the datafrom
    stats = airbnb_df.groupby(column).agg(avg_price=('price', 'mean'), std_price=('price', 'mean'), minimum_nights=('minimum_nights', 'mean'),
                                                      avg_reviews=('number_of_reviews', 'mean')).reset_index()
    counts = airbnb_df.groupby(column).size().reset_index(name='count')
    return stats, counts

#page setup
st.title('AirBNB Boston')
st.divider()
st.header('Dataset used for AirBNB Boston')
st.write('AirBNB Boston works closely with hosts and renters to ensure the best experience for everyone. Explore '
         'the information we collect below.')

st.subheader('Representations')
selectPriceMetric = st.multiselect('Choose which price metrics to see:', ['Mean', 'Maximum', 'Minimum'])
priceTable = summaryStats(selectPriceMetric)
userCategory = st.radio('Select a different category to view metrics for:', ['Number of reviews', 'Price', 'Minimum length of stay',
                                                                           'Number of days available', 'Last review'])
selectCategoryMetric = st.multiselect('Choose metrics to see:', ['Mean', 'Maximum', 'Minimum'])
categoryTable = summaryStats(selectCategoryMetric, userCategory)
st.write(priceTable)

listingNumStats, listingNumCounts = additionalInfo('calculated_host_listings_count')
roomTypeStats, roomTypeCounts = additionalInfo('room_type')

# Set up Streamlit plot container
vizB, axes = plt.subplots(3, 1, figsize=(12, 12))

# Plot for calculated_host_listings_count statistics, where axes[0] is position in created container
axes[0].bar(listingNumStats['calculated_host_listings_count'], listingNumStats['avg_reviews'], color='red')
axes[0].set_title('Avg Reviews by Host Listing Count')
axes[0].set_xlabel('Host Listings Count')
axes[0].set_ylabel('Avg Reviews')

# Plots for room_type statistics
axes[1].bar(roomTypeStats['room_type'], roomTypeStats['avg_price'], color='orange')
axes[1].set_title('Avg Price by Room Type')
axes[1].set_xlabel('Room Type')
axes[1].set_ylabel('Avg Price') #[VIZ2]

axes[2].bar(roomTypeStats['room_type'], roomTypeStats['avg_reviews'], color='yellow')
axes[2].set_title('Avg Reviews by Room Type')
axes[2].set_xlabel('Room Type')
axes[2].set_ylabel('Avg Reviews')

#add room between plots so labels aren't overlapping
plt.subplots_adjust(hspace=.5)
#display plots in streamlit
st.pyplot(vizB)


specificCounts = airbnb_df.groupby(['neighbourhood', 'room_type']).size().reset_index(name='count')
vizC, axC = plt.subplots(figsize=(12, 8))
sns.barplot(x='neighbourhood', y='count', hue='room_type', data=specificCounts, ax=axC)
axC.set_title('Number of Listings per Room Type and Neighborhood')
axC.set_xticklabels(axC.get_xticklabels(), rotation=45, ha='right')
st.pyplot(vizC) #[VIZ3]

#source 2: https://seaborn.pydata.org/tutorial.html
#source 3: https://discuss.streamlit.io/t/how-to-display-matplotlib-graphs-in-streamlit-application/35383/2
