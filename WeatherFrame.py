'''
Created on Apr 7, 2016

@author: cwpyb
'''
from tkinter import *
import HelperMethods
from mirrorbackend import weather

class WeatherFrame(Frame):
    
    main_icon = None
    main_temp = None
    main_highlow = None
    
    day_labels = [];
    day_icons = [];
    day_temps = [];
    
    def __init__(self, title, master=None):
        Frame.__init__(self, width=400, height=300, bg="black")
        global main_icon, main_temp, main_highlow, day_labels, day_icons, day_temps
        
        main_icon = StringVar()
        main_temp = StringVar()
        main_highlow = StringVar()
        
        weatherDays = weather()
        
        day_labels = [];
        day_icons = [];
        day_temps = [];
        day_hilows = [];
        
        main_temp_label = Label(self, textvariable=main_temp, font=("Meteocons", 60), bg="black", foreground="white")
        # main_temp.set("R")
        main_temp.set(weatherDays[0]['icon'])
        main_temp_label.place(x=0,y=0)
        
        main_icon_label = Label(self, textvariable=main_icon, font=("SFNS Display", 36), bg="black", foreground="white")
        # main_icon.set(u"71\xb0")
        main_icon.set(u"%d\xb0" % weatherDays[0]['temp'])
        main_icon_label.place(x=130,y=-5)
        
        main_highlow_label = Label(self, textvariable=main_highlow, font=("SFNS Display", 18), bg="black", foreground="white")
        main_highlow.set(u"( %d\xb0 | %d\xb0 )" % (weatherDays[0]['hi'], weatherDays[0]['lo']))
        main_highlow_label.place(x=100,y=50)
        
        currentday = HelperMethods.getCurrentDay_ShortName()
        
        #HARDCODED WEATHER
        # icons = ["B", "H", "Y", "F", "G"];
        # temps = [u"68\xb0", u"65\xb0", u"54\xb0", u"42\xb0", u"18\xb0"]
        # hilows = [u"( 72\xb0 | 55\xb0 )", u"( 70\xb0 | 61\xb0 )", u"( 59\xb0 | 48\xb0 )", u"( 50\xb0 | 36\xb0 )", u"( 21\xb0 | 16\xb0 )"]
        
        for num in range(0, len(weatherDays) - 1):
            day_labels.append(self.getNextDay(currentday))
            currentday = day_labels[num]
            day_labels[num] = Label(self, text=currentday, font=("SFNS Display", 14), bg="black", foreground="white", anchor=E)
            day_labels[num].place(y=(100 + (num*30)), x=15, width=50)
            
            day_icons.append(Label(self, text=weatherDays[num+1]['icon'], font=("Meteocons", 14), bg="black", foreground="white") )
            day_icons[num].place(y=(102 + (num*30)), x = 70)
            
            day_temps.append(Label(self, text=u"%d\xb0"%weatherDays[num+1]['temp'], font=("SFNS Display", 14), bg="black", foreground="white"))
            day_temps[num].place(y=(100 + (num*30)), x = 100)
            
            day_hilows.append(Label(self, text=u"( %d\xb0 | %d\xb0 )" % (weatherDays[num+1]['hi'], weatherDays[num+1]['lo']), font=("SFNS Display", 12), bg="black", foreground="white"))
            day_hilows[num].place(y=(102 + (num*30)), x = 140)
        
    def getNextDay(self, day):
        if(day == "Mon"):
            return "Tue"
        elif(day == "Tue"):
            return "Wed"
        elif(day == "Wed"):
            return "Thu"
        elif(day == "Thu"):
            return "Fri"
        elif(day == "Fri"):
            return "Sat"
        elif(day == "Sat"):
            return "Sun"
        elif(day == "Sun"):
            return "Mon"
        else:
            return day
        
        
        
