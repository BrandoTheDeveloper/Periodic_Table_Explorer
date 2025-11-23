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


def render_element_card(element):
    st.html(
        f"""
        <div style="
            background-color:#f8f9fa;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            ">
            <h3 style="margin-top: 0; font-weight: bold;">{element.get("name", "Unknown")}</h3>

            <p><strong>Atomic Number:</strong> {element.get("atomic_number", "N/A")}</p>
            <p><strong>Element Symbol:</strong> {element.get("symbol", "N/A")}</p>
            <p><strong>State:</strong> {element.get("type", "N/A")}</p>
            <p><strong># of Protons:</strong> {element.get("protons", "N/A")}</p>
            <p><strong># of Electrons:</strong> {element.get("electrons", "N/A")}</p>

            <p><strong>Description:</strong><br>{element.get("summary", "No description available.")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


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
            for el in result:
                render_element_card(el)
    elif isinstance(result, dict):
        render_element_card(result)
    else:
        st.write(result)
