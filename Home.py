import folium    

import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

from io import StringIO, BytesIO
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

from functions import read_df
from functions import general_info as info



# Set up the page configuration with the sidebar initially expanded
st.set_page_config(
    page_title='Your Dashboard Title',
    page_icon='🍽',
    layout = 'wide'
)

image = Image.open('assets/icon.png')
logo  = Image.open('assets/logo.png')
st.logo(logo)

# Read the data
df, df1 = read_df()

# ===================================
#            Main Page
# ==================================
st.write('# Welcome to Your Dashboard')

# ===================================
#            Sidebar
# ==================================
with st.sidebar.container():
    st.sidebar.image(image, use_column_width=True)
    st.sidebar.markdown('# Countries:')
    
    # Multiselect widget for selecting countries
    select_country = st.sidebar.multiselect('Select Countries:', 
                                           list(df['country_code'].unique()), 
                                           default=list(df['country_code'].unique()))

# Filter the DataFrame based on the selected countries
filtered_df = df[df['country_code'].isin(select_country)]

# Download button for the filtered DataFrame
csv_buffer = BytesIO()
filtered_df.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)

download_link = st.download_button(
    label="Download Filtered Data",
    data=csv_buffer,
    file_name=f"filtered_data_{filtered_df.shape[0]}_records.csv",
    mime="text/csv"
)
# Counters for unique values
num_selected_countries = len(set(select_country))
num_franchises         = len(filtered_df['restaurant_name'].unique())
num_cities             = len(filtered_df['city'].unique())
num_cuisines           = len(filtered_df['cuisines'].unique())
num_votes              = len(filtered_df['votes'])



with st.container():
    # Columns for displaying metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Display metrics using st.metric in each column
    with col1:
        st.metric( label = "Selected Countries", value=num_selected_countries)
    with col2:
        st.metric( label = "Franchises",         value=num_franchises)
    with col3: 
        st.metric( label = "Cities",             value=num_cities)
    with col4:
        st.metric( label = "Cuisines",           value=num_cuisines)
    with col5:
        st.metric( label = "Total Ratings",           value=num_votes)
    
    # Container for viewing the data
    
    with st.container():
        st.markdown("# Restaurant Locations")
    
        col2, col3 = st.columns([4, 2])
    
        with col2:
            cols = ['latitude', 'longitude', 'city', 'price_range', 'rating_color', 'cuisines']
            literal_cols = ['city', 'price_range', 'rating_color', 'cuisines']
            df_aux = filtered_df.loc[:, cols]
            df_aux = df_aux.groupby(literal_cols).median().reset_index().dropna()
        
            m = folium.Map(zoom_start=18)
            marker_cluster = MarkerCluster().add_to(m)
            
            for index, location_info in df_aux.iterrows():
                popup_content = (
                    f"City:           {location_info['city']}                 <br>"
                    f"Main Cuisine:   {location_info['cuisines']}              <br>"  
                    f"Price Range:    {location_info['price_range']}          <br>"
                )
        
                icon_color = location_info['rating_color']
                
                folium.Marker([location_info['latitude'],
                               location_info['longitude']],
                               popup=folium.Popup(popup_content, max_width=300),
                               icon=folium.Icon(color=icon_color)
                ).add_to(marker_cluster)
            
            folium_static(m, width=1024, height=600)
        with col3:
            st.title('')

