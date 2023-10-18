import os
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
    page_title="Data Driven Characters",
    page_icon="👋",
)


persona_pages = []
persona_names = []


for filename in sorted(os.listdir("pages")):
    persona_name = filename.replace(".py", "").replace("_", " ")
    persona_pages.append(
        Page(f"pages/{filename}", persona_name))
    persona_names.append(persona_name)


show_pages([
    Page("main.py", "Home"),
    *persona_pages
])

st.text_input("OpenAI API Key", type="password", key="openai_api_key")
st.text_input("Your Name", value="Anon", key="user_name")


if not st.session_state.openai_api_key:
    hide_pages(persona_names)

st.write("# Data Driven Characters")

if st.session_state.openai_api_key:
    st.sidebar.success("Select a character above")
else:
    st.sidebar.warning("Enter your OpenAI API key to see the character list")


st.markdown(
    """
    huzzah
    """
)
