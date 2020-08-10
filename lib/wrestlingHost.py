from tkinter import *
from threading import *
from socket import *
from time import *


fFont = "Lucida Grande"

matchScoreFrameSize = 55
teamFrameSize = 210 - matchScoreFrameSize
swOverlayWidth = 75

bottomy=60
hTeamScorex=240
homeFramex = hTeamScorex + matchScoreFrameSize
homeMatchScoreFrame=homeFramex + teamFrameSize

aTeamScorex = homeMatchScoreFrame + matchScoreFrameSize
awayFramex=aTeamScorex + matchScoreFrameSize
awayMatchScoreFrame = awayFramex + teamFrameSize

timeFramex=awayMatchScoreFrame+matchScoreFrameSize
swOverlayx=timeFramex+matchScoreFrameSize

weightFramex=swOverlayx+swOverlayWidth

class StopWatchwrestOverlay(Frame):
    """ Implements a stop watch frame widget. """

    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._startingTime = 120
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
        l.config(font=(fFont, 24), fg='#dbcf30')
        l.place(x=2,y=20, anchor='w')


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
                    if text[1]:
                        self.app.changeTime(text[1], text[2])
                elif recvText == 'ChangeTime':
                    self.app.changeTime(text[1], text[2])
                elif recvText == 'homeTeam':
                    self.app.changeHTeam(text[1]) #actually the wrestlersName
                elif recvText == 'awayTeam':
                    self.app.changeATeam(text[1]) #actually the wrestlers name
                elif recvText == 'homeScore':
                    self.app.changeHomeScore(text[1]) #match score
                elif recvText == 'awayScore':
                    self.app.changeAwayScore(text[1]) #match score
                elif recvText == 'hTeamScore':
                    self.app.changeHTeamScore(text[1])
                elif recvText == 'aTeamScore':
                    self.app.changeATeamScore(text[1])
                elif recvText == 'period':
                    self.app.changePeriod(text[1])
                elif recvText == 'homePrimary':
                    self.app.changeHP(text[1])
                elif recvText == 'homeSecondary':
                    self.app.changeHS(text[1])
                elif recvText == 'awayPrimary':
                    self.app.changeAP(text[1])
                elif recvText == 'awaySecondary':
                    self.app.changeAS(text[1])
                elif recvText == 'hAbrev':
                    self.app.changeHAbrev(text[1])
                elif recvText == 'aAbrev':
                    self.app.changeAAbrev(text[1])
                elif recvText == 'class':
                    self.app.changeWeightClass(text[1])
                elif recvText == 'sync':
                    self.app.changeHTeam(text[1])
                    self.app.changeATeam(text[2])
                    self.app.changeHomeScore(text[3])
                    self.app.changeAwayScore(text[4])
                    self.app.changeHTeamScore(text[5])
                    self.app.changeATeamScore(text[6])
                    self.app.changePeriod(text[7])
                    self.app.changeHP(text[8])
                    self.app.changeHS(text[9])
                    self.app.changeAP(text[10])
                    self.app.changeAS(text[11])
                    self.app.changeHAbrev(text[12])
                    self.app.changeAAbrev(text[13])
                    self.app.changeWeightClass(text[14])
                    self.app.stopClock()
                    self.app.changeTime(float(text[15]), float(text[16]))

            except:
                break

    def recevieData(self):
        global clients
        while True:
            datum = self.server.recv(256)
            datum = datum.decode('utf-8')
            if datum[0] == '~':
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
        self.swmaster.Start()

    def stopClock(self):
        global runnin
        runnin = 'Start'
        self.swmaster.Stop()

    def changeTime(self, timeM, timeS):
        global runnin
        runnin='Start'
        self.swmaster.Stop()
        self.swmaster.setClock(float(timeM), float(timeS))

    def changeHTeam(self, newName):
        global homeTeam
        homeTeam = newName
        self.homeTeammaster.configure(text=homeTeam)
        self.homeTeammaster.update()

    def changeATeam(self, newName):
        global awayTeam
        awayTeam = newName
        self.awayTeammaster.configure(text=awayTeam)
        self.awayTeammaster.update()

    def changeHomeScore(self, newScore):
        global homeScore
        homeScore = int(newScore)
        self.homeScoremaster.configure(text=homeScore)
        self.homeScoremaster.update()

    def changeAwayScore(self, newScore):
        global awayScore
        awayScore = int(newScore)
        self.awayScoremaster.configure(text=awayScore)
        self.awayScoremaster.update()

    def changeHTeamScore(self, newScore):
        global hTeamScore
        hTeamScore = int(newScore)
        self.hTeamScoreOverlay.configure(text=hTeamScore)
        self.hTeamScoreOverlay.update()

    def changeATeamScore(self, newScore):
        global aTeamScore
        aTeamScore = newScore
        self.aTeamScoreOverlay.configure(text=aTeamScore)
        self.aTeamScoreOverlay.update()

    def changePeriod(self, newPeriod):
        global half
        half = newPeriod
        self.halfmaster.configure(text = half)
        self.halfmaster.update()

    def changeHP(self, newColor):
        global homePrimaryColor
        homePrimaryColor = newColor
        self.homeFrame.configure(bg=homePrimaryColor)
        self.homeTeammaster.configure(bg = homePrimaryColor)

    def changeHS(self, newColor):
        global homeSecondColor
        homeSecondColor = newColor
        self.homeScoreFrame.configure(bg=homeSecondColor)
        self.homeScoremaster.configure(bg=homeSecondColor)

    def changeAP(self, newColor):
        global awayPrimaryColor
        awayPrimaryColor = newColor
        self.awayFrame.configure(bg=awayPrimaryColor)
        self.awayTeammaster.configure(bg=awayPrimaryColor)

    def changeAS(self, newColor):
        global awaySecondColor
        awaySecondColor = newColor
        self.awayScoreFrame.configure(bg=awaySecondColor)
        self.awayScoremaster.configure(bg=awaySecondColor)

    def changeHAbrev(self, newName):
        global hAbrev
        hAbrev = newName
        self.hTeamNameOverlay.configure(text=hAbrev)
        self.hTeamScoreOverlay.update()

    def changeAAbrev(self, newName):
        global aAbrev
        aAbrev = newName
        self.aTeamNameOverlay.configure(text=aAbrev)
        self.aTeamNameOverlay.update()

    def changeWeightClass(self, newClass):
        global weightClass
        weightClass = newClass
        self.weightOver.configure(text=weightClass)
        self.weightOver.update()

    def __init__(self, master, port, data):
        Thread.__init__(self)

        self.homeFrame = Frame(master)
        self.homeFrame.configure(bg=homePrimaryColor, width=teamFrameSize, height=40)
        self.homeFrame.place(x=homeFramex, y=bottomy, anchor='sw')  # 293.33

        self.homeScoreFrame = Frame(master)
        self.homeScoreFrame.configure(bg=homeSecondColor, width=matchScoreFrameSize, height=40)
        self.homeScoreFrame.place(x=homeMatchScoreFrame + matchScoreFrameSize, y=bottomy, anchor='se')

        self.awayFrame = Frame(master)
        self.awayFrame.configure(bg=awayPrimaryColor, width=teamFrameSize, height=40)
        self.awayFrame.place(x=awayFramex, y=bottomy, anchor='sw')

        self.awayScoreFrame = Frame(master)
        self.awayScoreFrame.configure(bg=awaySecondColor, width=matchScoreFrameSize, height=40)
        self.awayScoreFrame.place(x=awayMatchScoreFrame + matchScoreFrameSize, y=bottomy, anchor='se')

        self.hTeamScoreFrame = Frame(master)
        self.hTeamScoreFrame.config(bg=homeSecondColor, width=matchScoreFrameSize, height=40)
        self.hTeamScoreFrame.place(x=hTeamScorex, y=bottomy, anchor='sw')

        self.aTeamScoreFrame = Frame(master)
        self.aTeamScoreFrame.config(bg=awaySecondColor, width=matchScoreFrameSize, height=40)
        self.aTeamScoreFrame.place(x=aTeamScorex, y=bottomy, anchor='sw')

        self.hTeamScoreOverlay = Label(self.hTeamScoreFrame, text=hTeamScore)
        self.hTeamScoreOverlay.place(x=(matchScoreFrameSize / 2), y=40, anchor='s')
        self.hTeamScoreOverlay['bg'] = self.hTeamScoreOverlay.master['bg']
        self.hTeamScoreOverlay.config(font=(fFont, 17), fg=yellowColor)

        self.hTeamNameOverlay = Label(self.hTeamScoreFrame, text=hAbrev)
        self.hTeamNameOverlay.place(x=(matchScoreFrameSize / 2), y=0, anchor='n')
        self.hTeamNameOverlay['bg'] = self.hTeamNameOverlay.master['bg']
        self.hTeamNameOverlay.config(font=(fFont, 11), fg='#ffffff')

        self.aTeamScoreOverlay = Label(self.aTeamScoreFrame, text=aTeamScore)
        self.aTeamScoreOverlay.place(x=(matchScoreFrameSize / 2), y=40, anchor='s')
        self.aTeamScoreOverlay['bg'] = self.aTeamScoreOverlay.master['bg']
        self.aTeamScoreOverlay.config(font=(fFont, 17), fg=yellowColor)

        self.aTeamNameOverlay = Label(self.aTeamScoreFrame, text=aAbrev)
        self.aTeamNameOverlay.place(x=(matchScoreFrameSize / 2), y=0, anchor='n')
        self.aTeamNameOverlay['bg'] = self.aTeamNameOverlay.master['bg']
        self.aTeamNameOverlay.config(font=(fFont, 11), fg='#ffffff')

        self.homeScoremaster = Label(self.homeScoreFrame, text=homeScore)
        self.homeScoremaster.place(x=(matchScoreFrameSize / 2), y=20, anchor='c')
        self.homeScoremaster['bg'] = self.homeScoremaster.master['bg']
        self.homeScoremaster.config(font=(fFont, 29), fg='#ffffff')

        self.awayScoremaster = Label(self.awayScoreFrame, text=awayScore)
        self.awayScoremaster.place(x=(matchScoreFrameSize / 2), y=20, anchor='c')
        self.awayScoremaster['bg'] = self.awayScoremaster.master['bg']
        self.awayScoremaster.config(font=(fFont, 29), fg='#ffffff')

        self.homeTeammaster = Label(self.homeFrame, text=homeTeam)
        self.homeTeammaster.place(x=10, y=21, anchor='w')
        self.homeTeammaster['bg'] = self.homeTeammaster.master['bg']
        self.homeTeammaster.config(font=(fFont, 16), fg='#ffffff')

        self.awayTeammaster = Label(self.awayFrame, text=awayTeam)
        self.awayTeammaster.place(x=10, y=21, anchor='w')
        self.awayTeammaster['bg'] = self.awayTeammaster.master['bg']
        self.awayTeammaster.config(font=(fFont, 16), fg='#ffffff')

        self.swmaster = StopWatchwrestOverlay(master)
        self.swmaster.configure(bg='#000000', width=swOverlayWidth, height=40)
        self.swmaster.place(x=swOverlayx, y=bottomy, anchor='sw')
        self.swmaster.setClock(float(data[14]), float(data[15]))

        self.timeFrame = Frame(master)
        self.timeFrame.configure(bg='#000000', width=matchScoreFrameSize, height=40)
        self.timeFrame.place(x=timeFramex, y=bottomy, anchor='sw')

        self.halfmaster = Label(self.timeFrame, text=half)
        self.halfmaster.place(x=26, y=20, anchor='c')
        self.halfmaster['bg'] = self.halfmaster.master['bg']
        self.halfmaster.config(font=(fFont, 20), fg='#ffffff')

        self.weightFrame = Frame(master)
        self.weightFrame.config(bg='#000000', width=86, height=40)
        self.weightFrame.place(x=weightFramex, y=bottomy, anchor='sw')

        self.weightOver = Label(self.weightFrame, text=weightClass)
        self.weightOver.place(x=0, y=20, anchor='w')
        self.weightOver['bg'] = self.halfmaster.master['bg']
        self.weightOver.config(font=(fFont, 20), fg='#ffffff')

        #self.addr = 'localhost'
        self.addr = ''
        self.serverRun = True
        self.port = port


    def sendConfigData(self, client):
        data = '~wrestling`'
        data += str(homeTeam) + '`'
        data += str(awayTeam) + '`'
        data += str(hAbrev) + '`'
        data += str(aAbrev) + '`'
        data += str(hTeamScore) + '`'
        data += str(aTeamScore) + '`'
        data += str(homeScore) + '`'
        data += str(awayScore) + '`'
        data += str(half) + '`'
        data += str(homePrimaryColor) + '`'
        data += str(homeSecondColor) + '`'
        data += str(awayPrimaryColor) + '`'
        data += str(awaySecondColor) + '`'
        data += str(weightClass)+'`'
        data += str(self.swmaster.getMinutes()) + '`'
        data += str(self.swmaster.getSeconds()) + '`'
        client.sendall(data.encode())

    def run(self):
        global clients
        clients = []
        if self.serverRun == True:
            #if self.addr == 'localhost':
            if self.addr == '':
                server = socket(AF_INET, SOCK_STREAM)
                server.bind((self.addr, self.port))
                server.listen(5)
                while(1):
                    self.client, self.addr = server.accept()
                    clients.append(self.client)
                    self.sendConfigData(self.client)
                    Receive(self.client, self).start()
        else:
            server = socket()
            server.bind((self.addr, int(self.port)))
        
    
    
    
