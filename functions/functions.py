# ===================================
#            Libs                  
# ==================================

import matplotlib.pyplot as plt
import inflection
import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO

def general_info(df):
    """
    Prints General Info details
    """
    total_text_ratings = df['rating_text'].notna().sum()
    unique_restaurants_name = df['restaurant_name'].unique()
    unique_restaurants_id = df['restaurant_id'].unique()
    unique_countries = df['country_code'].unique()
    total_ratings = df['votes'].notna().sum()
    unique_cousines = df['cuisines'].unique()
    unique_cities = df['city'].unique()
    
    line = "------------- --- ------------- --- ------------- --- ------------- --- -------------\n\n"
    
    # 1 How many unique restaurants are registered?
    st.write(f"Number of unique restaurants presented is {len(unique_restaurants_id)}")
    st.write(line)
    st.write(f"Number of unique franchises: {len(unique_restaurants_name)}, considering IDs with the same name as part of the same franchise regardless of location.")
    
    st.write(line)
    
    # 2 How many unique countries are registered?
    st.write(f"Number of unique countries presented on sheet is {len(unique_countries)}")
    st.write(line)
    
    # 3 How many unique cities are registered?
    st.write(f"Number of unique cities presented on sheet is {len(unique_cities)}")
    st.write(line)
    
    # 4 What is the total number of reviews made?
    st.write(f"Total of {total_ratings} numbered ratings and {total_text_ratings} text comments.")
    st.write(line)
    
    # 5 What is the total number of types of cuisine registered?
    st.write(f"Number of unique cuisines presented on sheet is {len(unique_cousines)}")
    st.write(line)

    return None


def plot_bar_view_streamlit(df_query, filter_column, filtered_column, title, figsize=(10, 6)):
    """
    Plots a barplot using matplotlib in the configurations set:

    Parameters:
            - df_query            : df filtered by a bool query
            - filter_column       : the main col which you are filtering for
            - filtered_column     : col which you desired to group to
            - figsize (optional)  : (10,8) ~ fits the container
            - title               : defines header of the barplot

    Returns:
            - bar graph 
    """

    list_filter_entries = df_query[filter_column].tolist()
    list_filtered_entries = df_query[filtered_column].tolist()

    # Define a sequence of colors that repeats every two entries
    alternating_colors = ['darkgrey', 'red', 'darkgrey', 'red']

    # Create the bar plot
    fig, ax = plt.subplots(figsize=figsize)  # Using subplots for better control over the figure
    bars = ax.bar(list_filter_entries, list_filtered_entries, color=alternating_colors)

    # Customize the plot
    ax.set_title(title)
    ax.set_xlabel(filter_column)
    ax.set_ylabel(filtered_column)

    # Rotate x-axis labels by 45 degrees and align them to the right
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')

    # Add a dashed green grid
    ax.grid(axis='y', linestyle='--', linewidth=0.8, color='green', alpha=0.7)

    # Set y-axis to logarithmic scale
    ax.set_yscale('log')
    
    # Add value labels above each bar
    for bar in bars:
        height = bar.get_height() + 0.04
        ax.text(bar.get_x() + bar.get_width() / 2,
                height + 0.02,
                f'{height:.0f}',
                fontsize=8,
                ha='center',
                va='bottom',
                color='black',
                bbox=dict(facecolor='white', edgecolor='black'))

    # Show the plot in Streamlit
    st.pyplot(fig)


def plot_bar_view_streamlit2(df_query, filter_column, filtered_column, title, figsize=(10, 6)):
    """
    Plots a barplot using matplotlib in the configurations set:

    Parameters:
            - df_query            : df filtered by a bool query
            - filter_column       : the main col which you are filtering for
            - filtered_column     : col which you desired to group to
            - figsize (optional)  : (10,8) ~ fits the container
            - title               : defines header of the barplot

    Returns:
            - bar graph 
    """

    list_filter_entries = df_query[filter_column].tolist()
    list_filtered_entries = df_query[filtered_column].tolist()

    # Define a sequence of colors that repeats every two entries
    alternating_colors = ['darkgrey', 'red', 'darkgrey', 'red']

    # Create the bar plot
    fig, ax = plt.subplots(figsize=figsize)  # Using subplots for better control over the figure
    bars = ax.bar(list_filter_entries, list_filtered_entries, color=alternating_colors)

    # Customize the plot
    ax.set_title(title)
    ax.set_xlabel(filter_column)
    ax.set_ylabel(filtered_column)

    # Rotate x-axis labels by 45 degrees and align them to the right
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')

    # Add a dashed green grid
    ax.grid(axis='y', linestyle='--', linewidth=0.8, color='green', alpha=0.7)

    # Show the plot in Streamlit
    st.pyplot(fig)

def aggregator(df_query, column_filter, column_filtered, agg_method='size', max=1, min=0):
    """
        Groups by unique entries in the desired column and applies the specified aggregation method.
    
        Parameters:
                - df_query: DataFrame filtered by a boolean query.
                - column_filter: Main column to filter for grouping.
                - column_filtered: Column to group by.
                - agg_method: Aggregation method to apply ('mean', 'size', or 'nunique'). Default is 'size'.
                - max: Optional; prints max value of query if 1.
                - min: Optional; prints min value of query if 1.
    
        Returns:
                - DataFrame with grouped counts.
                - .idxmax() if requested == 1
                - .idxmin() if requested == 1 
    """

    line = '----------  ---  ----------  ---  ----------  ---  ----------\n'
    # Validate the aggregation method
    valid_methods = ['mean', 'size', 'nunique']
    if agg_method not in valid_methods:
        raise ValueError(f"Unsupported aggregation method '{agg_method}'. Supported methods are 'mean', 'size', and 'nunique'.")
    
    # Group by 'column_filter' and apply the specified aggregation method
    df_aux = df_query.groupby(column_filter)[column_filtered].agg(agg_method).reset_index(name='count')
    
    # Find the entries with the highest and lowest counts
    df_highest_query = df_aux.loc[df_aux['count'].idxmax()]
    df_lowest_query  = df_aux.loc[df_aux['count'].idxmin()]

    
    # Adjust print statements based on the values of max and min
    if max == 1:
        if agg_method == 'mean':
            # Format mean value to 2 decimal places
            formatted_mean = "{:.2f}".format(df_highest_query['count'])
            print(f">   {df_highest_query[column_filter]} is the {column_filter} with the highest average ({formatted_mean})")
        else:
            print(f">   {df_highest_query[column_filter]} is the {column_filter} with most unique entries ({df_highest_query['count']})")
        print(line)
    if min == 1:
        if agg_method == 'mean':
            # Format mean value to 2 decimal places
            formatted_mean = "{:.2f}".format(df_lowest_query['count'])
            print(f">   {df_lowest_query[column_filter]} is the {column_filter} with the lowest average ({formatted_mean})")
        else:
            print(f">   {df_lowest_query[column_filter]} is the {column_filter} with lesser unique entries ({df_lowest_query['count']})")
        print(line)
        
    return df_aux
    
def rename_columns(df1):
    ###  Rename columns removing backspace for undescores  ### 
        # backup of the original code
    df         = df1.copy()
    title      = lambda x: inflection.titleize(x)
    snakecase  = lambda x: inflection.underscore(x)
    spaces     = lambda x: x.replace(" ", "")
    cols_old   = list(df.columns)
    cols_old   = list(map(title, cols_old))
    cols_old   = list(map(spaces, cols_old))
    cols_new   = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


