"""
Backend API for the IED Team UU Smart Mirror
Author: Daniel Centore

Some prerequisites:
pip install --upgrade google-api-python-client
pip install python-mpd2
pip install mopidy-gmusic
pip install requests
"""

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
import rfc3339      # for date object -> date string
import iso8601      # for date string -> date object
import time
import mpd
import subprocess
import random
import json
from json import JSONDecoder
import uuid
import pprint
pp = pprint.PrettyPrinter(indent=4)

MAX_USERS = 6

# Clears all users
def clearusers():
    global _users
    del _users[:]
    _savedata()

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
    
    myid = str(uuid.uuid4())
    _users.append(_User(name, password, myid))
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
    _users[userid].store.spotify = {"type" : "spotify", "username" : username, "password" : password}
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
    _users[userid].store.gmusic = {"type" : "gplay", "username" : username, "password" : password, "all_access" : all_access}
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
def addgoogle(userid):
    global _users
    
    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'creds_%s.json' % _users[userid].store.myid)

    store = oauth2client.file.Storage(credential_path)
    # credentials = store.get()
    
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    if flags:
        credentials = tools.run_flow(flow, store, flags)
    else: # Needed only for compatibility with Python 2.6
        credentials = tools.run(flow, store)
    # print('Storing credentials to ' + credential_path)
    
    return credentials

def removegoogle(userid):
    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'creds_%s.json' % _users[userid].store.myid)
    if os.path.isfile(credential_path):
        os.remove(credential_path)

def getgoogle(userid):
    global _users
    
    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'creds_%s.json' % _users[userid].store.myid)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        return None
    
    return credentials

# Returns a person's tasks TODO
def gettasks(userid):
    credentials = getgoogle(userid)
    
    if credentials == None:
        return []
    
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('tasks', 'v1', http=http)

    result = []
    
    taskResults = service.tasklists().list(maxResults=10).execute()
    items = taskResults.get('items', [])
    if not items:
        return None         # No tasks found
    else:
        for item in items:
            pp.pprint(item)
    return ["Buy milk", "Go to store", "Call grandma"]

# Returns a person's calendar appointments TODO
def getcalendar(userid):
    credentials = getgoogle(userid)
    
    if credentials == None:
        return []
    
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
    result = []
    
    import datetime as dt
    if not events:
        return result       # No events found
    for event in events:
        # start = event['start'].get('dateTime', event['start'].get('date'))
        start = event['start']
        if 'date' in start:
            start = start['date']
            start = dt.datetime.strptime(start, '%Y-%m-%d').strftime("%a %-d %b (All day)")
        elif 'dateTime' in start:
            start = start['dateTime']
            start = get_date_object(start).strftime("%a %-d %b (%-I:%M %p)")
        else:
            start = "ERROR"
        
        result.append("%s: %s" % (start, event['summary']))
    # return ["Meeting @ 9am", "Robotics competition", "Swim meet"]
    return result

def get_date_object(date_string):
    return iso8601.parse_date(date_string)

def get_date_string(date_object):
    return rfc3339.rfc3339(date_object)

#################################################################################

# Sets user's location to a zip code
def setlocation(zip):
    global _users
    
    for user in _users:
        user.zip = zip

    _savedata()

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
    def __init__(self, name, password, myid):
        self.name = name
        self.password = password
        self.myid = myid
        self.zip = 06477
        self.spotify = None # {username = "fred", password = "flnstone"}
        self.gmusic = None  # {username = "fred", password = "flnstone", all_access = True}

# All of a user's data
class _User:
    def __init__(self, name, password, myid):
        self.store = _UserSave(name, password, myid)
        self.mopidy = None
        self.mopidyport = 0
        self.mpdclient = None

def user_from_json(json_object):
    # Handle gmusic and spotify accounts
    if 'type' in json_object:
        return json_object
    
    # Handle the main array
    if 'name' in json_object:
        user = _User(json_object['name'], json_object['password'], json_object['myid'])
        user.store.spotify = json_object['spotify']
        user.store.gmusic = json_object['gmusic']
        user.store.zip = json_object['zip']
        return user
    
    print("SOMETHING WENT WRONG 201604131027PM:")
    global pp
    pp.pprint(json_object)
    print()
    return None

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

# Saves user data to a file
def _savedata():
    global _users
    userstores = []
    for user in _users:
        userstores.append(user.store.__dict__)
    with open('data.conf', 'w') as outfile:
        json.dump(userstores, outfile)

def _loaddata():
    global _users
    with open('data.conf', 'r') as myfile:
        data = myfile.read().strip()
    _users = JSONDecoder(object_hook = user_from_json).decode(data)

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


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

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
    
    # Load data from file
    _loaddata()
    
    # Create mopidy instances
    for i, val in enumerate(_users):
        _updateMopidy(i)

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
    # adduser("Daniel", 1234)
    # adduser("Chris", 5678)
    # adduser("Both", 0123)
    #
    # # Add users' credentials
    # addgplay(0, "drdanielfc@gmail.com", credentials.gplaypass(), True)
    # _updateMopidy(0)
    
    # addspotify(1, "christopher@pybus.us", credentials.spotifypass())
    # _updateMopidy(1)
    
    # addgplay(2, "drdanielfc@gmail.com", credentials.gplaypass(), True)
    # _updateMopidy(2)
    # addspotify(2, "christopher@pybus.us", credentials.spotifypass())
    # _updateMopidy(2)
    
    # addgoogle(0)
    # addgoogle(2)
    
    # Test logging in as each user:
    test("Logging in user 0 with correct password", validateuser(0, 1234), True)
    test("Logging in user 0 with incorrect password", validateuser(0, 1235), False)
    test("Logging in user 1 with correct password", validateuser(1, 5678), True)
    test("Logging in user 1 with incorrect password", validateuser(1, 1678), False)
    test("Logging in user 2 with correct password", validateuser(2, 0123), True)
    test("Logging in user 2 with incorrect password", validateuser(2, 3221), False)
    
    # Testing list playlists
    # print("Listing user 0's playlists...")
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
