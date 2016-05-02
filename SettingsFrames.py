'''
Created on Apr 21, 2016

@author: cwpyb
'''
from tkinter import *
import HelperMethods

class GeneralSettingsFrame(Frame):
    
    def __init__(self, title, master=None):
        Frame.__init__(self, width=1080, height=1850, bg="black")
        
        self.gear = PhotoImage(file="./gear.gif")
        self.arrow = PhotoImage(file="./arrow.gif")
        
        Label(self, text="General Settings", font=("SFNS Display", 35), bg="black", foreground="white", anchor=W).place(y=500, x=500, width=500)
        Label(self, text="What would you like to do?", font=("SFNS Display", 18), bg="black", foreground="white", anchor=W).place(y=560, x=500, width=500)
        Label(self, image=self.gear, bg="black", anchor=W, height=100, width=110).place(y=500, x=370)
        self.arrowLabel = Label(self, image=self.arrow, anchor=W, bg="black", height=30, width=60)
        self.arrowLabel.place(y=656, x=340)
        
        self.currentPos = 0;
        self.currentScreen = ""
        
        self.interactiveFrame = None
            
        settings = ["Add User", "Remove User", "Change brightness", "Enter location", "Change time/date", "Change temperature metric"]
        
        num = 0
        for setting in settings:
            Label(self, text=setting, font=("SFNS Display", 26), bg="black", foreground="white", anchor=W).place(y=650+((num*85)), x=400, width=500)
            num += 1
    
    def moveArrowDown(self):
        if(self.currentPos < 5 and self.currentPos >= 0):
            self.currentPos = self.currentPos + 1;
            self.arrowLabel.place(y=656+((self.currentPos*85)), x=340)
            
    def moveArrowUp(self):
        if(self.currentPos > 0 and self.currentPos <= 5):
            self.currentPos = self.currentPos - 1;
            self.arrowLabel.place(y=656+((self.currentPos*85)), x=340)
            
    def select(self):
        if(self.currentScreen == ""):
            if(self.currentPos == 0):
                self.currentScreen = "AddUser"
                self.interactiveFrame = AddUserFrame(self)
                self.interactiveFrame.place(x=250, y=1200);
                
                
    def enter(self):
        if(self.interactiveFrame != None):
            ret = self.interactiveFrame.enter();
            if(ret != None):
                self.interactiveFrame.destroy()
                self.currentScreen = ""
                return ret;
        return None
    
    def backspace(self):
        if(self.interactiveFrame != None):
            self.interactiveFrame.backspace();
    
    def keyPress(self, key):
        if(self.interactiveFrame != None):
            self.interactiveFrame.keyPress(key);
            
class UserSettingsFrame(Frame):
    
    def __init__(self, title, master=None):
        Frame.__init__(self, width=1080, height=1850, bg="black")
        
        self.gear = PhotoImage(file="./gear.gif")
        self.arrow = PhotoImage(file="./arrow.gif")
        
        Label(self, text="General Settings", font=("SFNS Display", 35), bg="black", foreground="white", anchor=W).place(y=500, x=500, width=500)
        Label(self, text="What would you like to do?", font=("SFNS Display", 18), bg="black", foreground="white", anchor=W).place(y=560, x=500, width=500)
        Label(self, image=self.gear, bg="black", anchor=W, height=100, width=110).place(y=500, x=370)
        self.arrowLabel = Label(self, image=self.arrow, anchor=W, bg="black", height=30, width=60)
        self.arrowLabel.place(y=656, x=340)
        
        self.currentPos = 0;
        
        self.currentScreen = ""
            
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
            
    def select(self):
        if(self.currentScreen == ""):
            if(self.currentPos == 0):
                self.currentScreen = "ChangePasscode"
                self.interactiveFrame = ChangePasscodeFrame(self)
                self.interactiveFrame.place(x=250, y=1200);
                
    def enter(self):
        if(self.interactiveFrame != None):
            ret = self.interactiveFrame.enter();
            if(ret != None):
                self.interactiveFrame.destroy()
                self.currentScreen = ""
                return ret;
        return None
    
    def backspace(self):
        if(self.interactiveFrame != None):
            self.interactiveFrame.backspace();
    
    def keyPress(self, key):
        if(self.interactiveFrame != None):
            self.interactiveFrame.keyPress(key);
            
            
