import streamlit as st
import pyttsx3
import os
from PIL import Image

# Get absolute path for icons folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, "icons")

# Add as many as you like here:
phrases = {
    "water": "I want water please.",
    "hungry": "I am hungry.",
    "help": "I need help.",
    "toilet": "I want to go to the toilet.",
    "sleep": "I am feeling sleepy.",
    "pain": "I am in pain.",
    "play": "I want to play.",
    "thankyou": "Thank you so much."
}

# Streamlit app UI
st.set_page_config(page_title="AAC Voice Board", layout="wide")
st.title("🗣️ AI Voice Board (AAC Device Alternative)")
st.write("Click on a picture to speak the phrase.")

# Desired uniform size
IMAGE_SIZE = (200, 200)

# Display in grid (3 per row)
cols = st.columns(3)
col_index = 0

for label, phrase in phrases.items():
    with cols[col_index]:
        image_path = os.path.join(ICON_DIR, f"{label}.png")

        if os.path.exists(image_path):
            img = Image.open(image_path).resize(IMAGE_SIZE)

            # Button below image
            st.image(img, caption=label.capitalize(), use_container_width=False)

            if st.button(f"Speak {label.capitalize()}", key=label):
                st.success(phrase)

                # Initialize TTS engine inside button
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.say(phrase)
                engine.runAndWait()

        else:
            st.warning(f"Missing: {label}.png")

    # Move to next column, reset after 3
    col_index += 1
    if col_index == 3:
        col_index = 0
        cols = st.columns(3)
