import streamlit as st
import json
import pandas as pd
import math
from pathlib import Path

# Load elements JSON relative to this script for robustness
data_path = Path(__file__).parent / "PeriodicTableJSON.json"
with open(data_path, "r") as file:
    data = json.load(file)

# Your JSON has the structure {"elements": [...]}
elements = data["elements"]


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Periodic Table Explorer',
    # This is an emoji shortcode. Could be a URL too.
    page_icon='⚛️',
)

# Functions


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


def search_by_state(state):
    return [el for el in elements if el["type"].lower() == state.lower()]


def search_by_particle_count(particle_type, count):
    if particle_type not in ["electrons", "protons"]:
        return "Invalid particle type."
    return [el for el in elements if el[particle_type] == count]


st.title("Welcome to the Periodic Table Explorer!")

# Small welcome input
username = st.text_input("Enter your name:")
if username:
    st.write(f"Welcome, {username}!")

# Search method selection
option = st.radio("Choose a search method", [
    "By Name",
    "By Atomic Number",
    "By State",
    "By Particle Count",
])

result = None

if option == "By Name":
    name = st.text_input("Element name", key="name_input")
    if st.button("Search by name", key="search_name"):
        if not name or not name.strip():
            st.warning("Please enter an element name.")
        else:
            result = search_by_name(name.strip())

if option == "By Atomic Number":
    # Use a numeric input for atomic number to ensure correct type
    number = st.number_input("Atomic Number", min_value=1,
                             max_value=118, value=1, step=1, key="atomic_input")
    if st.button("Search by atomic number", key="search_atomic"):
        result = search_by_atomic_number(int(number))

if option == "By State":
    # Build a sorted list of available states/types
    types = sorted({el.get("type", "Unknown") for el in elements})
    state = st.selectbox("State / Type", options=types, key="state_input")
    if st.button("Search by state", key="search_state"):
        result = search_by_state(state)

if option == "By Particle Count":
    particle_type = st.selectbox(
        "Particle type", ["electrons", "protons"], key="particle_type")
    count = st.number_input("Count", min_value=0, value=1,
                            step=1, key="particle_count")
    if st.button("Search by particle count", key="search_particle"):
        result = search_by_particle_count(particle_type, int(count))

# Present results consistently
if result is not None:
    if isinstance(result, list):
        if len(result) == 0:
            st.info("No elements found.")
        else:
            # Show as dataframe for readability
            st.write(pd.DataFrame(result))
    elif isinstance(result, dict):
        st.json(result)
    else:
        st.write(result)
