import streamlit as st

from pathlib import Path
from streamlit.source_util import (
    page_icon_and_name, 
    calc_md5, 
    get_pages,
    _on_pages_changed
)

from st_pages import show_pages, Page, hide_pages

st.set_page_config(
    page_title="Data Driven and Personality Driven Characters",
    page_icon="👋",
)

if "debug_info" not in st.session_state:
    st.session_state.debug_info = ""

persona_pages = [
        Page("pages/Homer_Simpson.py", "Homer Simpson"),
        Page("pages/Patrick_Bateman.py", "Patrick Bateman"),
        Page("pages/Dwight_Schrute.py", "Dwight Schrute"),
        # Page("pages/Raymond_Reddington.py", "Raymond Reddington"),
        # Page("pages/Confucius.py", "Confucius"),
    ]

show_pages([
  Page("main.py", "Home"),
  *persona_pages
])

st.text_input("OpenAI API Key", type="password", key="openai_api_key")
st.text_input("Your Name", value="Anon", key="user_name")


if not st.session_state.openai_api_key:
    hide_pages(["Homer Simpson", "Patrick Bateman", "Dwight Schrute"])

st.write("# Personality and Data Driven Characters")

st.sidebar.success("Select a character above")


st.markdown(
    """
    huzzah
    """
)