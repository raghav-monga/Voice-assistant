import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import json
import pyjokes
import random
import smtplib
import pywhatkit as kit
from covid import Covid
from requests import get
from pytz import country_timezones as c_tz
from pytz import timezone as tz
from pytz import country_names as c_n
from datetime import date
from datetime import timedelta 


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[1].id)
username= ""

def speak(audio):
	engine.say(audio)
	engine.runAndWait()

def wishme():
	hour = int(datetime.datetime.now().hour)
	if hour>=0 and hour<12:
		speak("Good Morning!")

	elif hour>=12 and hour<18:
		speak("Good afternoon!")

	else:
		speak("Good Evening")
	speak("I am Friday, how may i assist you today?")	

def takeCommand():
	r=sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.pause_threshold=1
		audio = r.listen(source)

	try:
		print("Recognizing....")
		query = r.recognize_google(audio, language='en-in')
		print(f"User said: {query}\n")

	except Exception as e:
		print(e)
		print("say that again please..")
		return "None"
	return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email_address', 'your_password')
    server.sendmail('your_email_address', to, content)
    server.close()

def youthoob_video():
    speak("What do you want to play")
    query = takeCommand().lower()
    speak(f"ok playing {query} on youtube")
    kit.playonyt(query)

def covid():
    covid = Covid(source="worldometers")
    speak("Which country information you want")
    query = takeCommand().lower()
    country = query
    try:
        country_data = covid.get_status_by_country_name(country)
        speak(f"Corona Virus Info in {country} according to data provided by worldometer")
        output_text =   (f"Corona Virus Info in {country}:\n")
        speak(f"Confirmed cases are {country_data['confirmed']}")
        output_text +=  f"`⚠️  Confirmed   : {country_data['confirmed']}`\n"
        speak(f"active cases are {country_data['active']}")
        output_text += f"`☢️  Active      : {country_data['active']}`\n"
        speak(f"total deaths are {country_data['deaths']}")
        output_text += f"`⚰️  Deaths      : {country_data['deaths']}`\n"
        speak(f"total recovered cases are {country_data['recovered']}")
        output_text += f"`💖 Recovered   : {country_data['recovered']}`\n"
        output_text += ("Data provided by Worldometer")
        print(output_text)
    except ValueError:
        speak("No information yet about this country")

def whatsmyname():
    global username
    if username == "":
        speak("I don't know, but i will remember if u tell me. Would u like to add it now")
        query = takeCommand().lower()
        if query == 'ok':
           speak("Alright. What should i call you")
           query = takeCommand().lower()
           username = query
           speak(f"You'd like to call you {username}. Is that right")
           query = takeCommand().lower()
           if(query == "yep"):
               speak(f"Sure. I'll call you {username} from now on.")
           else:
               speak("Got it. What should i call you")
               query = takeCommand().lower()
               username = query
               speak(f"okay i will remember {username} as your name")
        else:
            speak("ok, lets stop it for now")
            username = ""
    else:
        speak(f"Your name is {username}")
def weather():
	APPID = "f9f2d475edf2bca62630272adc85d058" #Add your API key here...
	if not APPID:
		speak("Get an API key from openweathermap first.")
		return None
	speak("which location's weather information you need")
	query =takeCommand().lower()
	try:
		CITY = query
		url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}'
		request = get(url)
		result = json.loads(request.text)
		cityname = result['name']
		curtemp = result['main']['temp']
		min_temp = result['main']['temp_min']
		max_temp = result['main']['temp_max']
		country = result['sys']['country']
		desc = result['weather'][0]
		desc = desc['main']
		ctimezone = tz(c_tz[country][0])
		time = datetime.datetime.now(ctimezone).strftime("%A, %I:%M %p")
		fullc_n = c_n[f"{country}"]
		def celsius(c):
			temp = str((c - 273.15)).split(".")
			return temp[0]
		speak(f"Currently in {cityname} it is {celsius(curtemp)} and {desc} with the high of {celsius(max_temp)}°C and low of {celsius(min_temp)}°C")
		print("\n\n" +f"Temperature: {celsius(curtemp)}°C\n"+
			f"Min. Temp. : {celsius(min_temp)}°C\n"
			f"Max. Temp. : {celsius(max_temp)}°C\n\n"
			f"{desc}\n" +f"{cityname}, {fullc_n}\n" + f"{time}\n\n")
	except KeyError:
		speak("No information yet about this city")		

def whatsapp():
    contacts = {"<name1>" : "+91<number>" , "<name2>" : "+91<number>", "<name3>" : "+91<number>"}
    speak("Whom do you want to send message")
    query = takeCommand().lower()
    if query in contacts:
        sendto = contacts.get(query)
        person_name = query
        hrs = int(datetime.datetime.now().strftime("%H"))
        d = datetime.datetime.now() + timedelta(minutes=2)
        mins = int(d.strftime("Z%M").replace('Z0','Z').replace('Z',''))
        speak("whats the message.")
        query = takeCommand().lower()
        message = query
        speak(f" So, that's the message {person_name} saying {message}. Are you ready to send it")
        query = takeCommand().lower()
        if query == 'yes':
            kit.sendwhatmsg(sendto,message,hrs,mins)
            speak("message sent successfully")
        elif query == 'no' or query == 'cancel':
            speak("okay no problem. Message cancelled")
        else:
            speak("since i am having trouble, i won't send that message. You might want to try again later.")
    else:
        speak("No contact found of this name")
				
if __name__ =="__main__":
	wishme()
	while True:
		query = takeCommand().lower()
		 # Logic for executing tasks based on query
		if 'wikipedia' in query:
			speak('Searching Wikipedia...')
			query = query.replace("Wikipedia", "")
			results = wikipedia.summary(query, sentences = 3)
			speak("According to Wikipedia")
			speak(results)
			print(results) 

		elif 'open youtube' in query:
			webbrowser.open("www.youtube.com")
		
		elif 'play on youtube' in query:
			youthoob_video()
			break	
		
		elif 'open google' in query:
			webbrowser.open('www.google.com')
            
		elif 'open coursera' in query:
			webbrowser.open("www.coursera.org")

		elif 'open stackoverflow' in query:
			webbrowser.open("www.stackoverflow.com")

		elif 'time' in query:
			strTime = datetime.datetime.now().strftime("%H:%M:%S")
			speak(f"Sir, the time is {strTime}")   

		elif 'date' in query:
			today = date.today()
			speak(f"Today's date is {today}")
  
		elif 'open googlecolab' in query:
			webbrowser.open("www.googlecolab.com")
		
		elif 'covid' in query or 'corona' in query:
			covid()	

		elif "weather today" in query:
			weather()

		elif "send whatsapp message" in query:
			whatsapp()	

		elif "what's my name" in query:
			whatsmyname()

		elif 'joke' in query:
			speak(pyjokes.get_joke())
# 			print(joke)
			
		elif 'how are you'in query or "what's up" in query:
			lis=['I am cool, what about you?','Just doing my work','Performing my duty of serving you','I am nice and full of energy']
			speak(random.choice(lis))	

		elif 'send email' in query:
			try:
				speak('What should I say?')
				content = takeCommand()
				to = "your_email_address"
				sendEmail(to, content)
				speak("Email has been sent!")
			except Exception as e:
				print(e)
				speak("Sorry Boss, I am not able to send this email")    

		elif 'exit' or 'quit' in query:
			speak("Thank you for using me, have a nice day")
			exit()	           

		
