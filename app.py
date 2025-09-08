import streamlit as st
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import pyttsx3

# Load TTS
engine = pyttsx3.init()

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Labels
labels = ["water", "hungry", "help"]
phrases = {
    "water": "I want water please.",
    "hungry": "I am hungry.",
    "help": "I need help."
}

st.title("📷 AI Voice Board (AAC)")
st.write("Upload an image and the AI will say the phrase")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Run model
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True).to(device)
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)
    best_idx = probs.argmax().item()
    best_label = labels[best_idx]
    phrase = phrases[best_label]

    st.success(f"Prediction: {best_label} → {phrase}")

    # Speak
    engine.say(phrase)
    engine.runAndWait()
