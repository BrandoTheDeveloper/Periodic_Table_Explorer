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
        if element["name"].lower() == name.lower() or element["symbol"].lower() == name.lower():
            return element
    return "Element not found."


def search_by_atomic_number(number):
    for element in elements:
        if "number" in element and element.get("number") == number:
            return element
    return "Element not found. Please try again."


def search_by_state(state):
    return [el for el in elements if el["phase"].lower() == state.lower()]


def search_by_particle_count(particle_type, count):
    # Ensure the particle type is valid
    if particle_type not in ["protons", "electrons"]:
        return "Invalid particle type."

    # Since in your JSON, protons and electrons = atomic number
    matches = [el for el in elements if "number" in el and el["number"] == count]

    if not matches:
        return "No elements found."
    return matches


def show_markdown(el):
    st.markdown(f"""
                


**Element Name:** {el.get("name")}  

**Symbol:** {el.get("symbol")}  

**Atomic Number:** {el.get("number")}  

**State:** {el.get("phase")}  

**Protons:** {el.get("number")}  

**Electrons:** {el.get("number")}

**Appearance:** {el.get("appearance")}  

**Description:**  
{el.get("summary")}
""")


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
        if not name.isalpha():
            st.warning(
                "Please enter only letters for the element name or symbol.")
        else:
            result = search_by_name(name.strip())


if option == "By Atomic Number":
    # Use a numeric input for atomic number to ensure correct type
    number = st.number_input("Atomic Number", min_value=1,
                             max_value=118, value=1, step=1, key="atomic_input")
    if st.button("Search by atomic number", key="search_atomic"):
        result = search_by_atomic_number(int(number))


if option == "By State":
    # Build a sorted list of unique phases from your JSON
    phases = sorted({el.get("phase", "Unknown") for el in elements})

    state = st.selectbox("State / Phase", options=phases, key="state_input")

    if st.button("Search by state", key="search_state"):
        result = search_by_state(state)


if option == "By Particle Count":
    particle_type = st.radio("Choose a particle type", [
        "Protons",
        "Electrons",
    ])
    particle_count = st.number_input(f"{particle_type} Number", min_value=1,
                                     max_value=118, value=1, step=1, key="particle_input")

    if st.button("Search by particle count", key="search_particle"):
        result = search_by_particle_count(
            particle_type.lower(), int(particle_count))

    # Present results consistently


if result is not None:
    if isinstance(result, dict):
        show_markdown(result)

    elif isinstance(result, list):
        if len(result) == 0:
            st.info("No elements found.")
        else:
            for el in result:
                show_markdown(el)

    else:
        st.write(result)
