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

def makeUser(name, password, id):
    return _User(name, password, id)

'''
Shim for data access by the frontend
'''
class UserObject(object):
    
    def __init__(self, user, id):
        self.user = user
        # self._username = user.store.name
        # self._passcode = user.store.password
        # self._clock = user.store.clock
        # self._weather = user.store.weather
        # self._email = user.store.email
        # self._calendar = user.store.calendar
        # self._music = user.store.music
        self.id = id
    
    # TODO MAKE THESE UPDATE THE STORE
    def username():
        def fget(self):
            return self.user.store.name
        def fset(self, value):
            self.user.store.name = value
            import mirrorbackend
            mirrorbackend._savedata()
        return locals()
    username = property(**username())
    
    def passcode():
        def fget(self):
            return self.user.store.password
        def fset(self, value):
            self.user.store.password = value
            import mirrorbackend
            mirrorbackend._savedata()
        return locals()
    passcode = property(**passcode())
    
    def clock():
        def fget(self):
            return self.user.store.clock
        def fset(self, value):
            self.user.store.clock = value
            import mirrorbackend
            mirrorbackend._savedata()
        return locals()
    clock = property(**clock())

    def weather():
        def fget(self):
            return self.user.store.weather
        def fset(self, value):
            self.user.store.weather = value
            import mirrorbackend
            mirrorbackend._savedata()
        return locals()
    weather = property(**weather())

    def email():
        def fget(self):
            return self.user.store.email
        def fset(self, value):
            self.user.store.email = value
            import mirrorbackend
            mirrorbackend._savedata()
        return locals()
    email = property(**email())

    def calendar():
        def fget(self):
            return self.user.store.calendar
        def fset(self, value):
            self.user.store.calendar = value
            import mirrorbackend
            mirrorbackend._savedata()
        return locals()
    calendar = property(**calendar())

    def music():
        def fget(self):
            return self.user.store.music
        def fset(self, value):
            self.user.store.music = value
            import mirrorbackend
            mirrorbackend._savedata()
        return locals()
    music = property(**music())
    
    def getName(self):
        return self.username
    
    def changePasscode(self, passcode):
		self.passcode = passcode;
    
    #Name, Start Time, End Time
    #Integer start and end times only, military time
    def getCalendarEvents(self):
        import mirrorbackend
        res = mirrorbackend.getcalendar(self.id)
        return res
        #return [("IED Class", 9,12),("Multivariable", 12,13),("Colorguard Practice", 19,21)]
    
    def getEmails(self):
        import mirrorbackend
        source = mirrorbackend.getemail(self.id)[:5]
        res = []
        for s in source:
            res.append((s['sender'], s['subject'], s['snippet']))
        return res
        
    
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

    def getPlaylists(self):
        import mirrorbackend
        return mirrorbackend.listplaylists(self.id)
    
    def getSongs(self, playlist):
        import mirrorbackend
        return mirrorbackend.listsongs(self.id, playlist)
      
    #Will return the entire song object noted above
    def playSong(self, playlist, songObject):
        import mirrorbackend
        mirrorbackend.playsong(self.id, playlist, songObject['file'])
    
    def pause(self):
        import mirrorbackend
        mirrorbackend.pause(self.id)
        
    def skip(self):
        import mirrorbackend
        mirrorbackend.next(self.id)
    
    def shuffleplaylist(self, playlist):
        import mirrorbackend
        mirrorbackend.shuffleplaylist(self.id, playlist)
    
    def currentsong(self):
        import mirrorbackend
        return mirrorbackend.currentsong(self.id)

    def logout(self):
        import mirrorbackend
        mirrorbackend.stop(self.id)
