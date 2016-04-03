# sudo apt-get install python-tk
import Tkinter as tk
from Tkinter import *
import mirrorbackend

WIDTH = 900
HEIGHT = 1000
BORDER = 10

def onKeyPress(event):
    if event.char >= "1" and event.char <= "6":
        handleButton(int(event.char))
        
def handleButton(button):
    """You should handle button from 1-6 here
    I will call this function from the backend with the actual rPi buttons
    """

def placeLabel(text, x, y, anch):
    var = StringVar()
    label = Label(root, textvariable=var, relief=FLAT, background='black', foreground="white", bd=0, font=("Helvetica", 12), anchor=W, justify=LEFT)
    var.set(text)
    label.pack()
    label.place(x=x,y=y,anchor=anch)
    return label

labels = None
def updateLabels(names):
    global labels
    if (labels != None):
        for x in labels:
            x.destroy()
    labels = []
    LOWER = 20
    for i in range(0, 6):
        labels.append(placeLabel(names[i], i * 128 + 128, HEIGHT - LOWER, N))

root = tk.Tk()
root.attributes('-fullscreen', True)
root.config(cursor = "none")
root.configure(background = 'black')
root.bind('<KeyPress>', onKeyPress)
canvas = Canvas(root, width=WIDTH, height=HEIGHT, background='black', bd=2)
canvas.pack()
canvas.place(x=-1,y=-1)

placeLabel("Tasks:\n * Groceries\n * Call grandma\n\nCalendar:\n * Preschool closed\n * Dinner at George's", BORDER, 20, NW)

updateLabels(("Daniel", "Chris", "Briannah", "Shaina", "Patrick", "Avery"))
updateLabels(("Daniel", "Chris", "Briannah", "Shaina", "Patrick", "Potato"))
updateLabels(("\xe2\x96\xb2", "\xe2\x96\xbc", "Select", "Back", "Alt", "Off"))

root.mainloop()         #Starts the Tkinter and onKeyPress event
