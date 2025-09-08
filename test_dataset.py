import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import glob
import pyttsx3

# Initialize TTS
engine = pyttsx3.init()

# Load CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Define labels and phrases
labels = ["water", "hungry", "help"]
phrases = {
    "water": "I want water please.",
    "hungry": "I am hungry.",
    "help": "I need help."
}

print("Starting test on dataset...")

# Loop through images
for label in labels:
    print(f"\nTesting images in category: {label}")
    for img_path in glob.glob(f"dataset/{label}/*"):
        image = Image.open(img_path).convert("RGB")
        inputs = processor(text=labels, images=image, return_tensors="pt", padding=True).to(device)
        outputs = model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
        best_idx = probs.argmax().item()
        best_label = labels[best_idx]
        phrase = phrases[best_label]

        print(f"Image: {img_path} → Predicted: {best_label} → Speaking: {phrase}")
        engine.say(phrase)
        engine.runAndWait()
