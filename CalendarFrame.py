'''
Created on Apr 21, 2016

@author: cwpyb
'''
from tkinter import *
import HelperMethods

class CalendarFrame(Frame):
    
    def __init__(self, title, master=None):
        # maxHeight = 550
        maxHeight = 550
        Frame.__init__(self, width=400, height=maxHeight, bg="black")
        
        # times = ["8 am", "9 am", "10 am", "11 am", "12 pm", "1 pm", "2 pm", "3 pm", "4 pm", "5 pm", "6 pm", "7 pm", "8 pm", "9 pm", "10 pm"]
        self.canvas = Canvas(self, width=200, height=(maxHeight-40), bg="black", bd=0, relief='ridge', borderwidth=0, highlightthickness=0)
        self.canvas.place(x=80,y=0)
    
    def clearCalendar(self):
        pass
    
    def updateForUser(self, events):
        self.canvas.delete("all")
        for widget in self.winfo_children():
            widget.destroy()
        self.canvas = Canvas(self, width=200, height=510, bg="black", bd=0, relief='ridge', borderwidth=0, highlightthickness=0)
        self.canvas.place(x=80,y=0)
        
        MIN_FULL_DAY = 20
        earliest_event = 7
        latest_event = 16
        
        for event in events:
            if event[2] - event[1] < MIN_FULL_DAY:
                if event[1] < earliest_event:
                    earliest_event = event[1]
                if event[2] > latest_event:
                    latest_event = event[2]
        import math
        earliest_event = int(math.floor(earliest_event))
        latest_event = int(math.ceil(latest_event))
        
        for num in range(0, latest_event - earliest_event + 1):
            tme = earliest_event + num
            txt = ((str(tme) + " am") if 1 <= tme < 12 else ("12 pm" if (tme == 0 or tme == 12) else (str(tme - 12) + " pm")))
            
            Label(self, text=txt, font=("SFNS Display", 13), bg="black", foreground="gray", anchor=E).place(y=((num*35)), x=15, width=60)
            lineY = 13 + ((num*35))
            self.canvas.create_line(0, lineY, 200, lineY, fill="white")
        
        Label(self, text="All Day", font=("SFNS Display", 13), bg="black", foreground="gray", anchor=E).place(y=(((latest_event - earliest_event + 1)*35)), x=15, width=60)
        
        
        allDayIdx = 0
        for event in events:
            name = event[0]
            startTime = event[1]
            endTime = event[2]
            
            # Takes up most of the day
            if endTime - startTime > MIN_FULL_DAY:
                Label(self, text=name, font=("SFNS Display", 13), bg="black", foreground="white", anchor=W) \
                    .place(
                        y = (latest_event - earliest_event + 1 + allDayIdx) * 35,
                        x = 84,
                        width = 150)
                allDayIdx += 1
            else:
                self.canvas.create_rectangle(
                    3,
                    14 + (((startTime - earliest_event) * 35)),
                    196,
                    12 + (((endTime-earliest_event) * 35)),
                    fill="light slate gray"
                )
                Label(self, text=name, font=("SFNS Display", 13), bg="light slate gray", foreground="white", anchor=W) \
                    .place(
                        y = 15 + (((startTime - earliest_event) * 35)),
                        x = 84,
                        width = 150)
