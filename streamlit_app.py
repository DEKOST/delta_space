import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Space Shooter",
    page_icon="🚀",
    layout="wide"
)

# Inject custom CSS to remove padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 0;
            padding-bottom: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Open and read the HTML file
with open("templates/index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Display the game in fullscreen mode
html(html_content, width=600, height=1100, scrolling=False)
