#!/usr/bin/python3

import requests
import threading
import time
import sys
import chat_commands
from gtts import gTTS
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from flask import Flask, request, render_template
from PIL import Image, ImageTk
import speech_recognition as sr
import pygame
import speech_recognition as sr
import webbrowser
import re
import subprocess
import json
import bard
import bardapi



class BardChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://bard.ai/api/v1"

    def generate_response(self, prompt):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(
            f"{self.base_url}/query", headers=headers, json={"prompt": prompt}
        )
        return response.json()["response"]
response = bard.generate("What can I do for you today?")
# Initialize Bard Chatbot with your API key
chatbot = BardChatbot("AIzaSyCWA5Gnp2SRJgTjVcqmgkkUB-II3N6QP1w")

# Read the JSON file
with open("bard_json.json", "r") as f:
    json_data = json.load(f)

# Generate a response from Bard
response = bard.generate(json_data)

# Print the response
print(response)


doListenToCommand = True
listening = False

# List with common departures to end the while loop
despedida = ["Goodbye", "goodbye", "bye", "Bye", "See you later", "see you later"]

# Create the GUI window
window = tk.Tk()
window.title("Computer:AI")
window.geometry("400x400")

# Create the text entry box
text_entry = tk.Entry(window, width=50)
text_entry.pack(side=tk.BOTTOM)

# Create the submit button
submit_button = tk.Button(window, text="Submit", command=lambda: submit())
submit_button.pack(side=tk.BOTTOM)

# Create the text output box
text_output = tk.Text(window, height=300, width=300)
text_output.pack(side=tk.BOTTOM)

def submit(event=None, text_input=None):
    global doListenToCommand
    global listening

    # Get the user input and check if the input matches the list of goodbyes
    if text_input != "":
        usuario = text_input
    else:
        usuario = text_entry.get()

    if usuario in despedida:
        on_closing()
    else:
        # Generate a response using Bard Chatbot
        respuesta = chatbot.generate_response(usuario)

        # Converting text to audio
        texto = str(respuesta)
        tts = gTTS(texto, lang='en', tld='ie')
        tts.save("audio.mp3")

        # Displaying the answer on the screen
        text_output.insert(tk.END, "Bard: " + respuesta + "\n")

        # Clear the input text
        text_entry.delete(0, tk.END)

        # Playing the audio
        doListenToCommand = False
        time.sleep(1)
        os.system("play audio.mp3")
        doListenToCommand = True

        # Call function to listen to the user
        if listening == False:
            listen_to_command()

# Bind the Enter key to the submit function
window.bind("<Return>", submit)

# Flask app
app = Flask(__name__, template_folder='templates')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        file.save(file.filename)
        chatbot.api_key = request.form["apikey"]
        return "Model file and API key saved."
    return render_template("index.html")

def run_as_normal_app():
    window.update()

def run_on_flask():
    app.run()

def listen_to_command():
    global doListenToCommand
    global listening

    # If we are not to be listening, then exit the function.
    if doListenToCommand == True:
        # Initialize the recognizer
        r = sr.Recognizer()

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Listening...")
            listening = True
            audio = r.listen(source)
            listening = False

        try:
            # Use speech recognition to convert speech to text
            command = r.recognize_google(audio)
            print("You said:", command)
            text_output.insert(tk.END, "You: " + command + "\n")
            text_entry.delete(0, tk.END)

            # Process the commands
            # Prepare object to be passed.
            class passed_commands:
                tk = tk
                text_output = text_output
                submit = submit

            chat_commands.process_commands(passed_commands, command)

        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service:", str(e))

        listen_to_command()
        listening = False

def on_closing():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main program loop
if __name__ == "__main__":
    # Create the menu bar
    menu_bar = tk.Menu(window)

    # Create the "File" menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open LLM", command=lambda: filedialog.askopenfilename())
    file_menu.add_command(label="Save LLM", command=lambda: filedialog.asksaveasfilename())
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=on_closing)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Create the "Run" menu
    run_menu = tk.Menu(menu_bar, tearoff=0)
    run_menu.add_command(label="Run as normal app", command=run_as_normal_app)
    run_menu.add_command(label="Run on Flask", command=run_on_flask)
    menu_bar.add_cascade(label="Run", menu=run_menu)

    # Set the menu bar
    window.config(menu=menu_bar)

    # Start the main program loop
    start_listening_thread = threading.Thread(target=listen_to_command)
    start_listening_thread.daemon = True
    start_listening_thread.start()
    window.mainloop()
