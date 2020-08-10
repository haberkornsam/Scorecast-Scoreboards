from tkinter import *
from threading import *
from socket import *
from time import *
import os


yellowColor='#dbcf30'

overlayWindowWidth = 1280
overlayWindowHeight = 120

teamFrameWidth = 200
scoreFrameWidth = 60
periodFrameWidth = 110
timeFrameWidth = 144


teamsHeight = 35
extrasHeight = 15
possBarHeight = 3

overlayWidth=((teamFrameWidth+scoreFrameWidth)*2)+periodFrameWidth+timeFrameWidth
overlayHeight = teamsHeight+extrasHeight

homeTeamx = (overlayWindowWidth/2)-(overlayWidth/2)
homeScorex = homeTeamx + teamFrameWidth
awayTeamx=homeScorex+scoreFrameWidth
awayScorex = awayTeamx + teamFrameWidth
periodFramex = awayScorex+scoreFrameWidth
timeFramex = periodFramex+periodFrameWidth

centerLine = (overlayWindowHeight/2)

homeFoulxOverlay=teamFrameWidth+(scoreFrameWidth/2)
homeBonusxOverlay=homeFoulxOverlay-scoreFrameWidth
awayFoulxOverlay=homeFoulxOverlay+teamFrameWidth+scoreFrameWidth
awayBonusxOverlay=awayFoulxOverlay-scoreFrameWidth


extrasY = (extrasHeight/2)-1

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


fFont = resource_path("Futura.ttc")
#fFont = "futura"


class StopWatchbballoverlay(Frame):
    """ Implements a stop watch frame widget. """

    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._startingTime = 1080
        self._elapsedtime = 0.0
        self._running = 0
        self._minutes = 0
        self._seconds = 0
        self.timestr = StringVar()
        self.timeString = ''
        self.makeWidgets()

    def makeWidgets(self):
        global l
        """ Make the time label. """
        l = Label(self, text=self.timeString, bg='#000000')
        self._setTime(self._elapsedtime)
        l.config(font=(fFont, 22), fg = '#dbcf30')
        l.place(x=72, y=17, anchor='c')


    def _update(self):
        global clockFile
        """ Update the label with elapsed time. """
        self._elapsedtime = time() - self._start
        self._setTime(self._elapsedtime)

        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        newTime = self._startingTime-elap
        if newTime <=0:
            newTime = 0
        minutes = int(newTime / 60)
        seconds = int(newTime - minutes * 60.0)
        hseconds = int((newTime - minutes * 60.0 - seconds) * 10)

        self._minutes = str(minutes).zfill(2)
        self._seconds = str(seconds).zfill(2)+"."+str(hseconds).zfill(1)

        if minutes == 0:
            formatted = str(seconds).zfill(2)+"."+str(hseconds).zfill(1)
            format = str(seconds)+"."+str(hseconds).zfill(1)
        else:
            formatted = str(minutes).zfill(2)+":"+str(seconds).zfill(2)+"."+str(hseconds).zfill(1)
            format = str(minutes) + ":" + str(seconds).zfill(2)

        self.timeString = formatted
        l.configure(text=format)

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        """ Reset the stopwatch. """
        self._start = time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)

    def setClock(self, newTimeM, newTimeS):

        self._elapsedtime=0.0
        self._running=0
        self._startingTime=0
        try:
            self._startingTime = float(newTimeM)*60
        except ValueError:
            pass

        try:
            self._startingTime += float(newTimeS)
        except ValueError:
            pass

        self._start = time()
        self._setTime(self._elapsedtime)
        self.update()

    def getClockTime(self):
        return self._startingTime-self._elapsedtime


    def getMinutes(self):
        return self._minutes
    def getSeconds(self):
        return self._seconds




