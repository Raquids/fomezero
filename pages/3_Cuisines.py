import streamlit as st
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO

from functions import read_df
from functions import general_info as info
from functions import plot_bar_view_streamlit2









st.set_page_config( page_title='Cuisine View', page_icon = "🍽",  layout="wide") 


image = Image.open('assets/icon.png')
logo  = Image.open('assets/logo.png')
st.logo(logo)


df,df1 = read_df()

#===================================
 #       session state
# ===========================

# List of sessions for session state variables
sessions = [
            'cuisine_rating'
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
    

        
## ==================================
#           Body
# =================================
with st.container():
    col1, col2 = st.columns([2, 3])
    
    with col1:
        with st.container():
            # Include 'All cuisines' as an option
            cuisine_options = ['All cuisines'] + filtered_df['cuisines'].unique().tolist()
            selected_cuisine = st.selectbox('Select cuisine 🔻', cuisine_options)
            
            # Handle the case where 'All cuisines' is selected
            if selected_cuisine == 'All cuisines':
                # Calculate the mean aggregate_rating for all cuisines
                df_filtered_by_cuisine = filtered_df.groupby('country_code')['aggregate_rating'].mean().reset_index()
                df_filtered_by_cuisine = df_filtered_by_cuisine.sort_values(by='aggregate_rating', ascending=False)
            else:
                # Filter DataFrame by selected cuisine
                df_filtered_by_cuisine = filtered_df[filtered_df['cuisines'] == selected_cuisine]
                
                # Calculate average review score and cost for two per country for the selected cuisine
                df_filtered_by_cuisine = df_filtered_by_cuisine.groupby('country_code')[['aggregate_rating', 'average_cost_for_two']].mean().reset_index()

                # Sort by average score to find the highest and lowest
                df_filtered_by_cuisine = df_filtered_by_cuisine.sort_values(by='aggregate_rating', ascending=False)

            # Filter for top 5 or 10 countries based on selection
            options = ['Top5', 'Top10', 'All']
            st.session_state.filter_selection_cuisines_rating = st.radio(
                "Filter Options: ",
                options,
                key="cuisine_rating",
                index=options.index(st.session_state.get('filter_selection_cuisines_rating', 'All')) if 'filter_selection_cuisines_rating' in st.session_state else options.index('All')
            )

            if st.session_state.filter_selection_cuisines_rating == 'Top5':
                selected_rows1 = df_filtered_by_cuisine.dropna().head(5)
            elif st.session_state.filter_selection_cuisines_rating == 'Top10':
                selected_rows1 = df_filtered_by_cuisine.dropna().head(10)
            else:
                selected_rows1 = df_filtered_by_cuisine.dropna()


            # Display the final result
            st.table(selected_rows1.reset_index(drop=True))

    with col2:
        # Assuming plot_bar_view_streamlit is a function that takes the DataFrame and plots it
        # Note: Adjust the parameters according to your actual plotting function requirements
        fig3 = plot_bar_view_streamlit2(selected_rows1, 'country_code', 'aggregate_rating', 
                                       title=f'Highest Review Score for {selected_cuisine}', 
                                       figsize=(10, 6))
        #     fig1 = plot_bar_view_streamlit(selected_rows7,'country_code', cuisine_options, 
        #                                    title   = f'{st.session_state.filter_selection_cost} Average cost for two per Country', 
        #                                    figsize = (10, 6)
        #                                   )
#--\/--------------------------------------------------------------------------------------------------------------------------------------------------------