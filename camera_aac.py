import cv2
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import pyttsx3
import time

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # speech speed

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Labels and phrases
labels = ["water", "hungry", "help"]
phrases = {
    "water": "I want water please.",
    "hungry": "I am hungry.",
    "help": "I need help."
}

# Open webcam
cap = cv2.VideoCapture(0)
print("Press 'q' to quit.")

last_label = None
last_spoken_time = 0
cooldown = 3  # seconds between repeats

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show camera feed
    cv2.imshow("AAC Camera", frame)

    # Every 30 frames, do prediction
    if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % 30 == 0:
        # Convert frame to PIL
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Run CLIP
        inputs = processor(text=labels, images=image, return_tensors="pt", padding=True).to(device)
        outputs = model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
        best_idx = probs.argmax().item()
        best_label = labels[best_idx]
        phrase = phrases[best_label]

        print(f"Prediction: {best_label} → {phrase}")

        # Speak if new label OR cooldown passed
        now = time.time()
        if best_label != last_label or (now - last_spoken_time) > cooldown:
            engine.stop()   # clear old queue
            engine.say(phrase)
            engine.runAndWait()
            last_label = best_label
            last_spoken_time = now

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
