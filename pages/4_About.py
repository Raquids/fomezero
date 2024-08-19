import streamlit as st
from PIL import Image
from functions import general_info as info
from functions import read_df

# Set the page configuration
st.set_page_config(
    page_title='About',
    page_icon="❓",
    layout='wide'
)

# Load data
df, df1 = read_df()

# Open images
image = Image.open('assets/icon.png')
logo = Image.open('assets/logo.png')


# Sidebar container
with st.sidebar.container():
    st.sidebar.image(image, use_column_width=True)

# Main content container
with st.container():
    # Description of the project
    st.markdown('# About the project: ')
    st.write("""
    This is the Final Student Project for the FTC module in the 'Comunidade DS'. This study has no financial purpose and was developed by Raqui, at ([RaquiDS](https://github.com/Raquids)).
    """)

    # Using st.expander to display variable descriptions
    with st.expander('Variable description'):
    # Assuming info(df) returns a markdown-formatted string
        st.markdown(info(df))

    st.markdown('---')
    st.markdown('Powered by Comunidade DS')