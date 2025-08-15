import speech_recognition as sr
import pyttsx3
import pyaudio
import webbrowser

from humanfriendly.terminal import output

import musiclibrary
import requests
from client import ask_deepseek
newsapi = '8972f3551f7d4a76a7c94d67f3079996'

r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processcommand(command):
    if 'open google' in command.lower():
        webbrowser.open('https://www.google.com')
    elif 'open facebook' in command.lower():
        webbrowser.open('https://www.facebook.com')
    elif 'open linkdin' in command.lower():
        webbrowser.open('https://www.linkedin.com')
    elif 'open youtube' in command.lower():
        webbrowser.open('https://www.youtube.com')
    elif command.lower().startswith('play'):
        song = command.lower().split(' ')[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif 'news' in command.lower():
        response = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=8972f3551f7d4a76a7c94d67f3079996')
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            # Fetch articles list
            articles = data['articles']

            # Print all headlines
            print("Top Headlines:")
            for i, article in enumerate(articles):
                print(f"{i + 1}. {article['title']}")
        else:
            print("Failed to fetch news:", response.status_code)

    else:
        dsres = ask_deepseek(command)
        speak(dsres)


while True:
    with sr.Microphone() as source:
        print('Listening for Wake Word...')
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
            word = r.recognize_google(audio)

            if word.lower() == 'jarvis':
                speak('Yes?')
                print('Jarvis Active...')

                # Now listen for the next command
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)

                    processcommand(command)
                except sr.UnknownValueError:
                    speak('Sorry, I did not catch that.')
        except sr.WaitTimeoutError:
            print("Listening timed out, no wake word detected.")
        except sr.UnknownValueError:
            print("Could not understand audio, waiting again.")
