import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import time
import subprocess
import psutil  # For system usage
import platform  # For system information
import ctypes  # For locking the computer

# Initialize the TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

time.sleep(5)

# Function to make the assistant speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to wish the user based on the time of day
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Votta, your personal assistant. How may I assist you today?")

# Function to listen for voice commands
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, could you please say that again?")
        return "None"
    return query

# Function to play random music from the user's Music directory
def playMusic():
    music_dir = os.path.join(os.path.expanduser("~"), "Music")
    songs = os.listdir(music_dir)
    if songs:
        song = random.choice(songs)
        print(f"Playing: {song}")
        os.startfile(os.path.join(music_dir, song))
    else:
        speak("No music files found in your music directory")

# Function to open frequently used applications
def openApp(app_name):
    paths = {
        "notepad": r"C:\Windows\System32\notepad.exe",
        "calculator": r"C:\Windows\System32\calc.exe",
        "command prompt": r"C:\Windows\System32\cmd.exe"
    }
    if app_name in paths:
        subprocess.Popen(paths[app_name])
        speak(f"Opening {app_name}")
    else:
        speak(f"Sorry, I don't know how to open {app_name}")

# Function to check and speak the current time
def tellTime():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")

# Function to lock the computer
def lockSystem():
    speak("Locking the system")
    ctypes.windll.user32.LockWorkStation()

# Function to shutdown the computer
def shutdownSystem():
    speak("Shutting down the system")
    os.system("shutdown /s /t 5")

# Function to restart the computer
def restartSystem():
    speak("Restarting the system")
    os.system("shutdown /r /t 5")

# Function to check system health
def systemHealth():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    battery_info = psutil.sensors_battery()

    speak(f"CPU usage is at {cpu_usage} percent")
    speak(f"Memory usage is at {memory_info.percent} percent")
    if battery_info:
        speak(f"Battery is at {battery_info.percent} percent and it is {'charging' if battery_info.power_plugged else 'not charging'}")
    else:
        speak("Battery information not available")

# Function to display system info
def systemInfo():
    uname = platform.uname()
    speak(f"System: {uname.system}")
    speak(f"Node Name: {uname.node}")
    speak(f"Release: {uname.release}")
    speak(f"Version: {uname.version}")
    speak(f"Machine: {uname.machine}")
    speak(f"Processor: {uname.processor}")

# Main function to handle user commands
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Search Wikipedia
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        # Open popular websites
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")

        elif 'open instagram' in query:
            speak("Opening Instagram")
            webbrowser.open("instagram.com")

        # Play music
        elif 'play music' in query:
            speak("Playing music")
            playMusic()

        # Tell the current time
        elif 'the time' in query:
            tellTime()

        # Lock system
        elif 'lock system' in query:
            lockSystem()

        # Shutdown system
        elif 'shutdown system' in query:
            shutdownSystem()

        # Restart system
        elif 'restart system' in query:
            restartSystem()

        # Check system health (CPU, Memory, Battery)
        elif 'system health' in query:
            systemHealth()

        # Get system information
        elif 'system info' in query:
            systemInfo()

        # Open common applications
        elif 'open notepad' in query:
            openApp("notepad")

        elif 'open calculator' in query:
            openApp("calculator")

        elif 'open command prompt' in query:
            openApp("command prompt")

        # Exit the assistant
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye, have a great day!")
            break

        # Handle unknown commands
        else:
            speak("I'm sorry, I didn't understand that. Could you please repeat?")
