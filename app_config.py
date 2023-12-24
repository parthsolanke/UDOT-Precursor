import streamlit as st
from PIL import Image

img = Image.open(r"./static/logo.png")
def StreamlitConfig():
    st.set_page_config(page_title="U.D.O.T", layout="wide", page_icon=img)
    hide_default_format = """
           <style>
           #MainMenu {visibility: hidden; }
           footer {visibility: hidden;}
           </style>
           """
    st.markdown(hide_default_format, unsafe_allow_html=True)