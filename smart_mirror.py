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
import functools

root = Tk()
currentScreen = "Home"
currentWidget = ""
passcodeEntryNum = 0
passcodeEntryStr = ""
selectedUser = 0;

def onKeyPress(event):
	handleEvent(event.char, event.keycode)
	
def button1():
	global root
	root.after(0, hbut1)
def button2():
	global root
	root.after(0, hbut2)
def button3():
	global root
	root.after(0, hbut3)
def button4():
	global root
	root.after(0, hbut4)
def button5():
	global root
	root.after(0, hbut5)
def button6():
	global root
	root.after(0, hbut6)

def hbut1():
	handleEvent('1')
def hbut2():
	handleEvent('2')
def hbut3():
	handleEvent('3')
def hbut4():
	handleEvent('4')
def hbut5():
	handleEvent('5')
def hbut6():
	handleEvent('6')

def handleEvent(eid, keycode=0):
	# print keycode
	global currentScreen, passcodeEntryNum, passcodeEntryStr, selectedUser, userPasscodes, currentWidget
	
	if(currentScreen == "Home" and (eid == "1" or eid == "2" or eid == "3" or eid == "4" or eid == "5")):
		sU = int(eid) - 1
		if sU < len(mirrorbackend.getUsers()):
			selectedUser = sU
			buttons.enterPasscodeScreen();
			currentScreen = "Passcode"
	elif(currentScreen == "Home" and eid == "6"):
		currentScreen = "GenSettings"
		genSettings.place(x=0,y=0);
		buttons.enterSettingsScreen();
	elif(currentScreen == "Passcode"):
		if(eid == '1'):
			passcodeEntryStr += "a";
			passcodeEntryNum+=1
		elif(eid == '2'):
			passcodeEntryStr += "b";
			passcodeEntryNum+=1
		elif(eid == '3'):
			passcodeEntryStr += "c";
			passcodeEntryNum+=1
		elif(eid == '4'):
			passcodeEntryStr += "d";
			passcodeEntryNum+=1
		elif(eid == '5'):
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
			if(eid == "5"):
				currentScreen = "Home"
				buttons.enterHomeScreen()
				updateWidgets()
				selectedUser = 0;
				email.clearEmails();
				calendar.clearCalendar();
				music.clearMusic();
				logout()
			elif(eid == "3"):
				currentScreen = "User"
				currentWidget = "Music"
				music.reload()
				buttons.enterMusicWidget()
			elif(eid == "6"):
				currentScreen = "UserSettings"
				userSettings.place(x=0,y=0);
				buttons.enterSettingsScreen();
		elif(currentWidget == "Music"):
			if(eid == "1"):
				music.startPause(mirrorbackend.getUsers()[selectedUser])
			elif(eid == "2"):
				music.nextSong(mirrorbackend.getUsers()[selectedUser])
			elif(eid == "4"):
				music.moveArrowUp()
			elif(eid == "3"):
				music.moveArrowDown()
			elif(eid == "5"):
				if music.select(mirrorbackend.getUsers()[selectedUser]) == False:
					# If back button has been activated
					currentScreen = "User"
					currentWidget = ""
					buttons.enterUserScreen();
		
	elif(currentScreen == "GenSettings"):
		if(eid == "1"):
			genSettings.moveArrowUp()
		elif(eid == "2"):
			genSettings.moveArrowDown()
		elif(eid == "3"):
			# genSettings.select()
			pass
		elif(eid == "5"):
			genSettings.place_forget()
			buttons.enterHomeScreen()
			currentScreen = "Home"
		elif(eid == "6"):
			genSettings.place_forget()
			buttons.enterHomeScreen()
			blackscreen.place(x=0,y=0);
			currentScreen = "BlackG";
		elif(keycode == 36): #enter button
			ret = genSettings.enter()
			if(ret != None):
				mirrorbackend.adduser(ret[0], ret[1])
		elif(keycode == 22): #backspace
			genSettings.backspace()
		else:
			genSettings.keyPress(eid)
	elif(currentScreen == "UserSettings"):
		if(eid == "1"):
			userSettings.moveArrowUp()
		elif(eid == "2"):
			userSettings.moveArrowDown()
		elif(eid == "3"):
			# userSettings.select()
			pass
		elif(eid == "5"):
			userSettings.place_forget()
			buttons.enterUserScreen();
			currentScreen = "User"
		elif(eid == "6"):
			userSettings.place_forget()
			buttons.enterUserScreen()
			blackscreen.place(x=0,y=0);
			currentScreen = "BlackU";
		elif(keycode == 13): #enter button
			ret = userSettings.enter()
			if(ret != None):
				mirrorbackend.getUsers()[selectedUser].changePasscode(ret)
		elif(keycode == 8): #backspace
			userSettings.backspace()
		else:
			userSettings.keyPress(eid)
	elif(currentScreen == "BlackU"):
		if(eid == "6"):
			blackscreen.place_forget()
			currentScreen = "User"
	elif(currentScreen == "BlackG"):
		if(eid == "6"):
			blackscreen.place_forget()
			currentScreen = "Home"

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
	
	# GPIO
	try:
		from gpiozero import Button
		
		buttonA = Button(21)
		buttonA.when_pressed = button1
		
		buttonB = Button(16)
		buttonB.when_pressed = button2
		
		buttonC = Button(12)
		buttonC.when_pressed = button3
		
		buttonD = Button(25)
		buttonD.when_pressed = button4
		
		buttonE = Button(23)
		buttonE.when_pressed = button5
		
		buttonF = Button(18)
		buttonF.when_pressed = button6
		
	except:
	    print("This is not running on a Raspberry Pi")
	
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
	
	global blackscreen;
	blackscreen = BlackScreen(root, "Black Screen")
	blackscreen.place(x=1080, y=1920);
	
	root.after(500, updateTime)
	root.mainloop() #Starts the Tkinter and onKeyPress event
	
