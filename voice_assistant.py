import pywhatkit
import speech_recognition as sr
import pyttsx3
import datetime
import requests
import wikipedia
from bs4 import BeautifulSoup
import webbrowser
import subprocess
import pyautogui
import os
import random
import time
import sys
import openai
from pyautogui import click
from keyboard import press
from keyboard import write
from time import sleep
import threading

chatStr = ''
api_key = "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"
openai.api_key = api_key
listener = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty('rate', 150)

def recognize_intent(user_input):
    if "play music" in user_input:
        return "play_music"
    elif "search the web" in user_input:
        return "search_web"
    elif "tell me a joke" in user_input:
        return "tell_joke"
    else:
        return "unknown"

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            listener.pause_threshold = 1
            listener.adjust_for_ambient_noise(source, 1)
            voice = listener.listen(source, 0, 7)
            command = listener.recognize_google(voice, language='en-bn')
            command = command.lower()
            command = command.replace('jarvis', '')
        return command
    except Exception as e:
        return command

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Parallel lines have so much in common. It's a shame they'll never meet.",
       "What do you call a factory that makes good products?" "A satisfactory.",
        "I asked my dog what's two minus two. He said nothing."
    ]

    joke = random.choice(jokes)
    print(joke)
    talk(joke)

def get_spoken_time():
    current_time = datetime.datetime.now()
    hours = current_time.strftime('%I').lstrip('0')
    minutes = current_time.strftime('%M').lstrip('0')
    am_pm = current_time.strftime('%p')
    spoken_time = f"{hours}:{minutes} {am_pm}"
    return spoken_time
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('h3', class_='t')

    results = []
    for result in search_results:
        title = result.text
        link = result.a['href']
        results.append((title, link))
    return results

def ai(prompt):
    text = f'response for Prompt: {prompt} \n ****\n'
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists('all essays, letter etc (va)'):
        os.mkdir('all essays, letter etc (va)')
    with open(f"all essays, letter etc (va)/{''.join(prompt.split('write')[1:]).strip()}.txt", "w") as f:
        f.write(text)

def chat(command):
    global chatStr
    print(f"You: {command}")
    chatStr += f"You: {command}\nJarvis: "
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=chatStr,
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    jarvis_response = response["choices"][0]["text"]
    print(f"Jarvis: {jarvis_response}")
    talk(jarvis_response)
    chatStr = ''
    return jarvis_response

def WafeeMsg(name, message):
    pyautogui.hotkey('win', '7')
    sleep(4)
    click(x=254, y=120)
    sleep(1)
    write(name)
    sleep(2.2)
    click(x=270, y=193)
    sleep(1)
    click(x=892, y=692)
    sleep(1)
    write(message)
    press('enter')

def WafeeCall(name):
    pyautogui.hotkey('win', '7')
    sleep(4)
    click(x=254, y=120)
    sleep(1)
    write('wafee')
    sleep(1.5)
    click(x=270, y=193)
    sleep(1)
    click(x=1271, y=68)
    sleep(1)

def respond_to_greetings(command):
    greetings = ["hello", "hi", "hey"]
    well_being_questions = ["how are you", "how's it going", "how are you doing"]
    self_introduction = ["who are you", "introduce yourself"]
    response = ""

    if any(greeting in command for greeting in greetings):
        response = "Hello! How can I assist you today?"

    elif any(question in command for question in well_being_questions):
        response = "I am doing well, how about you?"
    elif any(question in command for question in self_introduction):
        response = "Hello, I am Jarvis, your intelligent and reliable voice assistant. " \
                    "I'm here to make your everyday tasks easier and more efficient. " \
                    "Whether you need assistance with tasks, information, or anything else, " \
                    "I'm here to help. Just ask, and I'll do my best to provide you with the answers and support you need."
    return response


