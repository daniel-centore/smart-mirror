# pip install --upgrade google-api-python-client
# pip install python-mpd2
# pip install mopidy-gmusic
# pip install requests

# Python 2 thru 3 Support
from __future__ import print_function
from builtins import input

# oauth
import httplib2
import os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
import time
import mpd
import subprocess
import random
import pprint
pp = pprint.PrettyPrinter(indent=4)

MAX_USERS = 6

# Lists all users. The person's userid is the index in the tuple.
def listusers():
    global _users
    result = []
    
    for x in _users:
        result.append(x.store.name)
    
    return result

# Adds a user with their 4 digit pin
# Returns true if successful; False otherwise
def adduser(name, password):
    global _users
    
    try:
        password = int(password)
    except:
        print("Password not integer")
        return False
    
    if not canadduser():
        print("Users list full")
        return False
    
    _users.append(_User(name, password))
    _savedata()
    return True

# Returns False if we are already full of users
def canadduser():
    global MAX_USERS, _users
    return len(_users) < MAX_USERS

# Validates a user's pin
def validateuser(userid, pin):
    global _users
    return _users[userid].store.password == pin

# Removes a given user
def removeuser(userid):
    global _users
    _users.pop(userid)
    _savedata()

# Adds or replaces Spotify credentials for a user
def addspotify(userid, username, password):
    global _users
    _users[userid].store.spotify = {"username" : username, "password" : password}
    _savedata()

# Clear's a person's Spotify credeentials
def removespotify(userid):
    global _users
    _users[userid].store.spotify = None
    _savedata()
    return

# Adds or replaces Google Play credentials for a user
# All Access is a boolean indicating whether or not the user pays
def addgplay(userid, username, password, all_access):
    global _users
    _users[userid].store.gmusic = {"username" : username, "password" : password, "all_access" : all_access}
    _savedata()
    return

# Clear's a person's Google Play credentials
def removegplay(userid):
    global _users
    _users[userid].store.gmusic = None
    _savedata()
    return

# Lists all a user's playlists as strings
def listplaylists(userid):
    if _mpdClient(userid) == None:
        return []
    
    rawData = _mpdClient(userid).listplaylists()
    playlists = []
    
    for playlist in rawData:
        playlists.append(playlist['playlist'])
    
    return playlists

# Lists all the songs in a playlist along with their metadata
def listsongs(userid, playlistname):
    try:
        return _mpdClient(userid).listplaylistinfo(playlistname)
    except Exception:
        pass
    return []

# Plays a song and shuffles the rest of the playlist
# ex. playsong(0, "Anime", "gmusic:track:37f9bdd9-dd2c-390b-9c72-c6c9e7353fbe")
def playsong(userid, playlistname, file):
    try:
        client = _mpdClient(userid);
        client.stop()
        client.clear()
        
        client.add(file)
        
        songs = client.listplaylistinfo(playlistname)
        random.shuffle(songs)
        
        for song in songs:
            if song['file'] != file:
                client.add(song['file'])
        
        client.play(0)
    except Exception:
        pass

# Shuffles a playlist
def shuffleplaylist(userid, playlistname):
    try:
        client = _mpdClient(userid);
        client.stop()
        client.clear()
        
        songs = client.listplaylistinfo(playlistname)
        random.shuffle(songs)
        
        for song in songs:
            client.add(song['file'])
        
        client.play(0)
    except Exception:
        pass

# Toggles whether or not we are paused
def pause(userid):
    try:
        _mpdClient(userid).pause()
    except Exception:
        pass

# Jumps to next song
def next(userid):
    try:
        _mpdClient(userid).next()
    except Exception:
        pass

#################################################################################
# Requests access to Google (Tasks + Calendar) for the user (this will pop open a web browser window)
# If the user has already authenticated once, forces them to re-authenticate
# TODO
def addgoogle(userid):
    _savedata()
    return

# Returns a person's tasks TODO
def gettasks(userid):
    return ["Buy milk", "Go to store", "Call grandma"]

# Returns a person's calendar appointments TODO
def getcalendar(userid):
    return ["Meeting @ 9am", "Robotics competition", "Swim meet"]

#################################################################################

# Sets user's location to a zip code
def setlocation(zip):
    _UserSave.zip = zip
    _savedata()
    return

# TODO
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

# All of a user's persistent data
class _UserSave:
    zip = 06477     # TODO: Switch to 12180
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.spotify = None # {username = "fred", password = "flnstone"}
        self.gmusic = None  # {username = "fred", password = "flnstone", all_access = True}

# All of a user's data
class _User:
    def __init__(self, name, password):
        self.store = _UserSave(name, password)
        self.mopidy = None
        self.mopidyport = 0
        self.mpdclient = None