class AddUserFrame(Frame):
    def __init__(self, title, master=None):
        Frame.__init__(self, width=800, height=300, bg="black")
        
        self.instruct = StringVar()
        self.instruct.set("Type the username, then press enter: ")
        
        self.hinttext = StringVar()
        self.hinttext.set("")
        
        self.textarea = StringVar()
        self.textarea.set("")
        self.textarea_para = ""
        
        Label(self, textvariable=self.instruct, font=("SFNS Display Bold", 22), bg="black", foreground="white", anchor=E).place(x=10, y=10, width=550)
        Label(self, textvariable=self.textarea, font=("SFNS Display", 22), bg="black", foreground="white", anchor=W).place(x=575, y=10)
        Label(self, textvariable=self.hinttext, font=("SFNS Display", 15), bg="black", foreground="gray", anchor=W).place(x=250, y=50)
        
        self.numEnters = 0;
        self.username = "";
        self.password = "";
        
    def enter(self):
        if(self.numEnters == 0):
            self.username = self.textarea.get()
            self.instruct.set("Now enter a 4 digit passcode: ")
            self.hinttext.set("where a-e represent buttons 1-5")
            self.textarea.set("");
            self.numEnters += 1;
            return None
        elif(self.numEnters == 1):
            self.password = self.textarea_para;
            self.instruct.set("Re-enter the 4 digit passcode: ")
            self.textarea.set("");
            self.numEnters += 1;
            return None
        elif(self.numEnters == 2):
            return [self.username, self.password]
    
    
    def keyPress(self, key):
        if(self.numEnters == 0):
            self.textarea.set(self.textarea.get() + key)
        elif(self.numEnters == 1):
            if(len(self.textarea.get()) < 4):
                self.textarea.set(self.textarea.get() + "*")
                self.textarea_para = (self.textarea_para + key)
        elif(self.numEnters == 2):
            if(len(self.textarea.get()) < 4):
                self.textarea.set(self.textarea.get() + "*")
                self.textarea_para = (self.textarea_para + key)
        
    
    def backspace(self):
        if(self.numEnters == 0):
            self.textarea.set(self.textarea.get()[:-1])
        elif(self.numEnters >= 1):
            self.textarea.set(self.textarea.get()[:-1])
            self.textarea_para = (self.textarea_para[:-1])
        
        
class ChangePasscodeFrame(Frame):
    def __init__(self, title, master=None):
        Frame.__init__(self, width=900, height=300, bg="black")
        
        self.instruct = StringVar()
        self.instruct.set("Type a new passcode, then press enter: ")
        
        self.hinttext = StringVar()
        self.hinttext.set("where a-e represent buttons 1-5")
        
        self.textarea = StringVar()
        self.textarea.set("")
        self.textarea_para = ""
        
        Label(self, textvariable=self.instruct, font=("SFNS Display Bold", 22), bg="black", foreground="white", anchor=E).place(x=10, y=10, width=600)
        Label(self, textvariable=self.textarea, font=("SFNS Display", 22), bg="black", foreground="white", anchor=W).place(x=620, y=10)
        Label(self, textvariable=self.hinttext, font=("SFNS Display", 15), bg="black", foreground="gray", anchor=W).place(x=250, y=50)
        
        self.password = "";
        
    def enter(self):
        if(len(self.textarea_para) == 4):
            self.password = self.textarea_para
            self.password.replace("a", "1").replace("b", "2").replace("c", "3").replace("d", "4").replace("e", "5")
            return self.password
        return None
    
    def keyPress(self, key):
        if(len(self.textarea.get()) < 4):
            self.textarea.set(self.textarea.get() + "*")
            self.textarea_para = self.textarea_para + key
    
    def backspace(self):
        self.textarea.set(self.textarea.get()[:-1])
        self.textarea_para = (self.textarea_para[:-1])
        

    
class BlackScreen(Frame):
    def __init__(self, title, master=None):
        Frame.__init__(self, width=1080, height=1920, bg="black")
        