def run_jarvis():
    while True:
        command = take_command()
        if 'exit' in command or 'goodbye' in command:
            print(f"You: {command}")
            talk('Goodbye!')
            sys.exit()
        greeting_response = respond_to_greetings(command)
        if greeting_response:
            print(f"You: {command}")
            print(f'Jarvis: {greeting_response}')
            talk(greeting_response)
            continue
        elif "open google" in command:
            webbrowser.open('https://www.google.com')
            talk("Opening Google")
        elif "open youtube" in command:
            webbrowser.open('https://www.youtube.com', 2)
            talk('Opening YouTube')
        elif 'open chrome' in command:
            subprocess.Popen(r"C:\Users\HP\OneDrive\Pictures\Desktop\Google Chrome.lnk")
            talk('Opening Chrome')
        elif 'open pycharm' in command:
            subprocess.Popen(r"C:\Users\HP")
        elif 'search' in command:
            print(f'You: {command}')
            google = command.replace('search', '')
            print(f'Jarvis: Searching {google} in google.')
            talk(f'Searching {google} in google.')
            pywhatkit.search(google)
        elif 'search' in command and 'on youtube' in command:
            print(f'You: {command}')
            use = command.replace('search', '').replace('on youtube', '')
            print(f'Jarvis: Searching {use} on youtube.')
            talk(f'Searching {use} on youtube')
            pywhatkit.playonyt(use)
        elif 'tell me about' in command or 'what is' in command:
            person = command.replace('tell me about', '').replace('what is', '').replace('jarvis', '')
            infor = wikipedia.summary(person, 2)
            print(infor)
            talk(infor)
        elif 'when was' in command or 'when is' in command or 'when did' in command:
            person = command.replace('when was', '').replace('when is', '').replace('when did', '')
            info = wikipedia.summary(person)
            print(info)
            talk(info)
        elif 'who is' in command or 'who was' in command:
            person = command.replace('who is', '').replace('who was', '').replace('jarvis', '')
            infor = wikipedia.summary(person, 2)
            print(infor)
            talk(infor)
        elif 'introduce yourself' in command or 'tell us about' in command or 'introduce' in command or 'yourself' in command:
            print(f'You: {command}')
            intro = "Hello, I am Jarvis, your intelligent and reliable voice assistant. " \
                    "I'm here to make your everyday tasks easier and more efficient. " \
                    "Whether you need assistance with tasks, information, or anything else, " \
                    "I'm here to help. Just ask, and I'll do my best to provide you with the answers and support you need."
            print(f'Jarvis: {intro}')
            talk(intro)
        elif 'say the first 50 digits of pi' in command:
            print('Jarvis: 3.14159265358979323846264338327950288419716939937510')
            talk("3.14159265358979323846264338327950288419716939937510")
        elif 'play' in command:
            print(f'You: {command}')
            song = command.replace('play', '')
            print(f'Jarvis: playing {song}')
            talk('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'close this website' in command or 'close this app' in command or 'close this' in command or 'close it' in command:
            print(f'You: {command}')
            talk('OK')
            print(f'Jarvis: OK')
            close_button_x = 1340
            close_button_y = 1
            pyautogui.moveTo(close_button_x, close_button_y, duration=1)
            pyautogui.click()
            time.sleep(2)
        elif 'time' in command:
            print(f'You: {command}')
            spoken_time = get_spoken_time()
            print(f'Jarvis: it is currently {spoken_time}')
            talk(f"it is currently {spoken_time}")
        elif 'take a screenshot' in command:
            print(f'You: take a screenshot')
            print(f'Jarvis: OK')
            talk('OK')
            pyautogui.hotkey('win', 'prtsc')
        elif 'shutdown pc' in command:
            talk('OK')
            os.system("shutdown /s /t 0")
        elif 'restart pc' in command:
            talk('OK')
            os.system("shutdown /r /t 0")
        elif 'tell me a joke' in command:
            print(f'You: {command}')
            print(f'Jarvis: {tell_joke}')
        elif 'write' in command:
            print(f'You: {command}')
            wes = ai(prompt=command)
            print(f'Jarvis: {wes}')
        elif "send a message" in command:
            name = command.replace("send a message", "")
            name = name.replace("to", "")
            wafee = str(name)
            talk(f"whats the message for {wafee}")
            MSG = take_command()
            WafeeMsg(wafee, MSG)
        elif 'call' in command:
            name = command.replace('call' ,'')
            name = name.replace('jarvis' ,'')
            Name = str(name)
            WafeeCall(Name)
        elif 'hello' in command:
            chat(command)

if __name__ == "__main__":
    print('Jarvis: Hello there!, how may i help you.')
    talk('Hello there!, how may i help you.')
    print('Listening...')
    run_jarvis()