# Obtains a fresh client for mpd
# You should call this once in each function that uses it, and then reuse it within the function
def _mpdClient(userid):
    global _users
    
    user = _users[userid]
    
    if user.mopidyport == 0:
        return None
    
    if user.mpdclient != None:
        try:
            user.mpdclient.close()
            user.mpdclient.kill()
        except Exception:
            pass
    
    try:
        client = mpd.MPDClient(use_unicode = True)
        client.connect("localhost", user.mopidyport)
        user.mpdclient = client
    except Exception:
        return None
    
    return user.mpdclient

# Saves user data to a file TODO
def _savedata():
    global _users

# Kill's a user's mopidy instance (if any) and loads a new one with the most up to date info
def _updateMopidy(userid):
    global _users
    global _mopidyPort
    
    _mopidyPort += 1
    
    user = _users[userid]
    store = user.store

    if user.mopidy != None:
        user.mopidy.kill()
    
    currentpath = os.path.dirname(os.path.realpath(__file__))
    configpath = os.path.join(currentpath, "mopidy%d.conf" % userid)
    
    with open(configpath, "w") as text_file:
        text_file.write("[spotify]\n")
        if store.spotify != None:
            text_file.write("username = %s\n" % store.spotify['username'])
            text_file.write("password = %s\n" % store.spotify['password'])
        else:
            text_file.write("enabled = false\n")
        text_file.write("\n")
        
        text_file.write("[gmusic]\n")
        if store.gmusic != None:
            text_file.write("username = %s\n" % store.gmusic['username'])
            text_file.write("password = %s\n" % store.gmusic['password'])
            text_file.write("all_access = %s\n" % ("true" if store.gmusic['all_access'] else "false"))
            text_file.write("radio_stations_as_playlists = false\n")
            text_file.write("radio_stations_count = 1\n")
            text_file.write("radio_tracks_count = 1\n")
        else:
            text_file.write("enabled = false\n")
        text_file.write("\n")
        
        text_file.write("[mpd]\n")
        text_file.write("enabled = true\n")
        text_file.write("hostname = 127.0.0.1\n")
        text_file.write("port = %d\n" % _mopidyPort)
        text_file.write("password =\n")
        text_file.write("max_connections = 20\n")
        text_file.write("connection_timeout = 60\n")
        text_file.write("zeroconf = Mopidy MPD server on\n")
        text_file.write("command_blacklist = listall,listallinfo\n")
        text_file.write("default_playlist_scheme = m3u\n")
        text_file.write("\n")
        text_file.write("[http]\n")
        text_file.write("enabled = false\n")
        text_file.close()
        
        fh = open("NUL", "w")
        user.mopidy = subprocess.Popen(["mopidy", "-q", "--config", configpath], stdout = fh, stderr = fh)
        user.mopidyport = _mopidyPort

# GPIO
try:
    # https://www.raspberrypi.org/learning/getting-started-with-gpio-zero/worksheet/
    from gpiozero import Button
except:
    print("This is not running on a Raspberry Pi :(")


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/tasks.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Smart Mirror'

# Users array
_users = None

# The port of the last created mopidy instance
_mopidyPort = 6600

# Whether or not we are currently running on Linux
_linux = False

# Handles initial load procedure
def initialize():
    global _users, _linux
    _users = []
    
    from sys import platform as _platform
    _linux = _platform.startswith('linux')
    
    if _linux:
        subprocess.call(["killall", "mopidy"])      # Always start clean
        time.sleep(3)

def test(testname, val, nominal):
    if val == nominal:
        print("%-50s[PASS]" % testname)
    else:
        print("%-50s[!!FAIL!!]" % testname)

initialize()

## Test Script ##
if __name__ == "__main__":
    print("BACKEND TEST SCRIPT")
    print()
    
    # for use during testing to keep credentials out of source control
    import credentials
    
    # Add users
    adduser("Daniel", 1234)
    adduser("Chris", 5678)
    adduser("Both", 0123)
    
    # Add users' credentials
    addgplay(0, "drdanielfc@gmail.com", credentials.gplaypass(), True)
    _updateMopidy(0)
    
    # addspotify(1, "christopher@pybus.us", credentials.spotifypass())
    # _updateMopidy(1)
    
    # addgplay(2, "drdanielfc@gmail.com", credentials.gplaypass(), True)
    # _updateMopidy(2)
    # addspotify(2, "christopher@pybus.us", credentials.spotifypass())
    # _updateMopidy(2)
    
    addgoogle(0)
    addgoogle(2)
    
    # Test logging in as each user:
    test("Logging in user 0 with correct password", validateuser(0, 1234), True)
    test("Logging in user 0 with incorrect password", validateuser(0, 1235), False)
    test("Logging in user 1 with correct password", validateuser(1, 5678), True)
    test("Logging in user 1 with incorrect password", validateuser(1, 1678), False)
    test("Logging in user 2 with correct password", validateuser(2, 0123), True)
    test("Logging in user 2 with incorrect password", validateuser(2, 3221), False)
    
    # Testing list playlists
    print("Listing user 0's playlists...")
    # while len(listplaylists(0)) == 0:
    #     time.sleep(10)
    # pp.pprint(listplaylists(0))

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
