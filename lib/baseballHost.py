from tkinter import *
from threading import *
from socket import *
from time import *

teamHeight = 30
infoFrameHeight = 25
baseGraphicHeight = teamHeight + teamHeight
topBottomCanvasHeight = infoFrameHeight * (.45)

teamNameWidth = 115
scoreFrameWidth = 50
baseGraphicWidth = teamHeight + teamHeight + infoFrameHeight - 5

infoFrameWidth = teamNameWidth + scoreFrameWidth + baseGraphicWidth
topBottomCanvasWidth = topBottomCanvasHeight
outWidth = 7

homey = 10
teamx = 20
awayy = homey + teamHeight
scorex = teamx + teamNameWidth
infoFramey = awayy + teamHeight
baseGraphicFramex = scorex + scoreFrameWidth
topBottomx = 35
inningx = topBottomx + (topBottomCanvasWidth / 2) + 5
outx = inningx + 55
outSx = outx + outWidth
countx = (baseGraphicFramex - teamx) + (baseGraphicWidth / 2)

baseSize = 13
baseOffset = 7

secondx = (baseGraphicWidth / 2)
secondy = (baseGraphicHeight / 2) - 3 + baseOffset

firstx = (baseGraphicWidth / 2) + 3
firsty = (baseGraphicHeight / 2) + baseOffset

thirdx = (baseGraphicWidth / 2) - 3
thirdy = (baseGraphicHeight / 2) + baseOffset

firstBasePoints = [firstx + baseSize, firsty - baseSize, firstx + baseSize + baseSize, firsty, firstx + baseSize,
                   firsty + baseSize, firstx, firsty]
secondBasePoints = [secondx, secondy - baseSize - baseSize, secondx + baseSize, secondy - baseSize, secondx, secondy,
                    secondx - baseSize, secondy - baseSize]
thirdBasePoints = [thirdx - baseSize, thirdy - baseSize, thirdx, thirdy, thirdx - baseSize, thirdy + baseSize,
                   thirdx - baseSize - baseSize, thirdy]

downArrowPoints = [0, 0, topBottomCanvasWidth, 0, topBottomCanvasWidth / 2, topBottomCanvasHeight]
upArrowPoints = [topBottomCanvasWidth / 2, 0, topBottomCanvasWidth, topBottomCanvasHeight, 0, topBottomCanvasHeight]


