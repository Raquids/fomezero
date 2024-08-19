import streamlit as st
import matplotlib.pyplot as plt

from io import BytesIO
from PIL import Image

from functions import read_df
from functions import general_info as info
from functions import plot_bar_view_streamlit2



st.set_page_config( page_title='City View', page_icon = "🍣", layout = 'wide') 


image = Image.open('assets/icon.png')
logo  = Image.open('assets/logo.png')
st.logo(logo)


df,df1 = read_df()


#===================================
 #       session state
# ===========================

sessions = [
            'filter_selection_city'
           ]

for session in sessions:
    if session not in st.session_state:
        st.session_state[session] = 'All'
        


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
    filtered_df = filtered_df.loc[(filtered_df['aggregate_rating'].notna()) & (filtered_df['aggregate_rating'] != 0)]
    filtered_df = filtered_df.loc[(filtered_df['average_cost_for_two'].notna()) & (filtered_df['average_cost_for_two'] != 0)]


# ===================================
#           Tabs
# ==================================


with st.container():
    col1, col2 = st.columns([1, 1], gap = 'large')

    with col1:
        with st.container():
            with st.container():
                st.markdown('# City View')
                
                # City selection dropbox 
                city_options = ['All cities'] + filtered_df['city'].unique().tolist()
                selected_city = st.selectbox('Select city 🔻', city_options)

                # Filter based on selected_city
                if selected_city != 'All cities':
                    filtered_df2 = filtered_df[filtered_df['city'] == selected_city]
                else:
                    filtered_df2 = filtered_df.copy()

                # aggregate_rating slider
                rate_slider = st.slider('Select minimun rating: ',
                                        min_value=0.0,
                                        max_value=5.0,
                                        step=0.5,
                                        value=filtered_df['aggregate_rating'].mean()
                                       )
                            
                # Filter based on rate_slider
                filtered_df2 = filtered_df2[(filtered_df2['aggregate_rating'] >= rate_slider)]

            with st.container():
                    # Correcting the column renaming issue
                    selected_rows         = filtered_df2[['restaurant_name','cuisines','average_cost_for_two','aggregate_rating']].dropna()
                    selected_rows_renamed = selected_rows.rename(columns={'average_cost_for_two': 'Cost for two USD', 
                                                                          'aggregate_rating': 'User Score',
                                                                          'restaurant_name':  'Franchise'
                                                                         })
                    st.dataframe(selected_rows_renamed.reset_index(drop=True))
                

            
    with col2:
        with st.container():
                    # Columns for displaying metrics
            col1, col2, col3, col4, col5 = st.columns(5)



            # Recalculate metrics based on filtered_df2
            num_cities             = len(filtered_df2['city'].unique())
            num_franchises         = len(filtered_df2['restaurant_name'].unique())
            num_cuisines           = len(filtered_df2['cuisines'].unique())
            num_votes              = filtered_df2['votes'].count()
            mean_votes             = round(filtered_df2['aggregate_rating'].mean(), 2)
            mean_cost              = round(filtered_df2['average_cost_for_two'].mean(), 2)

            
            # Display metrics using st.metric in each column
            with col1:
                st.metric(label="Selected Cities", value=num_cities)
            with col2:
                st.metric(label="Franchises", value=num_franchises)
            with col3:
                st.metric(label="Cuisines", value=num_cuisines)
            with col4:
                st.metric(label="Average cost :", value=mean_cost)
            with col5:
                st.metric(label="Average Rating", value= mean_votes)
                st.markdown('')
                st.metric(label="Total Ratings", value=num_votes)
        with st.container():
            st.markdown('---')
            col1,col2 = st.columns(2)
            # Extract the top 5 restaurant names
            with col1:
                top_5_restaurants = selected_rows_renamed['Franchise'].head(5).tolist()
                
                # Display the top 5 restaurants using a level 2 header
                st.markdown("## Top 5 Franchises:")
                for restaurant in top_5_restaurants:
                    st.markdown(f"- {restaurant}")
            with col2:
                # Sort the DataFrame in ascending order by 'aggregate_rating' and select the last 5
                bottom_5_restaurants = selected_rows_renamed.sort_values(by='User Score', ascending=True).tail(5)['Franchise'].tolist()
                
                # Display the bottom 5 restaurants using a level 2 header
                st.markdown("## Bot 5 Franchises:")
                for restaurant in bottom_5_restaurants:
                    st.markdown(f"- {restaurant}")






















            