class Receive(Thread):
    def __init__(self, server, app):
        Thread.__init__(self)
        self.server = server
        self.app = app

    def run(self):
        while 1:
            try:
                text = self.recevieData()
                recvText=text[0]
                if not recvText: break
                if recvText == 'Start':
                    self.app.startClock()
                elif recvText == 'Stop':
                    self.app.stopClock()
                    self.app.changeTime(text[1], text[2])
                elif recvText == 'ChangeTime':
                    self.timeM = text[1]
                    self.timeS = text[2]
                    self.app.changeTime(self.timeM, self.timeS)
                elif recvText == 'homeTeam':
                    self.app.changeHTeam(text[1])
                elif recvText == 'awayTeam':
                    self.app.changeATeam(text[1])
                elif recvText == 'homeScore':
                    self.app.changeHomeScore(text[1])
                elif recvText == 'awayScore':
                    self.app.changeAwayScore(text[1])
                elif recvText == 'homeFouls':
                    self.app.changeHomeFouls(text[1])
                elif recvText == 'awayFouls':
                    self.app.changeAwayFouls(text[1])
                elif recvText == 'half':
                    self.app.changeHalf(text[1])
                elif recvText == 'homeTO':
                    self.app.changeHomeFullTO(text[2])
                    self.app.changeHomePartTO(text[1])
                elif recvText == 'awayTO':
                    self.app.changeAwayFullTO(text[2])
                    self.app.changeAwayPartTO(text[1])
                elif recvText == 'homePrimary':
                    self.app.changeHP(text[1])
                elif recvText == 'homeSecondary':
                    self.app.changeHS(text[1])
                elif recvText == 'awayPrimary':
                    self.app.changeAP(text[1])
                elif recvText == 'awaySecondary':
                    self.app.changeAS(text[1])
                elif recvText == 'poss':
                    self.app.changePoss(text[1], text[2])
                elif recvText == 'sync':
                    self.app.changeHTeam(text[1])
                    self.app.changeATeam(text[2])
                    self.app.changeHomeScore(text[3])
                    self.app.changeAwayScore(text[4])
                    self.app.changeAwayFouls(text[5])
                    self.app.changeHomeFouls(text[6])
                    self.app.changeHalf(text[7])
                    self.app.changeHomePartTO(text[8])
                    self.app.changeAwayPartTO(text[9])
                    self.app.changeHomeFullTO(text[10])
                    self.app.changeAwayFullTO(text[11])
                    self.app.changeHP(text[12])
                    self.app.changeHS(text[13])
                    self.app.changeAP(text[14])
                    self.app.changeAS(text[15])
                    self.app.changeTime(text[16], text[17])
                    self.app.changePoss(text[18], text[19])


            except:
                break

    def recevieData(self):
        global clients
        datum = ""
        while True:
            datum = self.server.recv(256)
            datum = datum.decode('utf-8')
            if datum[0]=='~':
                for cli in clients:
                    if cli != self.server:
                        try:
                            cli.sendall(datum.encode())
                        except:
                            pass
                datum = datum[1:]
                data = datum.split('`')
                return data[:-1]
            else:
                break

