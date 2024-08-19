import streamlit as st
from PIL import Image

from functions import read_df
from functions import general_info as info
from functions import plot_bar_view_streamlit

from io import BytesIO

st.set_page_config( page_title='Country View', page_icon = "🌍",  layout="wide") 

image = Image.open('assets/icon.png')
logo  = Image.open('assets/logo.png')
st.logo(logo)


df,df1 = read_df()



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

    filtered_df = df[df['country_code'].isin(select_country)]
    filtered_df = filtered_df.loc[(filtered_df['country_code'].notna()) & (filtered_df['country_code'] != 0)]

    # Download button for the filtered DataFrame
    csv_buffer = BytesIO()
    filtered_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
#===================================
 #       session state
# ===========================

# List of sessions for session state variables
sessions = [
            'filter_selection_cities',
            'filter_selection_restaurants',
            'filter_selection_cuisines',
            'filter_select_unique_cuisines',
            'filter_select_votes',
            'filter_selection_views',
            'filter_selection_cost'
           ]

for session in sessions:
    if session not in st.session_state:
        st.session_state[session] = 'All'
        
## ==================================
#           Body
# =================================

st.markdown("# Select the view below 🔻")
with st.container():


# 1. Which country has the most cities registered?
    with st.expander("Cities per countries"):
        st.markdown("## Cities per countries")

        df_query1 = filtered_df[['country_code', 'city']].groupby('country_code').nunique().reset_index()
        df_query1 = df_query1.sort_values(by='city', ascending=False)
        df_plot1  = df_query1[df_query1['city'] > 0]
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            with st.container():

                # Define the options for the radio button
                options = ['Top5', 'Top10', 'All']

                # Use st.radio to create the filter selection widget
                with st.container():
                    st.session_state.filter_selection_cities = st.radio(
                                                                            "Filter Options: ", 
                                                                            options, 
                                                                            key = "cities_filter", 
                                                                            index=options.index(st.session_state.filter_selection_cities)
                                                                        )
                # Apply filter based on selection
                if st.session_state.filter_selection_cities == 'Top5':
                    selected_rows1 = df_plot1.head(5)
                elif st.session_state.filter_selection_cities == 'Top10':
                    selected_rows1 = df_plot1.head(10)
                else:  # Default to showing all rows if 'All' is selected
                    selected_rows1 = df_plot1
                
                # Display the selected rows
                st.table(selected_rows1.reset_index(drop=True))
      
        with col2:
            fig1 = plot_bar_view_streamlit2(selected_rows1, 'country_code', 'city', 
                                           title = f'{st.session_state.filter_selection_cities} cities per country', 
                                           figsize=(10, 6)
                                          )
#--\/--------------------------------------------------------------------------------------------------------------------------------------------------------
    # 2. Which country has the most restaurants registered?
    with st.expander("Restaurants per countries"):
        st.markdown("## Restaurants per countries")
    
        col1, col2 = st.columns([2, 3])
        
        with col1:
            with st.container():
                df_query2 = filtered_df[['country_code', 'restaurant_id']].groupby('country_code').nunique().reset_index()
                df_query2 = df_query2.sort_values(by='restaurant_id', ascending=False)
                df_plot2  = df_query2[df_query2['restaurant_id'] > 0]


                # Define the options for the radio button
                options = ['Top5', 'Top10', 'All']

                # Use st.radio to create the filter selection widget
                with st.container():
                    st.session_state.filter_selection_restaurants = st.radio(
                                                                            "Filter Options: ", 
                                                                            options, 
                                                                            key="restaurants_filter", 
                                                                            index=options.index(st.session_state.filter_selection_restaurants)
                                                                            )

                # Apply filter based on selection
                if st.session_state.filter_selection_restaurants == 'Top5':
                    selected_rows2 = df_plot2.head(5)
                elif st.session_state.filter_selection_restaurants == 'Top10':
                    selected_rows2 = df_plot2.head(10)
                else:  # Default to showing all rows if 'All' is selected
                    selected_rows2 = df_plot2
                
                # Display the selected rows
                st.table(selected_rows2.reset_index(drop=True))
      
        with col2:
            fig2 = plot_bar_view_streamlit(selected_rows2, 'country_code', 'restaurant_id', 
                                           title = f'{st.session_state.filter_selection_restaurants} restaurants per country', 
                                           figsize=(10, 6)
                                          )
        
