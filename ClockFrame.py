'''
Created on Apr 7, 2016

@author: cwpyb
'''

from tkinter import *
import HelperMethods

class ClockFrame(Frame):
    
    label_time_text = None
    label_date_text = None
    
    def __init__(self, params, master=None):
        Frame.__init__(self, width=300, height=100, bg="black" )
        global label_time_text, label_date_text
        
        label_time_text = StringVar()
        label_time = Label(self, textvariable=label_time_text, background='black', foreground="white", bd=0, font=("SFNS Display", 40), anchor=W, justify=LEFT)
        label_time_text.set(HelperMethods.getFormattedTime())
        label_time.place(x=0, y=0, anchor=NW)
    
        label_date_text = StringVar()
        label_date = Label(self, textvariable=label_date_text, background='black', foreground="white", bd=0, font=("SFNS Display", 16), anchor=W, justify=LEFT)
        label_date_text.set(HelperMethods.getFormattedDate())
        label_date.place(x=0, y=70, anchor=NW)
     
    def updateTime(self):
        global label_time_text, label_date_text
        label_time_text.set(HelperMethods.getFormattedTime())
        label_date_text.set(HelperMethods.getFormattedDate())
        
    def hide(self):
        self.width = 0;
        self.height = 0;
        
    def show(self):
        self.width = 300;
        self.height = 100;
        
