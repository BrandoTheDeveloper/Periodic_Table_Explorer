import streamlit as st
import json
import pandas as pd
import math
from pathlib import Path

with open("PeriodicTableJSON.json", "r") as file:
    elements = json.load(file)

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Periodic Table Explorer',
    # This is an emoji shortcode. Could be a URL too.
    page_icon='⚛️',
)


def search_by_name(name):
    for element in elements:
        if element["name"].lower() == name.lower():
            return element
    return "Element not found."


def search_by_atomic_number(number):
    for element in elements:
        if element["atomic_number"] == number:
            return element
    return "Element not found."


st.title("Welcome to the Periodic Table Explorer!")
username = st.text_input("Enter your name: ")
print(f"Welcome {username}!")
option = st.radio("Choose a search method", [
                  "By Name", "By Atomic Number", " By State"])
if option == "By Name":
    name = st.text_input("Element name")
    if st.button("Search"):
        result = search_by_name(name)
        st.write(result)
if option == "By Atomic Number":
    number = st.text_input("Atomic Number")
    if st.button("Search"):
        result = search_by_atomic_number(number)
        st.write(result)