fFont = "Lucida Grande"

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

                if recvText == 'homeTeam':
                    self.app.changeHomeTeam(text[1])
                elif recvText == 'awayTeam':
                    self.app.changeAwayTeam(text[1])
                elif recvText == 'homeScore':
                    self.app.changeHomeScore(text[1])
                elif recvText == 'awayScore':
                    self.app.changeAwayScore(text[1])
                elif recvText == 'changeInning':
                    self.app.changeInning(text[1])
                    self.app.changeTopBottom(text[2])
                    self.app.activateFirst(text[3])
                    self.app.activateSecond(text[4])
                    self.app.activateThird(text[5])
                    self.app.changeCount(text[6], text[7])
                    self.app.changeOuts(text[8], text[9])
                elif recvText == 'changeBases':
                    self.app.activateFirst(text[1])
                    self.app.activateSecond(text[2])
                    self.app.activateThird(text[3])
                elif recvText == 'changeAP':
                    self.app.changeAP(text[1])
                elif recvText == 'changeHP':
                    self.app.changeHP(text[1])
                elif recvText == 'count':
                    self.app.changeCount(text[2], text[1])
                elif recvText == 'changeOuts':
                    self.app.changeOuts(text[1], text[2])
                    self.app.changeCount(text[4], text[3])
                elif recvText == 'sync':
                    self.app.changeHomeTeam(text[1])
                    self.app.changeAwayTeam(text[2])
                    self.app.changeHomeScore(text[3])
                    self.app.changeAwayScore(text[4])
                    self.app.changeInning(text[5])
                    self.app.changeTopBottom(text[6])
                    self.app.activateFirst(text[7])
                    self.app.activateSecond(text[8])
                    self.app.activateThird(text[9])
                    self.app.changeOuts(text[10], text[11])
                    self.app.changeCount(text[12], text[13])
                    self.app.changeHP(text[14])
                    self.app.changeAP(text[15])


            except:
                break

    def recevieData(self):
        global clients
        datum = ""
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

    def changeHomeTeam(self, newTeam):
        global homeTeam
        homeTeam = newTeam
        self.homeTeambballoverlay.configure(text=homeTeam)
        self.homeTeambballoverlay.update()

    def changeAwayTeam(self, newTeam):
        global awayTeam
        awayTeam = newTeam
        self.awayTeambballoverlay.configure(text=awayTeam)
        self.awayTeambballoverlay.update()

    def changeHomeScore(self, newScore):
        global homeScore
        homeScore = newScore
        self.homeScorebballoverlay.configure(text=homeScore)
        self.homeScorebballoverlay.update()

    def changeAwayScore(self, newScore):
        global awayScore
        awayScore = newScore
        self.awayScorebballoverlay.configure(text=awayScore)
        self.awayScorebballoverlay.update()

    def changeInning(self, newInning):
        global inning
        inning = newInning
        self.inningNumberL.configure(text=inning)
        self.inningNumberL.update()

    def changeTopBottom(self, newValue):
        global topBottom
        topBottom = newValue
        if topBottom == "top":
            self.topBottomCanvas.coords('Arrow', upArrowPoints)
        elif topBottom == 'bottom':
            self.topBottomCanvas.coords('Arrow', downArrowPoints)

    def activateFirst(self, newBool):
        global firstActive
        firstActive = newBool
        if firstActive == 'true':
            self.baseGraphicCanvas.itemconfig('firstBase', fill=yellowColor, outline=yellowColor)
        elif firstActive == 'false':
            self.baseGraphicCanvas.itemconfig('firstBase', fill='#000000', outline= greyColor)

    def activateSecond(self, newBool):
        global secondActive
        secondActive = newBool
        if secondActive == 'true':
            self.baseGraphicCanvas.itemconfig('secondBase', fill=yellowColor, outline=yellowColor)
        elif secondActive == 'false':
            self.baseGraphicCanvas.itemconfig('secondBase', fill='#000000', outline= greyColor)

    def activateThird(self, newBool):
        global thirdActive
        thirdActive = newBool
        if thirdActive == 'true':
            self.baseGraphicCanvas.itemconfig('thirdBase', fill=yellowColor, outline=yellowColor)
        elif thirdActive == 'false':
            self.baseGraphicCanvas.itemconfig('thirdBase', fill='#000000', outline= greyColor)


    def changeOuts(self, newOuts, word):
        global outs, outOuts
        outs = newOuts
        outOuts = word
        self.outOverlay.configure(text=str(outs))
        self.outStaticOverlay.configure(text=outOuts)
        self.outOverlay.update()
        self.outStaticOverlay.update()

    def changeCount(self, newStrikes, newBalls):
        global balls, strikes
        balls = newBalls
        strikes = newStrikes
        self.countOverlay.config(text=str(balls) + '-' + str(strikes))
        self.countOverlay.update()

    def changeHP(self, newColor):
        global homePrimaryColor
        homePrimaryColor = newColor
        self.homeFrame.configure(bg=homePrimaryColor)
        self.homeTeambballoverlay.configure(bg=homePrimaryColor)
        self.homeScoreFrame.configure(bg=homePrimaryColor)
        self.homeScorebballoverlay.configure(bg=homePrimaryColor)

    def changeAP(self, newColor):
        global awayPrimaryColor
        awayPrimaryColor = newColor
        self.awayFrame.configure(bg=awayPrimaryColor)
        self.awayScorebballoverlay.configure(bg=awayPrimaryColor)
        self.awayScoreFrame.configure(bg=awayPrimaryColor)
        self.awayTeambballoverlay.configure(bg=awayPrimaryColor)



    def sendConfigData(self, client):
        data = '~baseball`'
        data += str(homeTeam)+'`'
        data += str(awayTeam) + '`'

        data += str(homeScore) + '`'
        data += str(awayScore) + '`'

        data += str(inning) + '`'
        data += str(topBottom) + '`'

        data += str(outs) + '`'
        data += str(outOuts) + '`'

        data += str(balls) + '`'
        data += str(strikes) + '`'

        data += str(firstActive) + '`'
        data += str(secondActive) + '`'
        data += str(thirdActive) + '`'

        data += str(homePrimaryColor) + '`'
        data += str(awayPrimaryColor) + '`'

        client.sendall(data.encode())

    def __init__(self, master, port, data):

        Thread.__init__(self)

        self.homeFrame = Frame(master)
        self.homeFrame.configure(bg=homePrimaryColor, width=teamNameWidth, height=teamHeight)
        self.homeFrame.place(x=teamx, y=homey, anchor='nw')  # 293.33

        self.homeTeambballoverlay = Label(self.homeFrame, text=homeTeam)
        self.homeTeambballoverlay.place(x=5, y=teamHeight / 2, anchor='w')
        self.homeTeambballoverlay['bg'] = self.homeTeambballoverlay.master['bg']
        self.homeTeambballoverlay.config(font=(fFont, 18), fg='#ffffff')

        self.homeScoreFrame = Frame(master)
        self.homeScoreFrame.configure(bg=homePrimaryColor, width=scoreFrameWidth, height=teamHeight)
        self.homeScoreFrame.place(x=scorex, y=homey, anchor='nw')

        self.homeScorebballoverlay = Label(self.homeScoreFrame, text=homeScore)
        self.homeScorebballoverlay.place(x=scoreFrameWidth / 2, y=teamHeight / 2, anchor='c')
        self.homeScorebballoverlay['bg'] = self.homeScorebballoverlay.master['bg']
        self.homeScorebballoverlay.config(font=(fFont, 23), fg='#ffffff')

        self.awayFrame = Frame(master)
        self.awayFrame.configure(bg=awayPrimaryColor, width=teamNameWidth, height=teamHeight)
        self.awayFrame.place(x=teamx, y=awayy, anchor='nw')

        self.awayTeambballoverlay = Label(self.awayFrame, text=awayTeam)
        self.awayTeambballoverlay.place(x=5, y=teamHeight / 2, anchor='w')
        self.awayTeambballoverlay['bg'] = self.awayTeambballoverlay.master['bg']
        self.awayTeambballoverlay.config(font=(fFont, 18), fg='#ffffff')

        self.awayScoreFrame = Frame(master)
        self.awayScoreFrame.configure(bg=awayPrimaryColor, width=scoreFrameWidth, height=teamHeight)
        self.awayScoreFrame.place(x=scorex, y=awayy, anchor='nw')

        self.awayScorebballoverlay = Label(self.awayScoreFrame, text=awayScore)
        self.awayScorebballoverlay.place(x=scoreFrameWidth / 2, y=teamHeight / 2, anchor='c')
        self.awayScorebballoverlay['bg'] = self.awayScorebballoverlay.master['bg']
        self.awayScorebballoverlay.config(font=(fFont, 23), fg='#ffffff')

        self.infoFrame = Frame(master)
        self.infoFrame.configure(bg='#000000', width=infoFrameWidth, height=infoFrameHeight)
        self.infoFrame.place(x=teamx, y=infoFramey, anchor='nw')

        self.topBottomCanvas = Canvas(self.infoFrame)
        self.topBottomCanvas.config(bg="#000000", width=topBottomCanvasWidth, height=topBottomCanvasHeight, bd=0,
                               highlightthickness=0)
        self.topBottomCanvas.place(x=topBottomx, y=infoFrameHeight / 2, anchor='c')

        self.topBottomArrow = self.topBottomCanvas.create_polygon(upArrowPoints, fill=greyColor, tags='Arrow')

        self.inningNumberL = Label(self.infoFrame, text=str(inning))
        self.inningNumberL.place(x=inningx, y=infoFrameHeight / 2, anchor='w')
        self.inningNumberL['bg'] = self.inningNumberL.master['bg']
        self.inningNumberL.config(font=(fFont, 15), fg='#ffffff')

        self.outOverlay = Label(self.infoFrame, text=outs, width=outWidth)
        self.outOverlay.place(x=outx, y=infoFrameHeight / 2, anchor='c')
        self.outOverlay['bg'] = self.outOverlay.master['bg']
        self.outOverlay.config(font=(fFont, 15), fg='#ffffff')

        self.outStaticOverlay = Label(self.infoFrame, text=outOuts)
        self.outStaticOverlay.place(x=outSx, y=infoFrameHeight / 2, anchor='w')
        self.outStaticOverlay['bg'] = self.outStaticOverlay.master['bg']
        self.outStaticOverlay.config(font=(fFont, 14), fg=greyColor)

        self.countOverlay = Label(self.infoFrame, text=str(balls) + '-' + str(strikes))
        self.countOverlay.place(x=countx, y=infoFrameHeight / 2, anchor='c')
        self.countOverlay['bg'] = self.countOverlay.master['bg']
        self.countOverlay.config(font=(fFont, 16), fg='#ffffff')

        self.baseGraphicCanvas = Canvas(master)
        self.baseGraphicCanvas.config(bg="#000000", width=baseGraphicWidth, height=baseGraphicHeight,
                                 borderwidth=0, highlightthickness=0)
        self.baseGraphicCanvas.place(x=baseGraphicFramex, y=homey, anchor='nw')

        self.firstBasePoly = self.baseGraphicCanvas.create_polygon(firstBasePoints, outline=greyColor, width=1,
                                                                   tags='firstBase')
        self.secondBasePoly = self.baseGraphicCanvas.create_polygon(secondBasePoints, outline=greyColor, width=1,
                                                          tags='secondBase')
        self.thirdBasePoly = self.baseGraphicCanvas.create_polygon(thirdBasePoints, outline=greyColor, width=1,
                                                                   tags='thirdBase')

        #self.addr = 'localhost'
        self.addr = ''
        self.serverRun = True
        self.port = port

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
    global homeTeam, awayTeam, homeScore, awayScore, inning, topBottom, outs, outOuts, balls, strikes, firstActive, \
        secondActive, thirdActive, homePrimaryColor, awayPrimaryColor, yellowColor, greyColor, overlay, network
    homeTeam = str(data[0])
    awayTeam = str(data[1])
    homeScore = int(data[2])
    awayScore = int(data[3])
    inning = int(data[4])
    topBottom = str(data[5])
    outs = int(data[6])
    outOuts = str(data[7])
    balls = int(data[8])
    strikes = int(data[9])

    firstActive = str(data[10])
    secondActive = str(data[11])
    thirdActive = str(data[12])
    homePrimaryColor = str(data[13])
    awayPrimaryColor = str(data[14])

    yellowColor = '#dbcf30'
    greyColor = '#737373'

    overlay = Tk()
    overlay.configure(bg='#00ff00')
    overlay.geometry('290x110')
    overlay.title('Scorecast Baseball Scoreboard')

    overlayApp = App(overlay, port, data).start()

    network = Tk()
    network.configure(bg='#000000')
    network.geometry('130x100')
    network.title('Network Info')
    try:
        ip = gethostbyname(gethostname())
    except:
        ip = 'Lookup ERROR'
    ipLabel = Label(network, fg='#ffffff', bg='#000000', text='IP: ' + ip);
    ipLabel.place(x=65, y=10, anchor='n')
    portLabel = Label(network, fg='#ffffff', bg='#000000', text='Port: ' + str(port))
    portLabel.place(x=65, y=90, anchor='s')

    overlay.mainloop()
