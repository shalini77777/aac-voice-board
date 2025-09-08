import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Phrases
PHRASES = {
    "water": "I want water please.",
    "hungry": "I am hungry.",
    "help": "I need help."
}

# Speak function
def speak(concept):
    text = PHRASES[concept]
    engine.say(text)
    engine.runAndWait()

# GUI setup
root = tk.Tk()
root.title("AAC Voice Board")
root.geometry("600x400")
root.configure(bg="white")

# Helper to make buttons with images
def create_button(concept, img_file, row, col):
    img = Image.open(img_file).resize((150, 150))
    photo = ImageTk.PhotoImage(img)
    btn = tk.Button(root, text=PHRASES[concept],
                    image=photo, compound="top",
                    font=("Arial", 16), bg="lightblue",
                    command=lambda: speak(concept))
    btn.image = photo  # keep a reference
    btn.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

# Create AAC buttons
create_button("water", "water.png", 0, 0)
create_button("hungry", "food.png", 0, 1)
create_button("help", "help.png", 1, 0)

# Make grid flexible
for i in range(2):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
