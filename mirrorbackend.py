# pip install --upgrade google-api-python-client
# pip install python-mpd2
# pip install mopidy-gmusic

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

import mpd
import pickle


# Lists all users. The person's userid is the index in the tuple.
def listusers():
    return ["Daniel", "Chris", "Briannah"]

# Adds a user
def adduser(username, pin):
    if not canadduser():
        return False
    return True

def validateuser(userid, pin):
    return

# Returns False if we are already full of users
def canadduser():
    return True

# Removes a given user
def removeuser(userid):
    return

# Adds or replaces Spotify credentials for a user
def addspotify(userid, username, password):
    return

# Clear's a person's Spotify credeentials
def removespotify(userid):
    return

# Adds or replaces Google Play credentials for a user
# All Access is a boolean indicating whether or not the user pays
def addgplay(userid, username, password, allaccess):
    return

# Clear's a person's Google Play credentials
def removegplay(userid):
    return

# Lists all a user's playlists as strings
def listplaylists(userid):
    return ["Anime", "Ukrainian Folk", "Classic Rock", "Spongebob"]

# Lists all the songs in a playlist along with their metadata
def listsongs(userid, playlistname):
    return [
        {u'album': u'Fullmetal Alchemist Brotherhood OST', \
        u'x-albumuri': u'gmusic:album:4b567e9f45df6cffbc9793953d6cb6f9', \
        u'x-albumimage': u'https://lh3.googleusercontent.com/iwxS307YhAYKz8PkxJMFFTPJL2virvBZyHr9deR64SY7z3TJxrS6BOFx8RU', \
        u'title': u'Rain (TV size)', \
        u'track': u'1/31', \
        u'artist': u'Akira Senju', \
        u'albumartist': u'Akira Senju', \
        u'file': u'gmusic:track:37f9bdd9-dd2c-390b-9c72-c6c9e7353fbe', \
        u'time': u'90', \
        u'date': u'2010'}, \
        \
        {u'album': u'Fullmetal Alchemist Brotherhood OST', \
        u'x-albumuri': u'gmusic:album:85ed62b962fe26e0e0bd7ddc6d53328d', \
        u'x-albumimage': u'https://lh3.googleusercontent.com/iwxS307YhAYKz8PkxJMFFTPJL2virvBZyHr9deR64SY7z3TJxrS6BOFx8RU', \
        u'title': u'Lullaby of Resembool', \
        u'track': u'14/0', \
        u'artist': u'Senju Akira', \
        u'albumartist': u'Senju Akira', \
        u'file': u'gmusic:track:93a8c5f9-93c8-3db0-8714-272cc759aa3a', \
        u'time': u'133', \
        u'date': u'2009'},
    ]

# Plays a song and the rest of its playlist in order
# ex. playsong(0, "Anime", "gmusic:track:37f9bdd9-dd2c-390b-9c72-c6c9e7353fbe")
def playsong(userid, playlistname, file):
    return

# Shuffles a playlist
def shuffleplaylist(userid, playlistname):
    return

# Toggles whether or not we are paused
def togglepause():
    return

#################################################################################
# Requests access to Google (Tasks + Calendar) for the user (this will pop open a web browser window)
# If the user has already authenticated once, forces them to re-authenticate
def addgoogle(userid):
    return

# Returns a person's tasks
def gettasks(userid):
    return ["Buy milk", "Go to store", "Call grandma"]

# Returns a person's calendar appointments
def getcalendar(userid):
    return ["Meeting @ 9am", "Robotics competition", "Swim meet"]

#################################################################################

# Sets user's location to a zip code
def setlocation(zip):
    return

# {
#    "coord":{
#       "lon":-73.69,
#       "lat":42.73
#    },
#    "weather":[
#       {
#          "id":804,
#          "main":"Clouds",
#          "description":"overcast clouds",
#          "icon":"04d"
#       }
#    ],
#    "base":"stations",
#    "main":{
#       "temp":66.9,
#       "pressure":1006,
#       "humidity":43,
#       "temp_min":64.4,
#       "temp_max":69.8
#    },
#    "visibility":16093,
#    "wind":{
#       "speed":17.22,
#       "deg":180,
#       "gust":10.8
#    },
#    "clouds":{
#       "all":90
#    },
#    "dt":1459464840,
#    "sys":{
#       "type":1,
#       "id":2088,
#       "message":0.0634,
#       "country":"US",
#       "sunrise":1459420569,
#       "sunset":1459466486
#    },
#    "id":5141502,
#    "name":"Troy",
#    "cod":200
# }
def weather():
    # Example image http://openweathermap.org/img/w/04d.png
    return {"main" : "Clouds", "description" : "overcast clouds", "image" : Image.open("04d.png"), "temp" : 66.9, "windspeed" : 17.22, "clouds" : 90, "City" : "Troy"}

class _User:
    zip = 06477     # TODO: Switch to 12180
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.gplay = None
        self.spotify = None

def _loaddata():
    try:
        return pickle.load(open("save.p", "rb"))
    except:
        return []

def _savedata(users):
    global _users
    pickle.dump(users, open("save.p", "wb"))

## Initialization code ##

# GPIO
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
except:
    print("This is not running on a Raspberry Pi :(")


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/tasks.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Smart Mirror'

## Test Script ##
if __name__ == "__main__":
    print("BACKEND TEST SCRIPT")
    print("To get a prompt when done run:")
    print("python -i mirrorbackend.py")
    print()

# client = mpd.MPDClient(use_unicode = True)
# client.connect("localhost", 6600)

# https://console.developers.google.com/apis/credentials?project=smartmirror-1267
# Client ID: 828223958708-vivbe6v9c8kal11i66jifs6k6b6j7mej.apps.googleusercontent.com
# Client secret: qhB-ZeJiCqqO8CS0zWlrq_6b
# google

# Weather
# http://api.openweathermap.org/data/2.5/weather?zip=12180,us&APPID=2d5d020421b0d10dbe30a762c5932f10&units=imperial
# http://api.openweathermap.org/data/2.5/forecast?id=5141502&APPID=2d5d020421b0d10dbe30a762c5932f10&units=imperial
# http://openweathermap.org/weather-conditions
