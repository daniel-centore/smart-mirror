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
		buttons.enterPasscodeScreen();
		currentScreen = "Passcode"
		selectedUser = int(event.char) - 1
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
			else:
				buttons.enterHomeScreen()
				currentScreen = "Home"
			
			passcodeEntryNum = 0;
			passcodeEntryStr = ""
	elif(currentScreen == "User"):
		if(event.char == "5"):
			if(currentWidget == ""):
				currentScreen = "Home"
				buttons.enterHomeScreen()
				updateWidgets()
				selectedUser = 0;
				email.clearEmails();
				calendar.clearCalendar();
			elif(currentWidget == "Music"):
				currentScreen = "User"
				currentWidget = ""
				buttons.enterUserScreen();
		elif(event.char == "3"):
			currentScreen = "User"
			currentWidget = "Music"
			buttons.enterMusicWidget()
		elif(event.char == "6"):
			currentScreen = "UserSettings"
			userSettings.place(x=0,y=0);
			buttons.enterSettingsScreen();
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
			
		if(mirrorbackend.getUsers()[selectedUser].displayClock()):
			weather.place(x=50,y=230)
		else:
			weather.place_forget()
			
		if(mirrorbackend.getUsers()[selectedUser].displayCalendar()):
			calendar.place(x=20,y=550)
		else:
			calendar.place_forget()
			
		if(mirrorbackend.getUsers()[selectedUser].displayEmail()):
			email.place(x=10,y=1150)
		else:
			email.place_forget()
	
	elif(currentScreen == "Home"):
		clock.place(x=50,y=50)
		weather.place(x=50,y=230)
		calendar.place_forget()
		email.place_forget()

def initRoot():
	root.attributes('-fullscreen', True)
	#root.config(cursor = "none")
	root.configure(background = 'black')
	root.bind('<KeyPress>', onKeyPress)
	
if __name__ == "__main__":
	
	mirrorbackend.initialize()
	
	initRoot();
	
	global clock;
	clock = ClockFrame(root, "Clock")
	clock.place(x=50,y=50)
	
	global weather;
	weather = WeatherFrame(root, "Weather")
	weather.place(x=50,y=230)
	
	global buttons;
	buttons = ButtonFrame(root, "Buttons")
	buttons.place(x=0, y=1720);
	
	global calendar;
	calendar = CalendarFrame(root, "Calendar")
	
	global email;
	email = EmailFrame(root, "Email")
	
	global music;
	music = MusicFrame(root, "Music")
	
	global genSettings;
	genSettings = GeneralSettingsFrame(root, "General Settings")
	
	global userSettings;
	userSettings = UserSettingsFrame(root, "User Settings")
	
	root.after(500, updateTime)
	root.mainloop() #Starts the Tkinter and onKeyPress event
	
	
	
	
	
	
	
	
