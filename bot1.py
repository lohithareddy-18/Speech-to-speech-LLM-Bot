#!/usr/bin/env python
# coding: utf-8

# # Installing requirements 

# In[2]:


pip install speechrecognition langdetect openai gtts pygame


# # Importing Libraries

# In[11]:


import speech_recognition as sr
import openai
from langdetect import detect
from gtts import gTTS
import os
import pygame
import cv2
from IPython.display import display, HTML, Javascript
from PIL import Image
import datetime
import random


# # OpenAI API Key

# In[12]:


openai.api_key = "your_real_api_key_here"


# # Pop up for webcamera access

# In[13]:


def request_webcam_access():
    display(Javascript("""
    (async function() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            alert("Webcam access granted!");
        } catch (err) {
            alert("Webcam access denied or not available.");
        }
    })();
    """))


# # Code to capture speech from user

# In[14]:


def capture_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return None
        except sr.WaitTimeoutError:
            print("Timeout. Try again.")
            return None


# # Query to Bot

# In[15]:


def query_gpt(prompt, response_language="en"):
    try:
        if response_language != "en":
            prompt = f"Respond in {response_language}: {prompt}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response['choices'][0]['message']['content']
        return reply.strip()
    except Exception as e:
        print(f"Error querying GPT: {e}")
        return "I encountered an issue. Please try again."


# # Text-to-Speech converstion

# In[16]:


def speak_text(text, language="en"):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save("output.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()
        os.remove("output.mp3")
    except Exception as e:
        print(f"Text-to-speech error: {e}")


# # Save the captured video by webcam

# In[17]:


def show_and_save_webcam():
    # OpenCV to capture video
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Video codec and output file
    out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (frame_width, frame_height))

    print("Recording video... Press 'q' to stop.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        display(img)
        
        # Stop recording if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print("Video saved as 'output_video.mp4'")


# # Detecting language by user input

# In[18]:


def determine_response_language(user_input):
    if "telugu" in user_input.lower():
        return "te"
    elif "hindi" in user_input.lower():
        return "hi"
    elif "english" in user_input.lower():
        return "en"
    return None


# # Greetings from user 

# In[19]:


def check_greeting(user_input):
    greetings = ["hi", "hello", "hola"]
    for greeting in greetings:
        if greeting in user_input.lower():
            return True
    return False


# # Time Query if user ask for time 

# In[20]:


def check_time_query(user_input):
    time_keywords = ["time", "current time", "what time is it", "tell me the time"]
    for keyword in time_keywords:
        if keyword in user_input.lower():
            return True
    return False


# # User ask joke 

# In[21]:


def check_joke_query(user_input):
    joke_keywords = ["joke", "tell me a joke", "say joke"]
    for keyword in joke_keywords:
        if keyword in user_input.lower():
            return True
    return False


# # dish query

# In[22]:


def check_dish_query(user_input):
    dish_keywords = ["dish", "best dish", "famous dish"]
    for keyword in dish_keywords:
        if keyword in user_input.lower():
            return True
    return False


# # Funtion to get random joke

# In[23]:


def get_random_joke():
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don’t oysters donate to charity? Because they are shellfish!",
        "I’m reading a book about anti-gravity. It’s impossible to put down."
    ]
    return random.choice(jokes)


# # Suggest famous dish

# In[24]:


def get_famous_dish():
    dishes = [
        "Pizza from Italy",
        "Sushi from Japan",
        "Tacos from Mexico",
        "Pasta from Italy",
        "Biryani from India"
    ]
    return random.choice(dishes)


# # Implementing all queries in bot using pipeline 

# In[27]:


def chatbot_pipeline():
    print("Welcome to the Multilingual Speech-to-Speech Bot!")
    
    # Display title with emoji
    display(HTML("<h1>Welcome to the Bot World! 🤖</h1>"))
    
    # Show webcam access request pop-up
    request_webcam_access()
    
    # Initial greeting
    greeting = "How would I need to help you today?"
    print(f"Bot: {greeting}")
    speak_text(greeting, "en")
    
    while True:
        user_input = capture_speech()
        if user_input is None:
            continue
        
        # Check if user says "hi", "hello", or "hola"
        if check_greeting(user_input):
            response = "How can I help you today?"
            print(f"Bot: {response}")
            speak_text(response, "en")
            continue

        # Check for time query
        if check_time_query(user_input):
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            response = f"The current time is {current_time}."
            print(f"Bot: {response}")
            speak_text(response, "en")
            continue

        # Check for joke query
        if check_joke_query(user_input):
            joke = get_random_joke()
            response = joke
            print(f"Bot: {response}")
            speak_text(response, "en")
            continue

        # Check for dish query
        if check_dish_query(user_input):
            dish = get_famous_dish()
            response = f"One famous dish is {dish}."
            print(f"Bot: {response}")
            speak_text(response, "en")
            continue
        

        # Check if the user wants to exit
        if "exit" in user_input.lower() or "bye" in user_input.lower():
            print("Exiting... Goodbye!")
            speak_text("Goodbye! Have a great day!")
            # Save the video when user exits
            show_and_save_webcam()
            break

        # Get GPT response in the appropriate language
        response = query_gpt(user_input, response_language)
        print(f"Bot ({response_language}): {response}")


# In[ ]:


# Run the chatbot
chatbot_pipeline()


# In[ ]:




