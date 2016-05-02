'''
Created on Apr 13, 2016

@author: cwpyb
'''

import datetime
import calendar

def ordinal(n):
    n = int(n);
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
        return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")

def getFormattedTime():
    now = datetime.datetime.now();
    return(now.strftime("%I:%M %p").lower())

def getFormattedDate():
    today = datetime.datetime.today();
    
    ordinalDay = ordinal(today.strftime("%d"))
    formmatedOutput = today.strftime("%A, %B ORDINAL, %Y")
    
    finalstr = formmatedOutput.replace("ORDINAL", ordinalDay)
    return finalstr

def getCurrentDay_FullName():
    today = datetime.datetime.today();
    name = calendar.day_name[today.weekday()]
    return name
    
def getCurrentDay_ShortName():
    today = datetime.datetime.today();
    return(today.strftime("%a"));