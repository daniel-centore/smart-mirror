'''
Created on Apr 21, 2016

@author: cwpyb
'''
from tkinter import *
import HelperMethods

class EmailFrame(Frame):
    
    
    
    def __init__(self, title, master=None):
        Frame.__init__(self, width=300, height=550, bg="black")
        
        self.canvas = Canvas(self, width=300, height=430, bg="black", bd=0, relief='ridge', borderwidth=0, highlightthickness=0)
        self.canvas.place(x=0,y=30)
        
        self.emailLabel = StringVar();
        Label(self, textvariable=self.emailLabel, font=("SFNS Display", 13), bg="black", foreground="gray", anchor=E).place(y=0, x=0)
        self.emailLabel.set("Email")
        
        self.currentEmail = 0;
        
              
            
    def addEmail(self, sender, subject, body):
        self.canvas.create_line(0, 1+((self.currentEmail*85)), 300, 1+((self.currentEmail*85)), fill="white")
        Label(self, text=sender, font=("SFNS Display Bold", 11), bg="black" , foreground="white", anchor=W).place(y=33+(self.currentEmail*85), x=0)
        Label(self, text=subject, font=("SFNS Display", 11), bg="black", foreground="white", anchor=W).place(y=53+(self.currentEmail*85), x=0)
        tbox = Text(self, height=2, width=30, bg="black", font=("SFNS Display", 11), foreground="gray", bd=0, wrap=WORD)
        tbox.place(y=75+(self.currentEmail*85), x=0 )
        tbox.insert(INSERT, body)
        self.currentEmail += 1;
        self.canvas.create_line(0, 1+((self.currentEmail*85)), 300, 1+((self.currentEmail*85)), fill="white")
        
    def updateForUser(self, emails):
        for entry in emails:
            self.addEmail(entry[0], entry[1], entry[2])
            
    def clearEmails(self):
        self.canvas.delete("all")
        for widget in self.winfo_children():
            widget.destroy()
        self.currentEmail = 0
        
        self.canvas = Canvas(self, width=300, height=430, bg="black", bd=0, relief='ridge', borderwidth=0, highlightthickness=0)
        self.canvas.place(x=0,y=30)
        
        self.emailLabel = StringVar();
        Label(self, textvariable=self.emailLabel, font=("SFNS Display", 13), bg="black", foreground="gray", anchor=E).place(y=0, x=0)
        self.emailLabel.set("Email")
