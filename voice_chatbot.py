import os
import torch
import speech_recognition as sr
import openai
import pyttsx3
from tortoise.api import TextToSpeech

# Set your OpenAI API key
openai.api_key = "your-openai-key"

# Initialize Tortoise TTS
tortoise_tts = TextToSpeech()

# Microphone setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Toggle between fast fallback and slow HQ voice
USE_FAST_TTS = True

# Fast fallback voice using pyttsx3
def speak_fast(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# High-quality voice using Tortoise with your "alle" folder
def speak_slow_tortoise(text):
    output_path = "output.wav"
    tortoise_tts.tts_to_file(text=text, voice_dir="voices/alle", file_path=output_path)
    # Play the audio (cross-platform)
    if os.name == 'nt':  # Windows
        os.system(f"start {output_path}")
    else:  # Linux/macOS
        os.system(f"aplay {output_path}")

# Speak function (decides which TTS to use)
def speak(text):
    if USE_FAST_TTS:
        speak_fast(text)
    else:
        speak_slow_tortoise(text)

# Query GPT
def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message["content"].strip()

# Voice chatbot loop
def run_chatbot():
    print("Say something...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")

        response = ask_gpt(query)
        print(f"GPT: {response}")

        speak(response)

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
    except Exception as e:
        print(f"Error: {e}")

# Run chatbot
if __name__ == "__main__":
    while True:
        run_chatbot()
