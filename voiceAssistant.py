
from newsapi import NewsApiClient
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
import re
import sys
import pywhatkit
import pickle

webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id) #voices[0] can be used for male voice
newsapi=NewsApiClient(api_key='89b19b7ee08c4de1b31a6a62551f4b16')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=0
    hour=int(datetime.datetime.now().hour)   
    if hour>= 0 and hour<12:
        speak("A very Good Morning to you Sir !")

    elif hour>=12 and hour < 18:
        speak("A very Good Afternoon to you Sir !")

    else:
        speak("A very Good Evening to you Sir !")   

def  takeCommand():
    r=sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening.......")
        r.pause_threshhold=100
        audio=r.listen(source)

    try:
        print("Recognizing.......")
        query=r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to recognize your voice")
        return "None"    

    return query 

def get_price(url):
    data = requests.get(url)
    soup = BS(data.text, 'html.parser')
    ans = soup.find("div", class_ ="BNeawe iBp4i AP7Wnd").text
    return ans      

a_file=open("contact.pkl","rb")
contact=pickle.load(a_file)
a_file.close()

if __name__ == '__main__':
    clear = lambda: os.system('cls')
     
    # This Function will clean any
    # command before execution of this python file
    clear()

    while True:
        check=takeCommand().lower()
        print(check)
        if 'robin' in check:
            try:
                wishMe()
                query=takeCommand().lower()

                if 'wikipedia' in query: #command:"wikipedia {keyword}"
                    query=query.replace('wikipedia'," ")
                    query=query.replace(" ","",1)
                    speak(f"Searching wikipedia for {query}")
                    results = wikipedia.summary(query, sentences = 4)
                    speak(f"According to wikipedia. {results}")

                elif 'open site' in query:#command:"open site {site 1} {site 2} {site 3}..."
                    l=query.split(" ")
                    for i in l:
                        if re.search(".com$",i):
                            speak(f"opening {i}")
                            webbrowser.get('chrome').open(i)

                elif 'open' in query or 'run' in query:#command:"open/run {shortcut name saved in dir}"
                    query=query.replace("run","")
                    query=query.replace("open","")
                    query=query.replace(" ","",1)
                    dir=f"C:/Users/shaur/OneDrive/Desktop/voiceassistant/shortcuts/{query}.lnk"#enter all shortcuts in a folder and specify its path here
                    dir1=f"C:/Users/shaur/OneDrive/Desktop/voiceassistant/shortcuts/{query}.url"##enter all shortcuts in a folder and specify its path here
                    speak(f"opening {query}")
                    try:
                        os.startfile(dir)
                    except:
                        os.startfile(dir1)  

                elif 'play' in query:#command:"play {video/song name}"
                    song=query
                    song=song.replace("play","")
                    song1=song
                    song=song.replace(" ","",1)
                    song=song.replace(" ","+")
                    speak(f"playing {song1} on youtube")
                    pywhatkit.playonyt(song)

                elif 'search google' in query:#command:"search google {keywords}"
                    q=query
                    q=q.replace("search google","")
                    q1=q
                    q=q.replace(" ","",1)
                    q=q.replace(" ","+")
                    speak(f"google resaults for {q1}")
                    pywhatkit.search(q) 

                elif query=="add contact":#command:"add contact" Note: create a "contact.pkl" file in the folder you have stored the python code
                    speak("please tell the name")
                    name=takeCommand().lower()
                    speak("please tell the number")
                    number=takeCommand().lower()
                    number=number.replace(" ","")
                    number=number.replace("plus","+")
                    if "+" not in number:
                        number="+"+number
                    number=number.replace(""," ")    
                    contact[name]=number
                    speak(f"added contact of {name}")
                    a_file=open("contact.pkl","wb")
                    pickle.dump(contact,a_file)
                    a_file.close()

                elif query=="delete contact":#command:"delete contact"
                    speak("whose contact do you want to delete")
                    name=takeCommand().lower()
                    del contact[name]  
                    speak(f"deleted contact of {name}")
                    a_file=open("contact.pkl","wb")
                    pickle.dump(contact,a_file)
                    a_file.close() 

                elif 'what is the contact of' in query:#command:"what is the contact of {name}"
                    q=query
                    q=q.replace("what is the contact of ","")
                    speak(f"number of {q} is {contact[q]}")

                elif query=='all contacts':#command:"all contacts"
                    for i in contact:
                        speak(f"contact of {i} is {contact[i]}")  

                elif query=="send a whatsapp":#command:"send a whatsapp"
                    speak( "tell receiver's name")
                    name=takeCommand().lower()
                    number=contact[name]
                    number=number.replace(" ","")
                    speak("tell the message")
                    txt=takeCommand().lower()
                    hr=int(datetime.datetime.now().hour)
                    mn=int(datetime.datetime.now().minute) 
                    mn=mn+1
                    if(mn==60):
                        mn=0
                        hr=hr+1
                    if(hr==24):
                        hr=0
                    pywhatkit.sendwhatmsg(contact[name],txt,hr,mn) 
                    speak(f"sending whatsapp message to {name}")  

                elif query=="news":#command:"news"
                    speak("Tell category")
                    cat=takeCommand().lower()
                    top_headlines = newsapi.get_top_headlines(q=cat,language='en',)
                    for article in top_headlines['articles']:
                        speak(article['title'])

                elif query=="crypto":#command:"crypto"
                    speak("tell the currency")
                    curr=takeCommand().lower()
                    url = f"https://www.google.com/search?q={curr}+price"   
                    ans = get_price(url)
                    speak(f"one {curr} is {ans}")   

                elif query=="turn off":#command:"turn off"
                    speak("say shutdown to shutdown windows")
                    passcode=takeCommand().lower()
                    passcode=passcode.replace(" ","")
                    if passcode=="shutdown":
                        speak("shutting down windows")
                        os.system("shutdown /s /t 1")  
                    else:
                        speak("shutdown failed")      

                elif query=="restart":#command:"restart"
                    speak("say restart to restart windows")
                    passcode=takeCommand().lower()
                    passcode=passcode.replace(" ","")
                    if passcode=="restart":
                        speak("restarting windows")
                        os.system("shutdown /r /t 1")  
                    else:
                        speak("restart failed")        
                                                   
            except:
                speak("Sorry Sir, Currently not able to perform the following action")  

            if query=='shutdown':#command:"shutdown"
                    speak('shutting down and stopping listening to you')
                    sys.exit()  
                
        

      


    
   