def tag_fixer(df):
    ### Replace the code for the country name ###
    COUNTRIES = {
        1  : "India",
        14 : "Australia",
        30 : "Brazil",
        37 : "Canada",
        94 : "Indonesia",
        148: "New Zealand",  
        162: "Philippines",
        166: "Qatar",
        184: "Singapore",  #
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "Arab Emirates",
        215: "England",
        216: "USA",
    }
    
    ### Translating color codes for establishment score ###
    COLORS = {
    "3F7E00":  "darkgreen",
    "5BA829":      "green",
    "9ACD32": "lightgreen",
    "CDD614":     "orange",
    "FFBA00":        "red",
    "CBCBC8":    "darkred",
    "FF7800":    "darkred",
    }

    ### Translate and standardize Rating comments in text ### 
    RATING_TRANSLATION = {
    "Very Good"     : "Good",
    "Excellent"     : "Excellent",
    "Good"          : "Good",
    "Average"       : "Average",
    "Not rated"     : np.nan,
    "Excelente"     : "Excellent",  
    "Velmi dobré"   : "Good",
    "Veľmi dobré"   : "Good",
    "Poor"          : "Poor",
    "Çok iyi"       : "Good",
    "Biasa"         : "Average",  
    "Bardzo dobrze" : "Good",
    "Sangat Baik"   : "Good",
    "Muy Bueno"     : "Good",
    "Baik"          : "Good",
    "Muito Bom"     : "Good",
    "Skvělá volba"  : "Excellent",
    "Harika"        : "Excellent",
    "Muito bom"     : "Good",
    "Skvělé"        : "Excellent",
    "Terbaik"       : "Excellent",
    "İyi"           : "Good",
    "Vynikajúce"    : "Excellent",
    "Bueno"         : "Good",
    "Bom"           : "Good",
    "Buono"         : "Good",
    "Wybitnie"      : "Excellent",
    "Eccellente"    : "Excellent",
    "Best"          : "Excellent"
    }

    # Converting cost for two to USD, values could be implemented with an API
    TO_DOLLAR = {
    'Dollar($)'             : 1.0,  
    'Real(R$)'              : 0.25, 
    'Pounds(£)'             : 1.36,  
    'Rupees(Rs.)'           : 0.013,  
    'Indonesian Rupiah(IDR)': 0.000063,  
    'Pula(P)'               : 0.18,  
    'Qatari Rial(QR)'       : 0.27,  
    'Rand(R)'               : 0.083,  
    'Sri Lankan Rupee(LKR)' : 0.0033,  
    'Turkish Lira(TL)'      : 0.030,  
    'Emirati Dirham(AED)'   : 0.27  
}
    
    ### Transforming scores from numbers to string for categorical manipulation  ###
    PRICE = {
        1: "Cheap",
        2: "Normal",
        3: "Expensive",
        4: "Gourmet"
    }

    # Replace the outlier at index 385 with 250
    outlier_index = 385
    df.at[outlier_index, 'average_cost_for_two'] = 250 # it was affecting the metrics, fixing to 2nd max value 250
    
    #Converting cost for two to USD 
    df["average_cost_for_two"] = (df['average_cost_for_two'] * df["currency"].map(TO_DOLLAR).fillna(0)).round(2)
    
    # Extracts only the first element prior to a coma in each df['cuisine'] cell
    df["cuisines"] = df["cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    df = df.replace({'cuisines': {'nan': np.nan}})

    # Mapping all previous dictionaries to replace columns with desired values
        # Country name per code
    df['country_code'] = df['country_code'].map(COUNTRIES).fillna(df['country_code'])
    
        # Color name per code
    df['rating_color'] = df['rating_color'].map(COLORS).fillna(df['rating_color'])
    
        # Standardize and translate rating comments 
    df['rating_text']  = df['rating_text'].map(RATING_TRANSLATION).where(df['rating_text'].isin(RATING_TRANSLATION.keys()), df['rating_text'])
    
        # Adjusting price range names
    df['price_range']  = df['price_range'].map(PRICE).fillna(df['price_range'])
   
        # Conversions
    to_category = [
        'locality_verbose'   ,
        'country_code'       ,
        'rating_color'       ,
        'price_range'        ,
        'rating_text'        ,
        'currency'           ,
        'locality'           ,
        'cuisines'           ,
        'city' 
    ]

    to_bool = [
        'has_online_delivery',
        'is_delivering_now'  ,
        'has_table_booking'  
    ]
    
    for col in to_category:
        df[col] = df[col].astype('category')
        
    for col in to_bool:
        df[col] = df[col].astype('bool')
        
    return df

def read_df ():
    df1 = pd.read_csv('datasets/zomato.csv')
    df = rename_columns(df1)
    df = tag_fixer(df)
    df = df.drop_duplicates(keep=False)
    return df, df1