#--\/----------------------------------------------------------------------------------------------------------------------------------------------------------
    # 3. What is the name of the country with the most restaurants with a price level of 'gourmet' registered?
    with st.expander("Price range per countries"):
        st.markdown("## Price range per countries")
    
        col1, col2 = st.columns([2, 3])
        
        with col1:
            with st.container():
                price_options = st.selectbox('Select price range 🔻', filtered_df['price_range'].unique().tolist())
                df_filtered_by_price = filtered_df[filtered_df['price_range'] == price_options]
    
               
                df_query3 = df_filtered_by_price[['country_code','price_range']].groupby('country_code').count().reset_index()
                df_query3 = df_query3.sort_values(by='price_range', ascending=False)
                df_plot3  = df_query3[df_query3['price_range'] > 0]
                
                # Define the options for the radio button
                options = ['Top5', 'Top10', 'All']
    
                # Use st.radio to create the filter selection widget
                st.session_state.filter_selection_cuisines = st.radio(
                                                                        "Filter Options: ", 
                                                                        options, 
                                                                        key="cuisine_filter", 
                                                                        index=options.index(st.session_state.get('filter_selection_cuisines', 'All'))
                                                                    )
    
                # Apply filter based on selection
                if st.session_state.filter_selection_cuisines == 'Top5':
                    selected_rows3 = df_plot3.head(5)
                elif st.session_state.filter_selection_cuisines == 'Top10':
                    selected_rows3 = df_plot3.head(10)
                else:  # Default to showing all rows if 'All' is selected
                    selected_rows3 = df_plot3
                
                # Display the selected rows
                st.table(selected_rows3.reset_index(drop=True))
      
        with col2:
            fig3 = plot_bar_view_streamlit(selected_rows3,'country_code', 'price_range', 
                                           title   = f'{price_options} per Country', 
                                           figsize = (10, 6)
                                          )

#--\/----------------------------------------------------------------------------------------------------------------------------------------------------------
    # 4. What is the name of the country with the highest number of distinct types of cuisine?
    with st.expander("Unique cuisines per countries"):
        st.markdown("## Unique cuisines per countries")
    
        col1, col2 = st.columns([2, 3])
        
        with col1:
            with st.container():
                
                # Group by country and count unique CUISINES
                df_query4 = filtered_df[filtered_df['cuisines'].notna()]
                df_query4 = df_query4[['country_code','cuisines']].groupby('country_code').nunique().reset_index()
                df_query4 = df_query4.sort_values(by='cuisines', ascending=False)
                df_plot4  = df_query4[df_query4['cuisines'] > 0]
                
                # Define the options for the radio button
                options = ['Top5', 'Top10', 'All']
    
                # Use st.radio to create the filter selection widget
                st.session_state.filter_select_unique_cuisines = st.radio(
                                                                    "Filter Options: ", 
                                                                    options, 
                                                                    key="unique_cuisine_filter", 
                                                                    index=options.index(st.session_state.get('filter_select_unique_cuisines', 'All'))
                                                                )
    
                # Apply filter based on selection
                if st.session_state.filter_select_unique_cuisines == 'Top5':
                    selected_rows4 = df_plot4.head(5)
                elif st.session_state.filter_select_unique_cuisines == 'Top10':
                    selected_rows4 = df_plot4.head(10)
                else:  # Default to showing all rows if 'All' is selected
                    selected_rows4 = df_plot4
                
                # Display the selected rows
                st.table(selected_rows4.reset_index(drop=True))
      
        with col2:
            fig3 = plot_bar_view_streamlit(selected_rows4, 'country_code', 'cuisines', 
                                           title   = f'{st.session_state.filter_select_unique_cuisines} unique cuisines per Country', 
                                           figsize = (10, 6)
                                          )


#--\/----------------------------------------------------------------------------------------------------------------------------------------------------------
    # 5. What is the name of the country with the highest number of reviews made?      
    with st.expander("Votes per cities"):
        st.markdown("## Votes per cities")
    
        col1, col2 = st.columns([2, 3])
            
        with col1:
            with st.container():
                
                # Calculate total votes per country
                df_query5 = filtered_df[['country_code', 'votes']].groupby('country_code').count().reset_index()
                df_query5 = df_query5.sort_values(by='votes', ascending=False)
                df_plot5  = df_query5[df_query5['votes'] > 0]
    
                # Correctly calculate average rating per country
                df_query51 = filtered_df[['country_code', 'aggregate_rating']].groupby('country_code')['aggregate_rating'].mean().reset_index()
                df_query51 = df_query51.sort_values(by='aggregate_rating', ascending=False)
                df_plot51 = df_query51[df_query51['aggregate_rating'] > 0]
                
                # Define the options for the radio button
                options = ['Top5', 'Top10', 'All']

                # Use st.radio to create the filter selection widget
                with st.container():
                    st.session_state.filter_select_votes = st.radio(
                                                                            "Filter Options: ", 
                                                                            options, 
                                                                            key = "votes_filter", 
                                                                            index=options.index(st.session_state.filter_select_votes)
                                                                        )
                # Apply filter based on selection
                if st.session_state.filter_select_votes == 'Top5':
                    selected_rows5  = df_plot5.head(5)
                    selected_rows51 = df_plot51.head(5)
                elif st.session_state.filter_select_votes == 'Top10':
                    selected_rows5 = df_plot5.head(10)
                    selected_rows51 = df_plot51.head(10)
                else:  # Default to showing all rows if 'All' is selected
                    selected_rows5 = df_plot5
                    selected_rows51 = df_plot51
                
                # Display the selected rows
                st.table(selected_rows5.reset_index(drop=True))
                st.table(selected_rows51.reset_index(drop=True))
      
        with col2:
            fig1 = plot_bar_view_streamlit(selected_rows5, 'country_code', 'votes', 
                                           title = f'{st.session_state.filter_select_votes} cities per country', 
                                           figsize=(10, 6)
                                          )


      
       
