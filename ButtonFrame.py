'''
Created on Apr 7, 2016

@author: cwpyb
'''

from tkinter import *
import HelperMethods
import mirrorbackend

class ButtonFrame(Frame):
    
    def __init__(self, params, master=None):
        Frame.__init__(self, width=1080, height=200, bg="black" )
        
        self.instruct_text = StringVar()
        self.buttons_labels = [];
        self.buttons_text = [];
        
        instruct_text = StringVar();
        if(len(mirrorbackend.getUsers()) == 0):
            self.instruct_text.set("Add an account in the settings...");
        else:
            self.instruct_text.set("Please select your account...");
        
        instruct_label = Label(self, textvariable=instruct_text, font=("SFNS Display", 16), bg="black", foreground="gray" )
        instruct_label.place(x=50, y=50)
        
        
        for num in range(0,5):
            self.buttons_text.append(StringVar())
            self.buttons_labels.append( Label(self, textvariable=self.buttons_text[num], font=("SFNS Display", 18), bg="black", foreground="white"))
            self.buttons_labels[num].place(x=(0 + (num*180)), y=150, width=175)
        
        num = 0
        for user in mirrorbackend.getUsers():
            self.buttons_text[num].set(user.getName())
            num += 1
    
    def enterPasscodeScreen(self):
        labels = ["1 - 2", "3 - 4", "5 - 6", "7 - 8", "9 - 0"]
        for num in range(0,5):
            self.buttons_text[num].set(labels[num])
           
        self.instruct_text.set("Please enter your four digit passcode...")
        
    def enterUserScreen(self):
        labels = [u"\u2022", u"\u2022", "Music", u"\u2022", "Log Out"]
        for num in range(0,5):
            self.buttons_text[num].set(labels[num])
            
        self.instruct_text.set("Good morning!")
        
    def enterSettingsScreen(self):
        labels = ["Up", "Down", "Select", u"\u2022", "Exit"]
        for num in range(0,5):
            self.buttons_text[num].set(labels[num])
            
        self.instruct_text.set("")
        
    def enterMusicWidget(self):
        # labels = ["Start/Pause", "Next Song", "Move Down", "Select", "Back"]
        labels = ["Play/Pause", "Skip Song", "Down", "Up", "Select"]
        for num in range(0,5):
            self.buttons_text[num].set(labels[num])
            
        self.instruct_text.set("")
        
    def enterHomeScreen(self):
        num = 0
        for user in mirrorbackend.getUsers():
            self.buttons_text[num].set(user.getName())
            num += 1
            
        while num < 5:
            self.buttons_text[num].set("")
            num += 1
            
        self.instruct_text.set("Please select your account...");
    
