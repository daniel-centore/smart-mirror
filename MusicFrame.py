'''
Created on Apr 21, 2016

@author: cwpyb
'''
from tkinter import *
import HelperMethods

class MusicFrame(Frame):
    
    def __init__(self, title, master=None):
        Frame.__init__(self, width=400, height=550, bg="black")
        
        self.canvas = Canvas(self, width=300, height=510, bg="blue", bd=0)
        self.canvas.place(x=0,y=0)
        
        self.arrow = PhotoImage(file="./smallarrow.gif")
        
        self.arrowLabel = Label(self, image=self.arrow, anchor=W, bg="black", height=30, width=60)
        self.arrowLabel.place(y=656, x=340)
        
        self.currentPos = 0;
        
        for num in range(0, 5):
            #Label(self, text=times[num], font=("SFNS Display", 13), bg="black", foreground="gray", anchor=E).place(y=((num*35)), x=15, width=50)
            self.canvas.create_line(0, 1+((num*65)), 300, 1+((num*65)), fill="white")
    
    def moveArrowDown(self):
        if(self.currentPos < 3 and self.currentPos >= 0):
            self.currentPos = self.currentPos + 1;
            self.arrowLabel.place(y=656+((self.currentPos*85)), x=340)
            
    def moveArrowUp(self):
        if(self.currentPos > 0 and self.currentPos <= 3):
            self.currentPos = self.currentPos - 1;
            self.arrowLabel.place(y=656+((self.currentPos*85)), x=340)