class App(Thread):


    def startClock(self):
        global runnin
        runnin = 'Stop'
        self.swbballoverlay.Start()

    def stopClock(self):
        global runnin
        runnin = 'Start'
        self.swbballoverlay.Stop()

    def changeTime(self, timeM, timeS):
        global runnin
        runnin='Start'
        self.swbballoverlay.Stop()
        self.swbballoverlay.setClock(float(timeM), float(timeS))

    def changeHTeam(self, newName):
        global homeTeam
        homeTeam = newName
        self.homeTeambballoverlay.configure(text=homeTeam)
        self.homeTeambballoverlay.update()

    def changeATeam(self, newName):
        global awayTeam
        awayTeam = newName
        self.awayTeambballoverlay.configure(text=awayTeam)
        self.awayTeambballoverlay.update()

    def changeHomeScore(self, newScore):
        global homeScore
        homeScore = int(newScore)
        self.homeScorebballoverlay.configure(text=homeScore)
        self.homeScorebballoverlay.update()

    def changeAwayScore(self, newScore):
        global awayScore
        awayScore = int(newScore)
        self.awayScorebballoverlay.configure(text=awayScore)
        self.awayScorebballoverlay.update()

    def changeHomeFouls(self, newFouls):
        global hFouls, awayBonusState
        hFouls=int(newFouls)
        if hFouls >= 7 and hFouls < 10:
            awayBonusState = 'BONUS'
            self.homeFoulsbballoverlay.config(text='Fouls: '+str(hFouls))
            self.homeFoulsbballoverlay.update()
        if hFouls >= 10:
            awayBonusState = 'BONUS+'
            self.homeFoulsbballoverlay.config(text='')
            self.homeFoulsbballoverlay.update()
        if hFouls < 7:
            awayBonusState = ''
            self.homeFoulsbballoverlay.config(text='Fouls: '+str(hFouls))
            self.homeFoulsbballoverlay.update()
        self.aBonusbballoverlay.configure(text=awayBonusState)
        self.aBonusbballoverlay.update()

    def changeAwayFouls(self, newFouls):
        global aFouls, homeBonusState
        aFouls = int(newFouls)
        if aFouls >= 7 and aFouls < 10:
            homeBonusState = 'BONUS'
            self.awayFoulsbballoverlay.configure(text='Fouls: '+str(aFouls))
            self.awayFoulsbballoverlay.update()
        if aFouls >= 10:
            homeBonusState = 'BONUS+'
            self.awayFoulsbballoverlay.configure(text='')
            self.awayFoulsbballoverlay.update()
        if aFouls < 7:
            homeBonusState = ''
            self.awayFoulsbballoverlay.configure(text='Fouls: '+str(aFouls))
            self.awayFoulsbballoverlay.update()
        self.hBonusbballoverlay.configure(text=homeBonusState)
        self.hBonusbballoverlay.update()

    def changeHalf(self, newHalf):
        global half
        half = newHalf
        self.halfbballoverlay.configure(text=str(half))
        self.halfbballoverlay.update()

    def changePoss(self, hPoss, aPoss):
        global homePoss, awayPoss
        homePoss = hPoss
        awayPoss = aPoss
        if homePoss == "True":
            self.homePossBar.configure(bg=yellowColor)
            self.homePossBar.update()
        else:
            self.homePossBar.configure(bg=homeSecondColor)
            self.homePossBar.update()

        if awayPoss == "True":
            self.awayPossBar.config(bg=yellowColor)
            self.awayPossBar.update()
        else:
            self.awayPossBar.configure(bg=awaySecondColor)
            self.awayPossBar.update()

    def changeHomeFullTO(self, newTO):
        global homeFullTO
        homeFullTO = int(newTO)
        self.homeTOUpdate()

    def changeAwayFullTO(self, newTO):
        global awayFullTO
        awayFullTO = int(newTO)
        self.awayTOUpdate()

    def changeHomePartTO(self, newTO):
        global homePartTO
        homePartTO = int(newTO)
        self.homeTOUpdate()

    def changeAwayPartTO(self, newTO):
        global awayPartTO
        awayPartTO = int(newTO)
        self.awayTOUpdate()

    def homeTOUpdate(self):
        global homeFullTO, homePartTO
        combTO = int(homeFullTO) + int(homePartTO)

        for i in range(totalTO):
            if(i<combTO):
                self.homeTOFrames[i].configure(bg='#ffffff')
            else:
                self.homeTOFrames[i].configure(bg='#3c3f41')

    def awayTOUpdate(self):
        global awayFullTO, awayPartTO
        combTO = int(awayFullTO)+int(awayPartTO)

        for i in range(totalTO):
            if(i<combTO):
                self.awayTOFrames[i].configure(bg='#ffffff')
            else:
                self.awayTOFrames[i].configure(bg='#3c3f41')



    def changeHP(self, newColor):
        global homePrimaryColor
        homePrimaryColor=newColor
        self.homeFrame.configure(bg=homePrimaryColor)
        self.homeTeambballoverlay.configure(bg=homePrimaryColor)

    def changeHS(self, newColor):
        global homeSecondColor
        homeSecondColor=newColor
        self.homeScoreFrame.configure(bg=homeSecondColor)
        self.homeScorebballoverlay.configure(bg = homeSecondColor)

    def changeAP(self, newColor):
        global awayPrimaryColor
        awayPrimaryColor=newColor
        self.awayFrame.configure(bg=awayPrimaryColor)
        self.awayTeambballoverlay.configure(bg = awayPrimaryColor)

    def changeAS(self, newColor):
        global awaySecondColor
        awaySecondColor=newColor
        self.awayScoreFrame.configure(bg=awaySecondColor)
        self.awayScorebballoverlay.configure(bg = awaySecondColor)



    def __init__(self, master, port, data):

        Thread.__init__(self)

        self.homeFrame=Frame(master)
        self.homeFrame.configure(bg=homePrimaryColor, width=teamFrameWidth, height=teamsHeight)
        self.homeFrame.place(x=homeTeamx, y=centerLine, anchor='sw')  # 293.33

        self.homeScoreFrame=Frame(master)
        self.homeScoreFrame.configure(bg=homeSecondColor, width=scoreFrameWidth, height=teamsHeight)
        self.homeScoreFrame.place(x=homeScorex, y=centerLine, anchor='sw')

        self.awayFrame=Frame(master)
        self.awayFrame.configure(bg=awayPrimaryColor, width=teamFrameWidth, height=teamsHeight)
        self.awayFrame.place(x=awayTeamx, y=centerLine, anchor='sw')

        self.awayScoreFrame=Frame(master)
        self.awayScoreFrame.configure(bg=awaySecondColor, width=scoreFrameWidth, height=teamsHeight)
        self.awayScoreFrame.place(x=awayScorex, y=centerLine, anchor='sw')

        self.periodFrame=Frame(master)
        self.periodFrame.configure(bg='#000000', width=periodFrameWidth, height=teamsHeight)
        self.periodFrame.place(x=periodFramex, y=centerLine, anchor='sw')

        self.swbballoverlay = StopWatchbballoverlay(master)
        self.swbballoverlay.configure(bg='#000000', width=timeFrameWidth, height=teamsHeight)
        self.swbballoverlay.place(x=timeFramex, y=centerLine, anchor='sw')

        self.swbballoverlay.setClock(float(data[19]), float(data[20]))

        self.foulFrame = Frame(master)
        self.foulFrame.configure(bg='#000000', width=overlayWidth, height=extrasHeight)  # '#473c34'
        self.foulFrame.place(x=homeTeamx, y=centerLine, anchor='nw')




        self.homeScorebballoverlay = Label(self.homeScoreFrame, text=homeScore)
        self.homeScorebballoverlay.place(x=scoreFrameWidth/2, y=((teamsHeight+possBarHeight)/2), anchor='c')
        self.homeScorebballoverlay.config(font=(fFont, 27), fg='#ffffff', bg = homeSecondColor)

        self.homePossBar=Frame(self.homeScoreFrame)
        self.homePossBar.config(bg=homeSecondColor, width=scoreFrameWidth, height=possBarHeight)
        self.homePossBar.place(x=0, y=0, anchor='nw')
        if (homePoss=='True'):
            self.homePossBar.config(bg=yellowColor)

        self.awayScorebballoverlay = Label(self.awayScoreFrame, text=awayScore)
        self.awayScorebballoverlay.place(x=scoreFrameWidth/2, y=((teamsHeight+possBarHeight)/2), anchor='c')
        self.awayScorebballoverlay.config(font=(fFont, 27), fg='#ffffff', bg = awaySecondColor)

        self.awayPossBar=Frame(self.awayScoreFrame)
        self.awayPossBar.configure(bg=awaySecondColor, width=scoreFrameWidth, height=possBarHeight)
        self.awayPossBar.place(x=0, y=0, anchor='nw')
        if (awayPoss=='True'):
            self.awayPossBar.config(bg=yellowColor)


        self.homeTeambballoverlay = Label(self.homeFrame, text=homeTeam)
        self.homeTeambballoverlay.place(x=20, y=teamsHeight/2, anchor='w')
        self.homeTeambballoverlay.config(font=(fFont, 18), fg='#ffffff', bg = homePrimaryColor)

        self.awayTeambballoverlay = Label(self.awayFrame, text=awayTeam)
        self.awayTeambballoverlay.place(x=20, y=teamsHeight/2, anchor='w')
        self.awayTeambballoverlay.config(font=(fFont, 18), fg='#ffffff', bg = awayPrimaryColor)

        self.homeFoulsbballoverlay = Label(self.foulFrame, text='Fouls: '+str(hFouls), fg='#ffffff')
        self.homeFoulsbballoverlay.place(x=homeFoulxOverlay, y=extrasY, anchor='c')
        self.homeFoulsbballoverlay.config(font=(fFont, 12), fg='#ffffff', bg = '#000000')

        self.awayFoulsbballoverlay = Label(self.foulFrame, text='Fouls: '+str(aFouls))
        self.awayFoulsbballoverlay.place(x=awayFoulxOverlay, y=extrasY, anchor='c')
        self.awayFoulsbballoverlay.config(font=(fFont, 12), fg='#ffffff', bg='#000000')

        self.halfbballoverlay = Label(self.periodFrame, text=half)
        self.halfbballoverlay.place(x=20, y=teamsHeight/2, anchor='w')
        self.halfbballoverlay.config(font=(fFont, 20), fg='#ffffff', bg='#000000')


        self.hBonusbballoverlay = Label(self.foulFrame, text=homeBonusState)
        self.hBonusbballoverlay.place(x=homeBonusxOverlay, y=extrasY, anchor='c')
        self.hBonusbballoverlay.config(font=(fFont, 12), fg='#dbcf30', bg='#000000')

        self.aBonusbballoverlay = Label(self.foulFrame, text=awayBonusState)
        self.aBonusbballoverlay.place(x=awayBonusxOverlay, y=extrasY, anchor='c')
        self.aBonusbballoverlay.config(font=(fFont, 12), fg='#dbcf30', bg='#000000')

        toBarWidth=((teamFrameWidth-scoreFrameWidth)/totalTO)-5

        if toBarWidth >35:
            toBarWidth = 35

        homeTOBarStart = ((teamFrameWidth-scoreFrameWidth)/2)-((toBarWidth+3)*(totalTO/2))

        self.homeTOFrames = []

        for i in range(totalTO):
            toBar = Frame(self.foulFrame)
            toBar.config(width = toBarWidth, height = possBarHeight)
            if i<homeFullTO+homePartTO:
                toBar.configure(bg='#ffffff')
            else:
                toBar.configure(bg='#3C3F41')
            toBar.place(x=homeTOBarStart+((toBarWidth+5)*i), y=extrasY, anchor='w')
            self.homeTOFrames.append(toBar)

        awayToBarStart = homeTOBarStart+teamFrameWidth+scoreFrameWidth+2

        self.awayTOFrames = []

        for i in range(totalTO):
            toBar = Frame(self.foulFrame)
            toBar.config(width = toBarWidth, height = possBarHeight)
            if i<awayFullTO+awayPartTO:
                toBar.configure(bg='#ffffff')
            else:
                toBar.configure(bg='#3C3F41')
            toBar.place(x=awayToBarStart+((toBarWidth+5)*i), y=extrasY, anchor='w')
            self.awayTOFrames.append(toBar)




        #self.addr = '127.0.0.1'
        self.addr = ''
        self.serverRun = True
        self.port = port





    def sendConfigData(self, client):
        data = '~basketball`'
        data += str(homeTeam)+'`'
        data += str(awayTeam)+'`'
        data += str(homeScore)+'`'
        data += str(awayScore)+'`'
        data += str(hFouls)+'`'
        data += str(aFouls)+'`'
        data += str(homeBonusState)+'`'
        data += str(awayBonusState)+'`'
        data += str(half)+'`'
        data += str(homePoss)+'`'
        data += str(awayPoss)+'`'
        data += str(homePartTO)+'`'
        data += str(homeFullTO)+'`'
        data += str(awayPartTO)+'`'
        data += str(awayFullTO)+'`'
        data += str(homePrimaryColor)+'`'
        data += str(homeSecondColor)+'`'
        data += str(awayPrimaryColor)+'`'
        data += str(awaySecondColor)+'`'
        data += str(self.swbballoverlay.getMinutes())+'`'
        data += str(self.swbballoverlay.getSeconds())+'`'
        data += str(homePoss)+'`'
        data += str(awayPoss)+'`'
        data += str(totalTO)+'`'
        client.sendall(data.encode())







    def run(self):
        global clients
        clients = []
        if self.serverRun == True:
            #if self.addr == '127.0.0.1':
            if self.addr == '':
                server = socket(AF_INET, SOCK_STREAM)
                server.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
                server.bind((self.addr, self.port))
                server.listen(5)
                while(1):
                    self.client, self.addr = server.accept()
                    clients.append(self.client)
                    #print("clientConnected")
                    self.sendConfigData(self.client)
                    Receive(self.client, self).start()
        else:
            server = socket()
            server.bind((self.addr, int(self.port)))

    def stopServe(self):
        global server
        from lib import basketballStandalone
        #stop clock here
        data = []
        data.append(homeTeam)
        data.append(awayTeam)
        data.append(homeScore)
        data.append(awayScore)
        data.append(hFouls)
        data.append(aFouls)
        data.append(homeBonusState)
        data.append(half)
        data.append(homePoss)
        data.append(awayPoss)
        data.append(homePartTO)
        data.append(homeFullTO)
        data.append(awayPartTO)
        data.append(awayFullTO)
        data.append(totalTO)
        data.append(homePrimaryColor)
        data.append(homeSecondColor)
        data.append(awayPrimaryColor)
        data.append(awaySecondColor)
        data.append(self.swbballoverlay.getMinutes())
        data.append(self.swbballoverlay.getSeconds())


