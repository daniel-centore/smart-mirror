# sudo apt-get install python-tk

from tkinter import *
import mirrorbackend
import time
import HelperMethods
from WeatherFrame import *
from ClockFrame import *
from ButtonFrame import *
from CalendarFrame import *
from SettingsFrames import *
from EmailFrame import *
from MusicFrame import *

root = Tk()
currentScreen = "Home"
currentWidget = ""
passcodeEntryNum = 0
passcodeEntryStr = ""
selectedUser = 0;

def onKeyPress(event):
	
	global currentScreen, passcodeEntryNum, passcodeEntryStr, selectedUser, userPasscodes, currentWidget
	
	if(currentScreen == "Home" and (event.char == "1" or event.char == "2" or event.char == "3" or event.char == "4" or event.char == "5")):
		sU = int(event.char) - 1
		if sU < len(mirrorbackend.getUsers()):
			selectedUser = sU
			buttons.enterPasscodeScreen();
			currentScreen = "Passcode"
	elif(currentScreen == "Home" and event.char == "6"):
		currentScreen = "GenSettings"
		genSettings.place(x=0,y=0);
		buttons.enterSettingsScreen();
	elif(currentScreen == "Passcode"):
		if(event.char == '1'):
			passcodeEntryStr += "a";
			passcodeEntryNum+=1
		elif(event.char == '2'):
			passcodeEntryStr += "b";
			passcodeEntryNum+=1
		elif(event.char == '3'):
			passcodeEntryStr += "c";
			passcodeEntryNum+=1
		elif(event.char == '4'):
			passcodeEntryStr += "d";
			passcodeEntryNum+=1
		elif(event.char == '5'):
			passcodeEntryStr += "e";
			passcodeEntryNum+=1
		
		if(passcodeEntryNum == 4):
			if(mirrorbackend.getUsers()[selectedUser].verifyPasscode(passcodeEntryStr)):
				currentScreen = "User"
				updateWidgets()
				buttons.enterUserScreen();
				calendar.updateForUser(mirrorbackend.getUsers()[selectedUser].getCalendarEvents())
				email.updateForUser(mirrorbackend.getUsers()[selectedUser].getEmails())
				music.updateForUser(mirrorbackend.getUsers()[selectedUser])
			else:
				buttons.enterHomeScreen()
				currentScreen = "Home"
			
			passcodeEntryNum = 0;
			passcodeEntryStr = ""
	elif(currentScreen == "User"):
		if(currentWidget == ""):
			if(event.char == "5"):
				currentScreen = "Home"
				buttons.enterHomeScreen()
				updateWidgets()
				selectedUser = 0;
				email.clearEmails();
				calendar.clearCalendar();
				music.clearMusic();
				logout()
			elif(event.char == "3"):
				currentScreen = "User"
				currentWidget = "Music"
				music.reload()
				buttons.enterMusicWidget()
			elif(event.char == "6"):
				currentScreen = "UserSettings"
				userSettings.place(x=0,y=0);
				buttons.enterSettingsScreen();
		elif(currentWidget == "Music"):
			if(event.char == "1"):
				music.startPause(mirrorbackend.getUsers()[selectedUser])
			elif(event.char == "2"):
				music.nextSong(mirrorbackend.getUsers()[selectedUser])
			elif(event.char == "4"):
				music.moveArrowUp()
			elif(event.char == "3"):
				music.moveArrowDown()
			elif(event.char == "5"):
				if music.select(mirrorbackend.getUsers()[selectedUser]) == False:
					# If back button has been activated
					currentScreen = "User"
					currentWidget = ""
					buttons.enterUserScreen();
		
	elif(currentScreen == "GenSettings"):
		if(event.char == "1"):
			genSettings.moveArrowUp()
		elif(event.char == "2"):
			genSettings.moveArrowDown()
		#elif(event.char == "3"):
			#select
		elif(event.char == "5"):
			genSettings.place_forget()
			buttons.enterHomeScreen()
			currentScreen = "Home"
	elif(currentScreen == "UserSettings"):
		if(event.char == "1"):
			userSettings.moveArrowUp()
		elif(event.char == "2"):
			userSettings.moveArrowDown()
		#elif(event.char == "3"):
			#select
		elif(event.char == "5"):
			userSettings.place_forget()
			buttons.enterUserScreen();
			currentScreen = "User"

def logout():
	import mirrorbackend
	mirrorbackend.stopall()

def updateTime():
	global clock
	clock.updateTime();
	root.after(500, updateTime)
	
def updateWidgets():
	if(currentScreen == "User"):
		if(mirrorbackend.getUsers()[selectedUser].displayClock()):
			clock.place(x=50,y=50)
		else:
			clock.place_forget()
			
		if(mirrorbackend.getUsers()[selectedUser].displayWeather()):
			weather.place(x=50,y=210)
		else:
			weather.place_forget()
			
		if(mirrorbackend.getUsers()[selectedUser].displayCalendar()):
			calendar.place(x=20,y=510)
		else:
			calendar.place_forget()
			
		if(mirrorbackend.getUsers()[selectedUser].displayEmail()):
			email.place(x=10,y=1090)
		else:
			email.place_forget()
			
		if(mirrorbackend.getUsers()[selectedUser].displayMusic()):
			music.place(x=40,y=1610)
		else:
			music.place_forget()
	
	elif(currentScreen == "Home"):
		clock.place(x=50,y=50)
		weather.place(x=50,y=230)
		calendar.place_forget()
		email.place_forget()
		music.place_forget()

def initRoot():
	root.attributes('-fullscreen', True)
	#root.config(cursor = "none")
	root.configure(background = 'black')
	root.bind('<KeyPress>', onKeyPress)
	
if __name__ == "__main__":
	
	import mirrorbackend
	mirrorbackend.initialize()
	
	initRoot();
	
	global clock;
	clock = ClockFrame(root, "Clock")
	clock.place(x=50,y=50)
	
	global weather;
	weather = WeatherFrame(root, "Weather")
	weather.place(x=50,y=210)
	
	global buttons;
	buttons = ButtonFrame(root, "Buttons")
	buttons.place(x=0, y=1720);
	
	global calendar;
	calendar = CalendarFrame(root, "Calendar")
	calendar.place(x=1080, y=1920);
	
	global email;
	email = EmailFrame(root, "Email")
	email.place(x=1080, y=1920);
	
	global music;
	music = MusicFrame(root, "Music")
	music.place(x=1080, y=1920);
	
	global genSettings;
	genSettings = GeneralSettingsFrame(root, "General Settings")
	genSettings.place(x=1080, y=1920);
	
	global userSettings;
	userSettings = UserSettingsFrame(root, "User Settings")
	userSettings.place(x=1080, y=1920);
	
	root.after(500, updateTime)
	root.mainloop() #Starts the Tkinter and onKeyPress event
	
	
	
	
	
	
	
	
