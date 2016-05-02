"""
Backend API for the IED Team UU Smart Mirror
Author: Daniel Centore

Some prerequisites:
pip install --upgrade google-api-python-client
pip install python-mpd2
pip install mopidy-gmusic
pip install requests

San Fransisco ttf
Metrocons ttf (weather)
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
from datetime import date, datetime, timedelta
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
from UserObject import *
import urllib2
from timeout import timeout

MAX_USERS = 5

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

def getUsers():
    global _users
    result = []
    for i in range(0, len(_users)):
        result.append(UserObject(_users[i], i))
    return result

# Adds a user with their 4 digit pin
# Returns true if successful; False otherwise
def adduser(name, password):
    global _users
    
    if not canadduser():
        print("Users list full")
        return False
    
    myid = str(uuid.uuid4())
    # usr = _User(name, password, myid);
    usr = makeUser(name, password, myid)
    if len(_users) > 0:
        usr.store.zip = _users[0].store.zip
    _users.append(usr)
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
    _updateMopidy(userid)

# Clear's a person's Spotify credeentials
def removespotify(userid):
    global _users
    _users[userid].store.spotify = None
    _savedata()
    _updateMopidy(userid)

# Adds or replaces Google Play credentials for a user
# All Access is a boolean indicating whether or not the user pays
def addgplay(userid, username, password, all_access):
    global _users
    _users[userid].store.gmusic = {"type" : "gplay", "username" : username, "password" : password, "all_access" : all_access}
    _savedata()
    _updateMopidy(userid)

# Clear's a person's Google Play credentials
def removegplay(userid):
    global _users
    _users[userid].store.gmusic = None
    _savedata()
    _updateMopidy(userid)

# listplaylists(0)
# shuffleplaylist(0, playlistname)
# listsongs(0, playlistname)
# playsong(0, playlistname, file)


# Lists all a user's playlists as strings
@timeout()
def listplaylists(userid):
    if _mpdClient(userid) == None:
        return []
    
    rawData = _mpdClient(userid).listplaylists()
    playlists = []
    
    for playlist in rawData:
        playlists.append(playlist['playlist'])
    
    return playlists

# Lists all the songs in a playlist along with their metadata
@timeout()
def listsongs(userid, playlistname):
    try:
        return _mpdClient(userid).listplaylistinfo(playlistname)
    except Exception:
        pass
    return []

@timeout()
def currentsong(userid):
    try:
        return _mpdClient(userid).currentsong()
    except Exception:
        pass
    return []

@timeout()
def stopall():
    global _users
    try:
        for i, user in enumerate(_users):
            _mpdClient(i).stop()
    except Exception:
        pass

# Plays a song and shuffles the rest of the playlist
# ex. playsong(0, "Anime", "gmusic:track:37f9bdd9-dd2c-390b-9c72-c6c9e7353fbe")
@timeout()
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
@timeout()
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
@timeout()
def pause(userid):
    try:
        _mpdClient(userid).pause()
    except Exception:
        pass

# Jumps to next song
@timeout()
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

# Returns a person's tasks
# TODO: Fix ordering!
@timeout()
def gettasks(userid):
    credentials = getgoogle(userid)
    
    if credentials == None:
        return []
    
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('tasks', 'v1', http=http)

    result = []
    
    tasks = service.tasks().list(tasklist='@default').execute()
    items = tasks.get('items', [])
    if not items:
        return []         # No tasks found
    else:
        for item in items:
            if 'due' in item and len(item['title'].strip()) > 0:
                due = get_date_object(item['due']).strftime("%a %-d %b")
                result.append("%s: %s" % (due, item['title']))
            elif len(item['title'].strip()) > 0:
                result.append(item['title'])
    return result
    # return ["Buy milk", "Go to store", "Call grandma"]

# Returns a person's calendar appointments
@timeout()
def getcalendar(userid):
    credentials = getgoogle(userid)
    
    if credentials == None:
        return []
    
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    startLooking = (datetime.utcnow() - timedelta(days=1)).isoformat() + 'Z' # 'Z' indicates UTC time
    
    # print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=startLooking, maxResults=40, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
    result = []
    
    import datetime as dt
    if not events:
        return result       # No events found
    for event in events:
        # start = event['start'].get('dateTime', event['start'].get('date'))
        start = parseGcalDate(event['start'])
        end = parseGcalDate(event['end'])
        
        if not isinstance(start, datetime):
            start = datetime.combine(start, datetime.min.time())
        if not isinstance(end, datetime):
            end = datetime.combine(end, datetime.max.time())
        
        start += timedelta(minutes=3)
        end -= timedelta(minutes=3)
            
        startDate = start
        endDate = end
        today = date.today()
        if isinstance(startDate, datetime):
            startDate = (startDate + timedelta(minutes=3)).date()
        if isinstance(endDate, datetime):
            endDate = (endDate - timedelta(minutes=3)).date()
        
        # If some portion of the event takes place today
        if startDate <= today and endDate >= today:
            if startDate < today:
                start = datetime.combine(today, datetime.min.time())
            if endDate > today:
                end = datetime.combine(today, datetime.max.time())
            
            evt = feCalEvent(start, end, event['summary'])
            result.append(evt)
            # result.append("%s: %s" % (start, event['summary']))
    # return ["Meeting @ 9am", "Robotics competition", "Swim meet"]
    # print(result)
    return result

def feCalEvent(start, end, text):
    if not (isinstance(start, datetime) and isinstance(end, datetime)):
        return (text, 0, 24)
    # print("%s %s %s" % (text, str(start), str(end)))
    return (text, roundHour(start.hour, start.minute), roundHour(end.hour, end.minute))

def roundHour(hour, min):
    return hour + (min / 60.0)

def parseGcalDate(d):
    if 'date' in d:
        d = d['date']
        d = datetime.strptime(d, '%Y-%m-%d')#.strftime("%a %-d %b (All day)")
    elif 'dateTime' in d:
        d = d['dateTime']
        d = get_date_object(d)#.strftime("%a %-d %b (%-I:%M %p)")
    else:
        d = None
    return d

@timeout()
def getemail(userid):
    credentials = getgoogle(userid)

    if credentials == None:
        return []

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    
    response = service.users().messages().list(userId='me', q='in:inbox', maxResults=10).execute()
    
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])

    while ('nextPageToken' in response) and (len(messages) < 10):
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me', q='', pageToken=page_token).execute()
        messages.extend(response['messages'])
    
    result = []
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        
        subject = '(untitled)'
        sender = '(unknown sender)'
        for header in message['payload']['headers']:
            if header['name'].lower() == 'subject':
                subject = header['value']
            if header['name'].lower() == 'from':
                sender = header['value']
        result.append({'subject': subject, 'snippet':unescape(message['snippet']), 'sender':sender})
    
    return result

import re, htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
# http://effbot.org/zone/re-sub.htm#unescape-html
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
    

def get_date_object(date_string):
    return iso8601.parse_date(date_string)

def get_date_string(date_object):
    return rfc3339.rfc3339(date_object)

#################################################################################

# Sets user's location to a zip code
def setlocation(zip):
    global _users
    
    for user in _users:
        user.store.zip = zip

    _savedata()


# Weather
# http://api.openweathermap.org/data/2.5/weather?zip=12180,us&APPID=2d5d020421b0d10dbe30a762c5932f10&units=imperial
# http://api.openweathermap.org/data/2.5/forecast?id=5141502&APPID=2d5d020421b0d10dbe30a762c5932f10&units=imperial
# http://openweathermap.org/weather-conditions
@timeout()
def weather():
    zip = 6477
    if len(_users) > 0:
        zip = _users[0].store.zip
    zip = "%05d" % zip
    # Example image http://openweathermap.org/img/w/04d.png
    source = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?zip=%s,us&APPID=2d5d020421b0d10dbe30a762c5932f10&units=imperial" % zip).read()
    js1 = json.loads(source)
    cityid = js1['id']
    
    source = urllib2.urlopen("http://api.openweathermap.org/data/2.5/forecast?id=%d&APPID=2d5d020421b0d10dbe30a762c5932f10&units=imperial" % cityid).read()
    js = json.loads(source)
    
    today = date.today()
    lastSample = date(2000, 1, 1)
    result = []
    items = js['list'][:]
    items.insert(0, js1)
    for sample in items:
        curDate = datetime.fromtimestamp(sample['dt']).date()
        if curDate > lastSample:
            lastSample = curDate
            result.append({"icon": convert_icon(sample['weather'][0]['icon'], 'd'), "temp": sample['main']['temp'], "hi": sample['main']['temp_max'], "lo": sample['main']['temp_min'], "date": curDate})
        else:
            result[-1]['hi'] = max(sample['main']['temp_max'], result[-1]['hi'])
            result[-1]['lo'] = min(sample['main']['temp_min'], result[-1]['lo'])
    
    for i in range(1, len(result)):
        result[i]['temp'] = (result[i]['lo'] + result[i]['hi']) / 2
    
    return result

def convert_icon(owm, mytime=None):
    if mytime != None:
        owm = owm.replace('d', mytime).replace('n', mytime)
    return {
        '01d': 'B',
        '01n': 'C',
        '02d': 'H',
        '02n': 'I',
        '03d': 'N',
        '03n': 'N',
        '04d': 'Y',
        '04n': 'Y',
        '09d': 'Q',
        '09n': 'Q',
        '10d': 'R',
        '10n': 'R',
        '11d': '0',
        '11n': '0',
        '13d': 'W',
        '13n': 'W',
        '50d': 'J',
        '50n': 'K'
    }.get(owm, ")")

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

# Kill's a user's mopidy instance (if any) and loads a new one with the most up to date info
def _updateMopidy(userid):
    global _users
    global _mopidyPort
    
    _mopidyPort += 1
    
    user = _users[userid]
    store = user.store

    if user.mopidy != None:
        user.mopidy.kill()
    
    # currentpath = os.path.dirname(os.path.realpath(__file__))
    currentpath = os.getcwd()
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


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/tasks.readonly https://www.googleapis.com/auth/gmail.readonly'
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
    
    # Create mopidy instances TODO: ADD THIS BACK
    for i, val in enumerate(_users):
        _updateMopidy(i)
    
    import atexit
    atexit.register(stopall)

def test(testname, val, nominal):
    if val == nominal:
        print("%-50s[PASS]" % testname)
    else:
        print("%-50s[!!FAIL!!]" % testname)

def user_from_json(json_object):
    # Handle gmusic and spotify accounts
    if 'type' in json_object:
        return json_object
    
    from UserObject import _User
    # Handle the main array
    if 'name' in json_object:
        user = _User(json_object['name'], json_object['password'], json_object['myid'])
        user.store.spotify = json_object['spotify']
        user.store.gmusic = json_object['gmusic']
        user.store.zip = json_object['zip']
        user.store.clock = (json_object['clock'] if 'clock' in json_object else user.store.clock)
        user.store.clock = (json_object['weather'] if 'weather' in json_object else user.store.clock)
        user.store.clock = (json_object['email'] if 'email' in json_object else user.store.clock)
        user.store.clock = (json_object['calendar'] if 'calendar' in json_object else user.store.clock)
        user.store.clock = (json_object['music'] if 'music' in json_object else user.store.clock)
        return user
    
    print("SOMETHING WENT WRONG:")
    global pp
    pp.pprint(json_object)
    print()
    return None

## Test Script ##
if __name__ == "__main__":
    initialize()
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
    # test("Logging in user 0 with correct password", validateuser(0, 1234), True)
    # test("Logging in user 0 with incorrect password", validateuser(0, 1235), False)
    # test("Logging in user 1 with correct password", validateuser(1, 5678), True)
    # test("Logging in user 1 with incorrect password", validateuser(1, 1678), False)
    # test("Logging in user 2 with correct password", validateuser(2, 0123), True)
    # test("Logging in user 2 with incorrect password", validateuser(2, 3221), False)
    
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
