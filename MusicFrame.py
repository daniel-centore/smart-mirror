'''
Created on Apr 21, 2016

@author: cwpyb
'''
from tkinter import *
import HelperMethods
import sched, time

class MusicFrame(Frame):
    
    def __init__(self, title, master=None):
        Frame.__init__(self, width=400, height=250, bg="black")
        
        self.arrow = PhotoImage(file="./smallarrow.gif")
        self.arrowLabel = Label(self, image='', anchor=W, bg="black")
        self.arrowLabel.place(x=0, y=30, height=30, width=60)
        
        self.playlistAndSongs = StringVar()
        self.playlistAndSongs.set("Playlists")
        Label(self, textvariable=self.playlistAndSongs, font=("SFNS Display Bold", 16), bg="black", foreground="white" ).place(x=30, y=0)
        
        self.labelTexts = []
        for num in range(0,5):
            self.labelTexts.append( StringVar())
            self.labelTexts[num].set("")
            Label(self, textvariable=self.labelTexts[num], font=("SFNS Display", 14), bg="black", foreground="white" ).place(x=30, y=30+(num*25))
        
        
        #Currently Playing
        self.currentlyPlayingTitle = StringVar()
        self.currentlyPlayingTitle.set("Currently Playing")
        Label(self, textvariable=self.currentlyPlayingTitle, font=("SFNS Display Bold", 16), bg="black", foreground="white" ).place(x=30, y=180)
        self.currentlyPlaying = StringVar()
        self.currentlyPlaying.set("Nothing")
        Label(self, textvariable=self.currentlyPlaying, font=("SFNS Display", 14), bg="black", foreground="white" ).place(x=30, y=210)
        
        self.currentPos = 0;
        
    
    def updateForUser(self, user):
        self.currentPos = 0
        self.playlists = user.getPlaylists()
        self.playlists.insert(0, u"\u2190 Exit music")
        self.current_list = self.playlists
        self.updateScreen()
        self.keepUpdating = True
        self.currentuser = user
        self.after(1000, self.handle_updates)
        
    def handle_updates(self):
        if not self.keepUpdating:
            return
        
        self.updatePlaying()
        self.after(1000, self.handle_updates)
        
        
    def clearMusic(self):
        self.keepUpdating = False
        
        self.currentPos = 0;
        for widget in self.winfo_children():
            widget.destroy()
        self.arrow = PhotoImage(file="./smallarrow.gif")
        self.arrowLabel = Label(self, image='', anchor=W, bg="black")
        self.arrowLabel.place(x=0, y=30, height=30, width=60)
        
        self.playlistAndSongs = StringVar()
        self.playlistAndSongs.set("Playlists")
        Label(self, textvariable=self.playlistAndSongs, font=("SFNS Display Bold", 16), bg="black", foreground="white" ).place(x=30, y=0)
        
        self.labelTexts = []
        for num in range(0,5):
            self.labelTexts.append( StringVar())
            self.labelTexts[num].set("")
            Label(self, textvariable=self.labelTexts[num], font=("SFNS Display", 14), bg="black", foreground="white" ).place(x=30, y=30+(num*25))
        
        # Currently Playing
        self.currentlyPlayingTitle = StringVar()
        self.currentlyPlayingTitle.set("Currently Playing")
        Label(self, textvariable=self.currentlyPlayingTitle, font=("SFNS Display Bold", 16), bg="black", foreground="white" ).place(x=30, y=180)
        self.currentlyPlaying = StringVar()
        self.currentlyPlaying.set("Nothing")
        Label(self, textvariable=self.currentlyPlaying, font=("SFNS Display", 14), bg="black", foreground="white" ).place(x=30, y=210)
    
    def reload(self):
        self.arrowLabel.config(image=self.arrow)
            
    def moveArrowDown(self):
        if(self.currentPos + 1 < len(self.current_list)):
            self.currentPos = self.currentPos + 1;
        else:
            self.currentPos = 0;
        self.updateScreen()
    
    def moveArrowUp(self):
        if self.currentPos > 0:
            self.currentPos -= 1
        else:
            self.currentPos = len(self.current_list) - 1;
        self.updateScreen()
     
    def select(self, user):
        if(self.playlistAndSongs.get() == "Playlists"):
            if self.currentPos == 0:
                self.arrowLabel.config(image='')
                return False
            
            self.playlistAndSongs.set("Songs")
            self.currentPlaylist = self.playlists[self.currentPos]
            # print("Selected playlist: %s" % self.currentPlaylist)
            self.songs = user.getSongs(self.currentPlaylist)
            
            self.songlist = [u"\u2190 Playlists", "== Shuffle =="]
            for song in self.songs:
                self.songlist.append(song['title'])
            
            self.current_list = self.songlist
            self.currentPos = 0
            self.updateScreen()
        elif(self.playlistAndSongs.get() == "Songs"):
            if self.currentPos == 0:
                self.playlistAndSongs.set("Playlists")
                self.current_list = self.playlists
                self.currentPlaylist = ""
                self.updateScreen()
                return True
            elif self.currentPos == 1:
                user.shuffleplaylist(self.currentPlaylist)
                # self.updatePlaying()
                return True
            
            currentTitle = self.songlist[self.currentPos]
            for song in self.songs:
                if(song.get("title") == currentTitle):
                    user.playSong(self.currentPlaylist, song)
                    # self.updatePlaying()
        return True
    def updateScreen(self):
        SHOW_ITEMS = 5
        
        import math
        startpos = self.currentPos - int(math.floor(SHOW_ITEMS / 2))
        startpos = max(startpos, 0)
        startpos = min(startpos, len(self.current_list) - SHOW_ITEMS)
        startpos = max(startpos, 0)
        
        self.arrowLabel.place(y=30+(((self.currentPos - startpos)*25)), x=0)
        
        for num in range(0, SHOW_ITEMS):
            self.labelTexts[num].set("")
        for num in range(0, min(SHOW_ITEMS, len(self.current_list))):
            self.labelTexts[num].set(self.current_list[startpos + num])
        
    def startPause(self, user):
        user.pause()
        
    def nextSong(self, user):
        user.skip()
        # self.updatePlaying()
        
    def updatePlaying(self):
        song = self.currentuser.currentsong()
        if len(song) == 0:
            return
        # curr = "%s - %s" % (song.get("title"), song.get("artist"))
        curr = song.get("title")
        self.currentlyPlaying.set(curr)
