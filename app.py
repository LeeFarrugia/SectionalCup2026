import streamlit as st
import pandas as pd
import datetime
import os

# Constants
SECTIONS = ["Cubs", "Troop", "Ventures", "Rovers"]
SECTION_ICONS = {
  "Cubs": "https://shop.scouts.mt/wp-content/uploads/Cubs_logo.png.webp",
  "Troop": "https://www.sliemascouts.net/wp-content/uploads/2018/07/scouts2-1.png",
  "Ventures": "https://shop.scouts.mt/wp-content/uploads/Ventures_logo.png.webp",
  "Rovers": "https://shop.scouts.mt/wp-content/uploads/Rovers_logo.png.webp",
}

st.set_page_config(page_title="Sectional Cup 2026", layout="centered")

# Load query parameter for QR ID
qr_id = st.query_params.get("qr_id", "qr1")

# Header
st.image("https://www.sliemascouts.net/wp-content/uploads/2018/07/logo3-1.png", width=200)
st.title("Sectional Cup 2026")
st.markdown("### Choose Your Section")

# Section Selection UI
selected_section = st.session_state.get("selected_section")

if not selected_section:
  for section in SECTIONS:
    if st.button(f"\n<img src='{SECTION_ICONS[section]}' width='40px' style='vertical-align:middle;'> - {section}\n", key=section, help=section):
      st.session_state["selected_section"] = section
      selected_section = section

# Load challenge from CSV if section is selected
if selected_section:
  st.markdown(f"## {selected_section} Challenge for QR Code: {qr_id.upper()}")
  
  try:
    df = pd.read_csv("challenges.csv")
    challenge_row = df[(df['qr_id'] == qr_id) & (df['section'] == selected_section)]
    if not challenge_row.empty:
      st.write(challenge_row.iloc[0]['challenge'])
    else:
      st.warning("No challenge found for this section at this QR code.")
  except FileNotFoundError:
    st.error("Challenges file not found. Please upload challenges.csv.")

  # Upload section
  st.markdown("### Upload Your Evidence")
  uploaded_files = st.file_uploader("Upload images or videos", accept_multiple_files=True)
  notes = st.text_area("Optional Notes")

  if st.button("Submit Challenge"):
    st.success("Your submission has been logged. Thank you!")
    # Add integration with Google Sheets + Drive here

# Footer
st.markdown("""
<hr style='border:1px solid #ccc'>
<div style='text-align: center;'>Powered by Sliema Scout Group</div>
""", unsafe_allow_html=True)
