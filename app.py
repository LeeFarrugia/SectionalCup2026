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

# Load query parameters
query_params = st.experimental_get_query_params()
qr_id = query_params.get("qr_id", ["qr1"])[0]
if "selected" in query_params:
  st.session_state["selected_section"] = query_params["selected"][0]

# Header
st.image("https://scontent-fra5-1.xx.fbcdn.net/v/t39.30808-6/326566525_2386990981461745_2123444378451707595_n.png?_nc_cat=102&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=kiCSbvmQTIwQ7kNvwFte-mX&_nc_oc=Adn9DlDwX9zd2aQVVnwV2IxhX7zQydPdYWjsYlzNiltR_I59P-Q25ErVhUAlGKA1MXs&_nc_zt=23&_nc_ht=scontent-fra5-1.xx&_nc_gid=y64pWyqNmRZt77mSH5bhMQ&oh=00_AfSBRL3zKteTkCRSFvn5ZKBtPyI_8LtV9YF_YE4WzCRYGw&oe=688E6107", width=200)
st.title("Sectional Cup 2026")

# Section Selection UI
selected_section = st.session_state.get("selected_section")

def section_button(icon_url, label):
  btn_html = f"""
  <a href="?qr_id={qr_id}&selected={label}" style="
    display: block;
    background-color: #0080c9;
    color: white;
    padding: 12px;
    margin: 10px 0;
    border-radius: 12px;
    text-align: center;
    text-decoration: none;
    font-size: 20px;
  ">
    <img src="{icon_url}" width="30" style="vertical-align: middle; margin-right: 10px;">
    {label}
  </a>
  """
  st.markdown(btn_html, unsafe_allow_html=True)

if not selected_section:
  st.markdown("### Choose Your Section")
  for section in SECTIONS:
    section_button(SECTION_ICONS[section], section)

# Show challenge if selected
selected_section = st.session_state.get("selected_section")
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

  st.markdown("### Upload Your Evidence")
  uploaded_files = st.file_uploader("Upload images or videos", accept_multiple_files=True)
  notes = st.text_area("Optional Notes")

  if st.button("Submit Challenge"):
    st.success("Your submission has been logged. Thank you!")
    # Add Google Sheets + Drive integration here

# Footer
st.markdown("""
<hr style='border:1px solid #ccc'>
<div style='text-align: center;'>Powered by Sliema Scout Group</div>
""", unsafe_allow_html=True)