#--\/----------------------------------------------------
    #6 Booking, delivery status and online orders per country
    with st.expander("Booking, delivery and online orders per country"):
        st.markdown("## Booking, delivery and online orders per country")
    
        col1, col2 = st.columns([2, 3])
        
        with col1:
            with st.container():
                # Select price range
                view_options = st.selectbox('Select price range 🔻', ['has_table_booking','is_delivering_now','has_online_delivery'])
                
                # Ensure the column is treated as boolean for accurate summation
                filtered_df[view_options] = filtered_df[view_options].astype(bool)
                
                # Filter DataFrame based on selected option
                df_filtered_by_view = filtered_df[['country_code', view_options]]
                
                # Sum the boolean values (True becomes 1, False becomes 0)
                df_query6 = df_filtered_by_view.groupby('country_code')[view_options].sum().reset_index()
                df_query6 = df_query6.sort_values(by=view_options, ascending=False)
                df_plot6  = df_query6[df_query6[view_options] > 0]
                
                # Define the options for the radio button
                options = ['Top5', 'Top10', 'All']
    
                # Use st.radio to create the filter selection widget
                st.session_state.filter_selection_views = st.radio(
                                                                        "Filter Options: ", 
                                                                        options, 
                                                                        key="view_filter", 
                                                                        index=options.index(st.session_state.get('filter_selection_views', 'All'))
                                                                    )
    
                # Apply filter based on selection
                if st.session_state.filter_selection_views == 'Top5':
                    selected_rows6 = df_plot6.head(5)
                elif st.session_state.filter_selection_views == 'Top10':
                    selected_rows6 = df_plot6.head(10)
                else:  # Default to showing all rows if 'All' is selected
                    selected_rows6 = df_plot6
                
                # Display the selected rows
                st.table(selected_rows6.reset_index(drop=True))
      
        with col2:
            fig6 = plot_bar_view_streamlit(selected_rows6,'country_code', view_options, 
                                           title   = f'{view_options} per Country', 
                                           figsize = (10, 6)
                                          )
#--\/----------------------------------------------------
    #7 What is the average price of a dish for two people per country?
    with st.expander("Average cost for two per Country"):
        st.markdown("## Average cost for two per Country")
    
        col1, col2 = st.columns([2, 3])
        
        with col1:
            with st.container():
                df_query7 = filtered_df[['country_code', 'average_cost_for_two']].groupby('country_code')['average_cost_for_two'].mean().reset_index()
                df_query7 = df_query7.sort_values(by='average_cost_for_two', ascending=False)
                df_plot7  = df_query7[df_query7['average_cost_for_two'] > 0]


                # Define the options for the radio button
                options = ['Top5', 'Top10', 'All']
    
                # Use st.radio to create the filter selection widget
                st.session_state.filter_selection_cost = st.radio(
                                                                        "Filter Options: ", 
                                                                        options, 
                                                                        key="cost_filter", 
                                                                        index=options.index(st.session_state.get('filter_selection_cost', 'All'))
                                                                    )
    
                # Apply filter based on selection
                if st.session_state.filter_selection_cost == 'Top5':
                    selected_rows7 = df_plot7.head(5)
                elif st.session_state.filter_selection_cost == 'Top10':
                    selected_rows7 = df_plot7.head(10)
                else:  # Default to showing all rows if 'All' is selected
                    selected_rows7 = df_plot7
                
                # Display the selected rows
                st.table(selected_rows7.reset_index(drop=True))
      
        with col2:
            fig7 = plot_bar_view_streamlit(selected_rows7,'country_code', 'average_cost_for_two', 
                                           title   = f'{st.session_state.filter_selection_cost} Average cost for two per Country', 
                                           figsize = (10, 6)
                                          )