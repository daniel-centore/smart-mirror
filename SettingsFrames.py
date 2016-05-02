'''
Created on Apr 21, 2016

@author: cwpyb
'''
from tkinter import *
import HelperMethods

class GeneralSettingsFrame(Frame):
    
    def __init__(self, title, master=None):
        Frame.__init__(self, width=1080, height=1700, bg="black")
        
        self.gear = PhotoImage(file="./gear.gif")
        self.arrow = PhotoImage(file="./arrow.gif")
        
        Label(self, text="General Settings", font=("SFNS Display", 35), bg="black", foreground="white", anchor=W).place(y=500, x=500, width=500)
        Label(self, text="What would you like to do?", font=("SFNS Display", 18), bg="black", foreground="white", anchor=W).place(y=560, x=500, width=500)
        Label(self, image=self.gear, bg="black", anchor=W, height=100, width=110).place(y=500, x=370)
        self.arrowLabel = Label(self, image=self.arrow, anchor=W, bg="black", height=30, width=60)
        self.arrowLabel.place(y=656, x=340)
        
        self.currentPos = 0;
            
        settings = ["Add/Remove User", "Change brightness", "Enter location", "Change time/date", "Change temperature metric"]
        
        num = 0
        for setting in settings:
            Label(self, text=setting, font=("SFNS Display", 26), bg="black", foreground="white", anchor=W).place(y=650+((num*85)), x=400, width=500)
            num += 1
    
    def moveArrowDown(self):
        if(self.currentPos < 4 and self.currentPos >= 0):
            self.currentPos = self.currentPos + 1;
            self.arrowLabel.place(y=656+((self.currentPos*85)), x=340)
            
    def moveArrowUp(self):
        if(self.currentPos > 0 and self.currentPos <= 4):
            self.currentPos = self.currentPos - 1;
            self.arrowLabel.place(y=656+((self.currentPos*85)), x=340)
      
            
class UserSettingsFrame(Frame):
    
    def __init__(self, title, master=None):
        Frame.__init__(self, width=1080, height=1700, bg="black")
        
        self.gear = PhotoImage(file="./gear.gif")
        self.arrow = PhotoImage(file="./arrow.gif")
        
        Label(self, text="General Settings", font=("SFNS Display", 35), bg="black", foreground="white", anchor=W).place(y=500, x=500, width=500)
        Label(self, text="What would you like to do?", font=("SFNS Display", 18), bg="black", foreground="white", anchor=W).place(y=560, x=500, width=500)
        Label(self, image=self.gear, bg="black", anchor=W, height=100, width=110).place(y=500, x=370)
        self.arrowLabel = Label(self, image=self.arrow, anchor=W, bg="black", height=30, width=60)
        self.arrowLabel.place(y=656, x=340)
        
        self.currentPos = 0;
            
        settings = ["Change passcode", "Add/Change email account", "Add/Change calendar account", "Add/Change music account", ""]
        
        num = 0
        for setting in settings:
            Label(self, text=setting, font=("SFNS Display", 26), bg="black", foreground="white", anchor=W).place(y=650+((num*85)), x=400, width=500)
            num += 1
    
    def moveArrowDown(self):
        if(self.currentPos < 3 and self.currentPos >= 0):
            self.currentPos = self.currentPos + 1;
            self.arrowLabel.place(y=656+((self.currentPos*85)), x=340)
            
    def moveArrowUp(self):
        if(self.currentPos > 0 and self.currentPos <= 3):
            self.currentPos = self.currentPos - 1;
            self.arrowLabel.place(y=656+((self.currentPos*85)), x=340)