def start(port, data):
    global runnin, homeTeam, awayTeam, hAbrev, aAbrev, hTeamScore, aTeamScore, homeScore, awayScore, half,\
        homePrimaryColor, awayPrimaryColor, homeSecondColor, awaySecondColor, weightClass, yellowColor, overlay, network
    # default variables
    runnin = 'Start'
    homeTeam = str(data[0])
    awayTeam = str(data[1])
    hAbrev = str(data[2])
    aAbrev = str(data[3])

    hTeamScore = int(data[4])
    aTeamScore = int(data[5])

    homeScore = int(data[6])
    awayScore = int(data[7])
    half = str(data[8])

    homePrimaryColor = str(data[9])
    homeSecondColor = str(data[10])
    awayPrimaryColor = str(data[11])
    awaySecondColor = str(data[12])
    weightClass = str(data[13])

    yellowColor = '#dbcf30'

    overlay = Tk()
    overlay.configure(bg='#00ff00')
    overlay.geometry('1280x120')
    overlay.title('Scorecast Wrestling Scoreboard')
    overlayApp = App(overlay, port, data).start()
    network = Tk()
    network.configure(bg='#000000')
    network.geometry('130x100')
    network.title('Network Info')
    try:
        ip = gethostbyname(gethostname())
    except:
        ip = 'Lookup ERROR'
    ipLabel = Label(network, fg='#ffffff', bg='#000000', text='IP: ' + ip)
    ipLabel.place(x=65, y=10, anchor='n')
    portLabel = Label(network, fg='#ffffff', bg='#000000', text='Port: ' + str(port))
    portLabel.place(x=65, y=90, anchor='s')

    overlay.mainloop()