def goMainMenu(event=None):
    overlay.destroy()
    #kill threads

def stopServer(ap):
    ap.stopServe()



def start(port, data):
    global runnin, homeTeam, awayTeam, homeScore, awayScore, hFouls, aFouls, homeBonusState, awayBonusState, half, \
        homePoss, awayPoss, homePartTO, homeFullTO, awayPartTo, awayFullTO, awayPartTO, homePrimaryColor, \
        homeSecondColor, awayPrimaryColor, awaySecondColor, control, controlApp, overlayApp, overlay, control, totalTO, \
        ipLabel
    runnin = 'Start'
    homeTeam = str(data[0])
    awayTeam = str(data[1])
    homeScore = int(data[2])
    awayScore = int(data[3])
    hFouls = int(data[4])
    aFouls = int(data[5])
    homeBonusState = str(data[6])
    awayBonusState = str(data[7])
    half = str(data[8])
    homePoss = str(data[9])
    awayPoss = str(data[10])
    homePartTO = int(data[11])
    homeFullTO = int(data[12])
    awayPartTO = int(data[13])
    awayFullTO = int(data[14])
    homePrimaryColor = str(data[15])
    homeSecondColor = str(data[16])
    awayPrimaryColor = str(data[17])
    awaySecondColor = str(data[18])
    totalTO = int(data[21])


    overlay = Tk()
    overlay.configure(bg='#00ff00')
    overlay.geometry('1280x120')
    overlay.title('Scorecast Basketball Scoreboard')

    overlayApp = App(overlay, port, data).start()

    try:
        ip = gethostbyname(gethostname())
    except:
        ip = 'Lookup ERROR'

#menubar
    menubar=Menu(overlay)
    fileMenu=Menu(menubar, tearoff=0)
    #fileMenu.add_command(label='Save Configuration', command=overlayApp.saveConfig)
    #fileMenu.add_command(label='Open Configuration', command=overlayApp.openConfig)
    fileMenu.add_separator()
    fileMenu.add_command(label='Quit', command=goMainMenu)

    serverMenu=Menu(menubar, tearoff=0)
    serverMenu.add_command(label='IP: '+ip, state='disabled')
    serverMenu.add_command(label='Port: '+str(port), state='disabled')
    serverMenu.add_separator()
    #serverMenu.add_command(label='Stop Server', command=overlayApp.stopServe)

    menubar.add_cascade(label='File', menu=fileMenu)
    menubar.add_cascade(label='Server', menu=serverMenu)
    overlay.config(menu=menubar)

    overlay.mainloop()


