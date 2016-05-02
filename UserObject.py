import warnings

'''
Persistent data
'''
class _UserSave:
    def __init__(self, name, password, myid):
        self.name = name
        self.password = password
        self.myid = myid
        self.zip = 06477
        self.spotify = None # {username = "fred", password = "flnstone"}
        self.gmusic = None  # {username = "fred", password = "flnstone", all_access = True}
        self.clock = True
        self.weather = True
        self.email = True
        self.calendar = True
        self.music = True

'''
Main user data contained for the backend
'''
class _User:
    def __init__(self, name, password, myid):
        self.store = _UserSave(name, password, myid)
        self.mopidy = None
        self.mopidyport = 0
        self.mpdclient = None

'''
Shim for data access by the frontend
'''
class UserObject(object):
    
    def __init__(self, user, id):
        self._user = user
        self._username = user.store.name
        self._passcode = user.store.password
        self._clock = user.store.clock
        self._weather = user.store.weather
        self._email = user.store.email
        self._calendar = user.store.calendar
        self._music = user.store.music
        self.id = id
    
    def username():
        def fget(self):
            return self._username
        def fset(self, value):
            self._username = value
        return locals()
    username = property(**username())
    
    def passcode():
        def fget(self):
            return self._passcode
        def fset(self, value):
            self._passcode = value
        return locals()
    passcode = property(**passcode())
    
    def clock():
        def fget(self):
            return self._clock
        def fset(self, value):
            self._clock = value
        return locals()
    clock = property(**clock())

    def weather():
        def fget(self):
            return self._weather
        def fset(self, value):
            self._weather = value
        return locals()
    weather = property(**weather())

    def email():
        def fget(self):
            return self._email
        def fset(self, value):
            self._email = value
        return locals()
    email = property(**email())

    def calendar():
        def fget(self):
            return self._calendar
        def fset(self, value):
            self._calendar = value
        return locals()
    calendar = property(**calendar())

    def music():
        def fget(self):
            return self._music
        def fset(self, value):
            self._music = value
        return locals()
    music = property(**music())
    
    def getName(self):
        warnings.warn(
            "You should be using 'username' instead of 'getName()''",
            DeprecationWarning
        )
        return self.username
    
    #Name, Start Time, End Time
    #Integer start and end times only, military time
    def getCalendarEvents(self):
        import mirrorbackend
        res = mirrorbackend.getcalendar(self.id)
        return res
        #return [("IED Class", 9,12),("Multivariable", 12,13),("Colorguard Practice", 19,21)]
    
    def getEmails(self):
        return [("Mailsvs-l@lists.rpi.edu", "RPI Student PACKAGE RECEIPT NOTICE", "Dear Pybus, Christopher William, Your package has arrived at RPI! Please retrieve your package at the student"),
                ("Abigail Agosto", "RE: CMADD RFF", "Good afternoon MIDN Pybus, The CMADD Party RFF was approved for up to $85. Attached is the edited RFF with."),
                ("Matt Gerrard", "[navyship] POW 4 APR 2016", "Ships Company, Attached is the POW for this upcoming week. Very respectfully, MIDN 3C Gerrard OPS SCPO"),
                ("Morning Mail", "Morning Mail 04-07-2016", "Morning Mail is the official news and announcements sharing service of Rensselaer Polytechnic Institute"),
                ("William Ash", "[navyship] Ships Company Data", "Ships Company, This year is coming to a close and we would like to collect data on what each MIDN did throughout")]
        
    
    def verifyPasscode(self, passcode):
        if(passcode == self.passcode):
            return True;
        else:
            return False;
        
    def displayClock(self):
        return self.clock
        
    def displayWeather(self):
        return self.weather
    
    def displayEmail(self):
        return self.email
    
    def displayCalendar(self):
        return self.calendar
    
    def displayMusic(self):
        return self.music
