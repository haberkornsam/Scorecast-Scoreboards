from tkinter import *
import time
import easygui
import xml.etree.ElementTree as ET
from lib import wrestlingHost


# control values
centerx = 300
swx = centerx
swy = 10
startx = centerx
starty = 40
setClockx = centerx
setClocky = 70
enterTimeMx = 250
enterTimeMy = 10
enterTimeColonx = 300
enterTimeColony = 12
enterTimeSx = 350
enterTimeSy = 10
homeLabelx = 10
teamLabely = 40
awayLabelx = 590
homeScoreLx = 10
matchScoreLy = 100
awayScoreLx = 590
teamEditScorey = 145
hscore1x = 8
hscore2x = 73
hscore3x = 138
ascore1x = 600 - hscore3x
ascore2x = 600 - hscore2x
ascore3x = 600 - hscore1x
scorey = 222
hFoulLabx = 35
aFoulLabx = 600 - hFoulLabx
foulLaby = 260
hFoulLx = 10
FoulLy = 300
aFoulLx = 600 - hFoulLx
homeBonusx = 165
awayBonusx = 600 - homeBonusx
foulAdy = 295
foulSubty = 320
homePossx = 215
awayPossx = 600 - homePossx
homeStaticTOx = 30
awayStaticTOx = 600 - homeStaticTOx
staticTOy = 350
hPartTOLabelx = 10
hFullTOLabelx = 80
TOLabely = 390
aPartTOLabelx = 600 - hFullTOLabelx
aFullTOLabelx = 600 - hPartTOLabelx
hTakex = 145
aTakex = 600 - hTakex
takeParty = 385
takeFully = 410
hcolorx = 15
acolorx = 600 - hcolorx
priColory = 375
secColory = 400
servery = 350


fFont = "Lucida Grande"


class StopWatch(Frame):
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
        self.formatted = ''
        # self.makeWidgets()
        self.l = Label(self, text=self.formatted, width=20)
        self.l.grid(row=0, column=3, columnspan=3)
        self._setTime(self._elapsedtime)

    def makeWidgets(self):
        """ Make the time label. """
        # l = Label(self, textvariable=self.timestr, width=20)
        # self._setTime(self._elapsedtime)
        # l.grid(row=0, column=3, columnspan=3)

    def _update(self):
        global clockFile
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)

        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        newTime = self._startingTime - elap
        if newTime <= 0:
            newTime = 0
        minutes = int(newTime / 60)
        seconds = int(newTime - minutes * 60.0)
        hseconds = int((newTime - minutes * 60.0 - seconds) * 10)

        self.formatted = str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "." + str(hseconds).zfill(1)
        self._minutes = str(minutes).zfill(2)
        self._seconds = str(seconds).zfill(2) + "." + str(hseconds).zfill(1)
        format = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        self.timestr.set(self.formatted)
        self.l.configure(text=self.formatted)

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)

    def setClock(self, newTimeM, newTimeS):

        self._elapsedtime = 0.0
        self._running = 0
        self._startingTime = 0
        try:
            self._startingTime = float(newTimeM) * 60
        except ValueError:
            pass

        try:
            self._startingTime += float(newTimeS)
        except ValueError:
            pass

        self._start = time.time()
        self._setTime(self._elapsedtime)

    def getClockTime(self):
        return self._startingTime - self._elapsedtime

    def getMinutes(self):
        return self._minutes

    def getSeconds(self):
        return self._seconds


class StopWatchwrestOverlay(Frame):
    """ Implements a stop watch frame widget. """

    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._startingTime = 120
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.timeString = ''
        self.makeWidgets()

    def makeWidgets(self):
        global l
        """ Make the time label. """
        l = Label(self, text=self.timeString, bg='#000000')
        self._setTime(self._elapsedtime)
        l.config(font=(fFont, 24), fg='#dbcf30')
        l.place(x=2, y=20, anchor='w')

    def _update(self):
        global clockFile
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)

        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        newTime = self._startingTime - elap
        if newTime <= 0:
            newTime = 0
        minutes = int(newTime / 60)
        seconds = int(newTime - minutes * 60.0)
        hseconds = int((newTime - minutes * 60.0 - seconds) * 10)

        if minutes == 0:
            formatted = str(seconds).zfill(2) + "." + str(hseconds).zfill(1)
            format = str(seconds) + "." + str(hseconds).zfill(1)
        else:
            formatted = str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "." + str(hseconds).zfill(1)
            format = str(minutes) + ":" + str(seconds).zfill(2)

        self.timeString = formatted
        l.configure(text=format)

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)

    def setClock(self, newTimeM, newTimeS):

        self._elapsedtime = 0.0
        self._running = 0
        self._startingTime = 0
        try:
            self._startingTime = float(newTimeM) * 60
        except ValueError:
            pass

        try:
            self._startingTime += float(newTimeS)
        except ValueError:
            pass

        self._start = time.time()
        self._setTime(self._elapsedtime)

    def getClockTime(self):
        return self._startingTime - self._elapsedtime


def toggleStartLabel(event):
    global runnin
    if runnin == 'Start':
        runnin = 'Stop'
        star.configure(text=runnin)
        sw.Start()
        swwrestOverlay.Start()

    else:
        runnin = 'Start'
        star.configure(text=runnin)
        sw.Stop()
        swwrestOverlay.Stop()


def changeTime(event):
    global runnin
    sw.Stop()
    swwrestOverlay.Stop()
    runnin = "Stop"
    star.configure(text=runnin)
    sw.place_forget()
    enterTimeM.delete(0, END)
    enterTimeS.delete(0, END)
    enterTimeM.place(x=enterTimeMx, y=enterTimeMy, anchor='n')
    enterTimeColon.place(x=enterTimeColonx, y=enterTimeColony, anchor='n')
    enterTimeS.place(x=enterTimeSx, y=enterTimeSy, anchor='n')
    star.place_forget()
    sub.place(x=startx, y=starty, anchor='n')
    setClock.place(x=setClockx, y=setClocky, anchor='n')


def submitTime(event):
    global runnin
    sw.setClock(enterTimeM.get(), enterTimeS.get())
    swwrestOverlay.setClock(enterTimeM.get(), enterTimeS.get())
    runnin = "Start"
    star.configure(text=runnin)
    enterTimeM.place_forget()
    enterTimeS.place_forget()
    enterTimeColon.place_forget()
    sub.place_forget()
    sw.place(x=swx, y=swy, anchor='n')
    star.place(x=startx, y=starty, anchor='n')


def changeHomeTeam(event):
    homeLabel.place_forget()
    homeInput.place(x=homeLabelx, y=teamLabely, anchor='nw')


def changeAwayTeam(event):
    awayLabel.place_forget()
    awayInput.place(x=awayLabelx, y=teamLabely, anchor='ne')


def saveHomeTeam(event):
    global homeTeam
    homeTeam = str(homeInput.get())
    homeInput.place_forget()
    homeLabel.configure(text=homeTeam)
    homeLabel.place(x=homeLabelx, y=teamLabely, anchor='nw')
    homeTeamwrestOverlay.configure(text=homeTeam)
    homeTeamwrestOverlay.update()


def saveAwayTeam(event):
    global awayTeam
    awayTeam = str(awayInput.get())
    awayInput.place_forget()
    awayLabel.configure(text=awayTeam)
    awayLabel.place(x=awayLabelx, y=teamLabely, anchor='ne')
    awayTeamwrestOverlay.configure(text=awayTeam)
    awayTeamwrestOverlay.update()


def editHomeScore(event):
    homeScoreL.place_forget()
    hEditScore.place(x=homeScoreLx, y=teamEditScorey, anchor='nw')


def editAwayScore(event):
    awayScoreL.place_forget()
    aEditScore.place(x=awayScoreLx, y=teamEditScorey, anchor='ne')


def homeScoreOverride(event):
    global homeScore
    homeScore = int(hEditScore.get())
    homeScoreFileUpdate()
    hEditScore.place_forget()
    homeScoreL.place(x=homeScoreLx, y=matchScoreLy, anchor='nw')


def awayScoreOverride(event):
    global awayScore
    awayScore = int(aEditScore.get())
    awayScoreFileUpdate()
    aEditScore.place_forget()
    awayScoreL.place(x=awayScoreLx, y=matchScoreLy, anchor='ne')


def homeScoreFileUpdate():
    global homeScore, awayScore
    homeScorewrestOverlay.configure(text=homeScore)
    homeScorewrestOverlay.update()
    homeScoreL.configure(text=homeScore)


def awayScoreFileUpdate():
    global homeScore, awayScore
    awayScorewrestOverlay.configure(text=awayScore)
    awayScorewrestOverlay.update()
    awayScoreL.configure(text=awayScore)


def hScore1(event):
    global homeScore, awayScore
    homeScore += 1
    homeScoreFileUpdate()


def aScore1(event):
    global homeScore, awayScore
    awayScore += 1
    awayScoreFileUpdate()


def hScore2(event):
    global homeScore, awayScore
    homeScore += 2
    homeScoreFileUpdate()


def aScore2(event):
    global homeScore, awayScore
    awayScore += 2
    awayScoreFileUpdate()


def hScore3(event):
    global homeScore, awayScore
    homeScore += 3
    homeScoreFileUpdate()


def aScore3(event):
    global homeScore, awayScore
    awayScore += 3
    awayScoreFileUpdate()


def changehTeamScore(event):
    hTeamScoreL.place_forget()
    hTeamScoreIn.place(x=hFoulLx, y=FoulLy, anchor='nw')


def changeaTeamScore(event):
    aTeamScoreL.place_forget()
    aTeamScoreIn.place(x=aFoulLx, y=FoulLy, anchor='ne')


def submithTeamScore(event):
    global hTeamScore
    hTeamScoreL.place(x=hFoulLx, y=FoulLy, anchor='nw')
    hTeamScoreIn.place_forget()
    hTeamScore = int(hTeamScoreIn.get())
    hTeamScoreUpdate()


def submitaTeamScore(event):
    global aTeamScore
    aTeamScoreL.place(x=aFoulLx, y=FoulLy, anchor='ne')
    aTeamScoreIn.place_forget()
    aTeamScore = int(aTeamScoreIn.get())
    aTeamScoreUpdate()


def hTeamScoreSix(event):
    global hTeamScore
    hTeamScore += 6
    hTeamScoreUpdate()


def aTeamScoreSix(event):
    global aTeamScore
    aTeamScore += 6
    aTeamScoreUpdate()


def hTeamScoreThree(event):
    global hTeamScore
    hTeamScore += 3
    hTeamScoreUpdate()


def aTeamScoreThree(event):
    global aTeamScore
    aTeamScore += 3
    aTeamScoreUpdate()


def hTeamScoreUpdate():
    global hTeamScore
    hTeamScoreOverlay.configure(text=hTeamScore)
    hTeamScoreOverlay.update()
    hTeamScoreL.configure(text=hTeamScore)


def aTeamScoreUpdate():
    global aTeamScore
    aTeamScoreOverlay.configure(text=aTeamScore)
    aTeamScoreOverlay.update()
    aTeamScoreL.configure(text=aTeamScore)


def resetMatchScore(event):
    global homeScore, awayScore
    homeScore = 0
    awayScore = 0
    homeScoreFileUpdate()
    awayScoreFileUpdate()


def changeHalf(event):
    halfLabel.place_forget()
    halfIn.place(x=centerx, y=teamEditScorey, anchor='n')


def submitHalf(event):
    global half
    halfIn.place_forget()
    halfLabel.place(x=centerx, y=teamEditScorey, anchor='n')
    half = str(halfIn.get())
    halfLabel.configure(text=half)
    halfwrestOverlay.configure(text=str(half))
    halfwrestOverlay.update()


def changeHPrimary(event):
    setHPrimary.place_forget()
    hPriIn.place(x=hcolorx, y=priColory, anchor='nw')


def changeHSecond(event):
    setHSecond.place_forget()
    hSecIn.place(x=hcolorx, y=secColory, anchor='nw')


def changeAPrimary(event):
    setAPrimary.place_forget()
    aPriIn.place(x=acolorx, y=priColory, anchor='ne')


def changeASecond(event):
    setASecond.place_forget()
    aSecIn.place(x=acolorx, y=secColory, anchor='ne')


def subHP(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    homePrimaryColor = str(hPriIn.get())
    homeFrame.configure(bg=homePrimaryColor)
    homeTeamwrestOverlay.configure(bg=homePrimaryColor)
    hPriIn.place_forget()
    setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')


def subHS(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    homeSecondColor = str(hSecIn.get())
    homeScoreFrame.configure(bg=homeSecondColor)
    homeScorewrestOverlay.configure(bg = homeSecondColor)
    hSecIn.place_forget()
    setHSecond.place(x=hcolorx, y=secColory, anchor='nw')
    hTeamScoreFrame.configure(bg=homeSecondColor)
    hTeamScoreOverlay.configure(bg = homeSecondColor)
    hTeamNameOverlay.configure(bg = homeSecondColor)


def subAP(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    awayPrimaryColor = str(aPriIn.get())
    awayFrame.configure(bg=awayPrimaryColor)
    awayTeamwrestOverlay.configure(bg = awayPrimaryColor)
    aPriIn.place_forget()
    setAPrimary.place(x=acolorx, y=priColory, anchor='ne')


def subAS(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    awaySecondColor = str(aSecIn.get())
    awayScoreFrame.configure(bg=awaySecondColor)
    awayScorewrestOverlay.configure(bg=awaySecondColor)
    aSecIn.place_forget()
    setASecond.place(x=acolorx, y=secColory, anchor='ne')

    aTeamScoreFrame.config(bg=awaySecondColor)
    aTeamScoreOverlay.configure(bg=awaySecondColor)
    aTeamNameOverlay.configure(bg=awaySecondColor)


def updateTeamNames():
    homeLabel.configure(text=homeTeam)
    homeTeamwrestOverlay.configure(text=homeTeam)
    homeTeamwrestOverlay.update()
    awayLabel.configure(text=awayTeam)
    awayTeamwrestOverlay.configure(text=awayTeam)
    awayTeamwrestOverlay.update()


def updateColors():
    homeFrame.configure(bg=homePrimaryColor)
    homeTeamwrestOverlay.configure(bg=homePrimaryColor)

    homeScoreFrame.config(bg=homeSecondColor)
    homeScorewrestOverlay.config(bg=homeSecondColor)

    awayFrame.configure(bg=awayPrimaryColor)
    awayTeamwrestOverlay.configure(bg=awayPrimaryColor)

    awayScoreFrame.configure(bg=awaySecondColor)
    awayScorewrestOverlay.configure(bg=awaySecondColor)

    hTeamScoreFrame.configure(bg=homeSecondColor)
    hTeamScoreOverlay.configure(bg=homeSecondColor)
    hTeamNameOverlay.configure(bg=homeSecondColor)

    aTeamScoreFrame.config(bg=awaySecondColor)
    aTeamScoreOverlay.config(bg=awaySecondColor)
    aTeamNameOverlay.config(bg=awaySecondColor)


def changeHomeAbrev(event):
    homeAbrevL.place_forget()
    homeAbrevIn.place(x=homeLabelx, y=10, anchor='nw')


def subHomeAbrev(event):
    global hAbrev
    hAbrev = str(homeAbrevIn.get())
    homeAbrevL.config(text=hAbrev)
    hTeamNameOverlay.config(text=hAbrev)
    hTeamNameOverlay.update()
    homeAbrevIn.place_forget()
    homeAbrevL.place(x=homeLabelx, y=10, anchor='nw')


def changeAwayAbrev(event):
    awayAbrevL.place_forget()
    awayAbrevIn.place(x=awayLabelx, y=10, anchor='ne')


def subAwayAbrev(event):
    global aAbrev
    aAbrev = str(awayAbrevIn.get())
    awayAbrevL.config(text=aAbrev)
    aTeamNameOverlay.config(text=aAbrev)
    aTeamNameOverlay.update()
    awayAbrevIn.place_forget()
    awayAbrevL.place(x=awayLabelx, y=10, anchor='ne')


def abrevUpdate():
    homeAbrevL.config(text=hAbrev)
    hTeamNameOverlay.config(text=hAbrev)
    hTeamNameOverlay.update()
    awayAbrevL.config(text=aAbrev)
    aTeamNameOverlay.config(text=aAbrev)
    aTeamNameOverlay.update()


def changeWeightClass(event):
    weightClassCtrl.place_forget()
    weightClassIn.place(x=centerx, y=FoulLy, anchor='n')


def subWeightClass(event):
    global weightClass
    weightClass = str(weightClassIn.get())
    weightUpdate()
    weightClassCtrl.place(x=centerx, y=FoulLy, anchor='n')
    weightClassIn.place_forget()


def weightUpdate():
    weightClassCtrl.config(text=weightClass)
    weightOver.config(text=weightClass)
    weightOver.update()


def updateLabels():
    updateTeamNames()
    homeScoreFileUpdate()
    awayScoreFileUpdate()
    hTeamScoreUpdate()
    aTeamScoreUpdate()
    weightUpdate()
    abrevUpdate()
    updateColors()


def openConfig(event):
    global homeTeam, awayTeam, homeScore, awayScore, aTeamScore, hTeamScore, half, homePoss, awayPoss, homePartTO, awayPartTO, \
        homeFullTO, awayFullTO, homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, sw, hAbrev, aAbrev, \
        hTeamScore, aTeamScore, weightClass
    tree = ET.parse(easygui.fileopenbox(filetypes=['*.xml'])).getroot()
    if (tree.tag == 'wrestling'):
        hAbrev = str(tree[0][0].text)
        hTeamScore = int(tree[0][1].text)
        homeTeam = str(tree[0][2].text)
        homeScore = int(tree[0][3].text)
        homePrimaryColor = str(tree[0][4].text)
        homeSecondColor = str(tree[0][5].text)

        aAbrev = str(tree[1][0].text)
        aTeamScore = int(tree[1][1].text)
        awayTeam = str(tree[1][2].text)
        awayScore = int(tree[1][3].text)
        awayPrimaryColor = str(tree[1][4].text)
        awaySecondColor = str(tree[1][5].text)
        half = str(tree[2].text)
        sw.setClock(int(tree[3][0].text), float(tree[3][1].text))
        swwrestOverlay.setClock(int(tree[3][0].text), float(tree[3][1].text))
        weightClass = str(tree[4].text)
        updateLabels()


def saveConfig(event):
    global homeTeam, awayTeam, homeScore, awayScore, aTeamScore, hTeamScore, half, homePoss, awayPoss, homePartTO, awayPartTO, \
        homeFullTO, awayFullTO, homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, sw, hAbrev, aAbrev, \
        hTeamScore, aTeamScore, weightClass
    wrestling1 = ET.Element('wrestling')
    homeTeam1 = ET.SubElement(wrestling1, 'home')
    hAbrev1 = ET.SubElement(homeTeam1, 'abrev')
    hAbrev1.text = str(hAbrev)
    hTScore1 = ET.SubElement(homeTeam1, 'teamScore')
    hTScore1.text = str(hTeamScore)
    hname1 = ET.SubElement(homeTeam1, 'wrestlerName')
    hname1.text = str(homeTeam)
    hscore1 = ET.SubElement(homeTeam1, 'matchScore')
    hscore1.text = str(homeScore)
    hpriColor1 = ET.SubElement(homeTeam1, 'primaryColor')
    hpriColor1.text = str(homePrimaryColor)
    hsecColor1 = ET.SubElement(homeTeam1, 'secondaryColor')
    hsecColor1.text = str(homeSecondColor)
    awayTeam1 = ET.SubElement(wrestling1, 'away')
    aAbrev1 = ET.SubElement(awayTeam1, 'abrev')
    aAbrev1.text = str(aAbrev)
    aTScore1 = ET.SubElement(awayTeam1, 'teamScore')
    aTScore1.text = str(aTeamScore)
    aname1 = ET.SubElement(awayTeam1, 'wrestlerName')
    aname1.text = str(awayTeam)
    ascore1 = ET.SubElement(awayTeam1, 'matchScore')
    ascore1.text = str(awayScore)
    apriColor1 = ET.SubElement(awayTeam1, 'primaryColor')
    apriColor1.text = str(awayPrimaryColor)
    asecColor1 = ET.SubElement(awayTeam1, 'secondaryColor')
    asecColor1.text = str(awaySecondColor)

    half1 = ET.SubElement(wrestling1, 'Period')
    half1.text = str(half)
    clock1 = ET.SubElement(wrestling1, 'Clock')
    minutes1 = ET.SubElement(clock1, 'Minutes')
    minutes1.text = str(sw.getMinutes())
    seconds1 = ET.SubElement(clock1, 'Seconds')
    seconds1.text = str(sw.getSeconds())
    weightClass1 = ET.SubElement(wrestling1, 'weightClass')
    weightClass1.text = str(weightClass)
    myData = ET.tostring(wrestling1).decode("utf-8")

    configFile = open(str(easygui.filesavebox()) + '.xml', 'w')
    configFile.write(myData)


def enterPort(event):
    serverLabel.place_forget()
    portSubmit.place(x=centerx, y=servery, anchor='n')
    portLabel.place(x=centerx-15, y=servery-25, anchor='ne')
    portEntry.place(x=centerx-15, y=servery-25, anchor='nw')

def submitPort(event):
    port = int(portEntry.get())
    data = []
    data.append(homeTeam)
    data.append(awayTeam)
    data.append(hAbrev)
    data.append(aAbrev)
    data.append(hTeamScore)
    data.append(aTeamScore)
    data.append(homeScore)
    data.append(awayScore)
    data.append(half)
    data.append(homePrimaryColor)
    data.append(homeSecondColor)
    data.append(awayPrimaryColor)
    data.append(awaySecondColor)
    data.append(weightClass)
    data.append(sw.getMinutes())
    data.append(sw.getSeconds())

    wrestOverlay.destroy()
    wrestlingCtrl.destroy()
    wrestlingHost.start(port, data)

def start():
    global runnin, clockFile, sw, enterTimeM, star, sub, submit, enterTimeS, setClock, enterTimeColon, \
        homeLabel, homeTeam, awayLabel, awayTeam, homeSave, awaySave, homeInput, awayInput, homeScoreL, awayScoreL, \
        homeScore, awayScore, homeScore1, homeScore2, homeScore3, awayScore1, awayScore2, awayScore3, hEditScore, \
        aEditScore, awayEditScoreSave, homeEditScoreSave, hTeamScoreL, hTeamScore, aTeamScoreL, aTeamScore, hTeamScoreIn, \
        aTeamScoreIn, half, halfLabel, halfIn, \
        swwrestOverlay, homeTeamwrestOverlay, awayTeamwrestOverlay, homeScorewrestOverlay, awayScorewrestOverlay, \
        halfwrestOverlay, \
        setHPrimary, setHSecond, setAPrimary, setASecond, hSecIn, hPriIn, aSecIn, aPriIn, \
        homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, homeFrame, awayFrame, homeScoreFrame, \
        awayScoreFrame, homeAbrevL, homeAbrevIn, awayAbrevIn, awayAbrevL, hAbrev, aAbrev, weightClassIn, weightClassCtrl, \
        weightClass, hTeamNameOverlay, aTeamNameOverlay, weightClass, weightClassCtrl, weightClassIn, weightOver, \
        hTeamScore, aTeamScore, homeScoreFrame, aScoreFrame, hTeamScoreFrame, aTeamScoreFrame, hTeamScoreOverlay, \
        aTeamScoreOverlay, hTeamNameOverlay, aTeamNameOverlay, serverLabel, portSubmit, portLabel, portEntry, \
        wrestOverlay, wrestlingCtrl
    wrestlingCtrl = Tk()
    wrestlingCtrl.configure(bg='#000000')
    wrestlingCtrl.title("Scorecast Wrestling Controller")
    wrestlingCtrl.geometry('600x435')
    wrestOverlay = Tk()
    wrestOverlay.configure(bg='#00ff00')
    wrestOverlay.geometry('1280x120')
    wrestOverlay.title('Scorecast Wrestling Scoreboard')
    sw = StopWatch(wrestlingCtrl)
    sw.place(x=300, y=10, anchor='n')

    # default variables
    runnin = 'Start'
    homeTeam = 'ERIKSON'
    awayTeam = 'JOHNSON'
    hAbrev = 'HOME'
    aAbrev = "GUEST"

    hTeamScore = 0
    aTeamScore = 0

    homeScore = 0
    awayScore = 0
    half = '1st'

    homePrimaryColor = '#c1a551'
    homeSecondColor = '#877338'
    awayPrimaryColor = '#110b5d'
    awaySecondColor = '#0d084a'
    weightClass = '103 lbs'

    yellowColor = '#dbcf30'

    # start button
    star = Label(wrestlingCtrl, text=runnin, width=20)
    star.bind('<Button-1>', toggleStartLabel)
    star.place(x=startx, y=starty, anchor='n')

    # set Clock Button
    setClock = Label(wrestlingCtrl, text='Set Time', width=20)
    setClock.bind('<Button-1>', changeTime)
    setClock.place(x=setClockx, y=setClocky, anchor='n')

    # Enter time entries
    enterTimeM = Entry(wrestlingCtrl, text='mm', width=5)
    enterTimeM.place(x=enterTimeMx, y=enterTimeMy, anchor='n')
    enterTimeM.place_forget()
    enterTimeColon = Label(wrestlingCtrl, text=':', width=3)
    enterTimeColon.place(x=enterTimeColonx, y=enterTimeColony, anchor='n')
    enterTimeColon.place_forget()
    enterTimeS = Entry(wrestlingCtrl, text="ss", width=5)
    enterTimeS.place(x=enterTimeSx, y=enterTimeSy, anchor='n')
    enterTimeS.place_forget()

    # submit time button
    sub = Label(wrestlingCtrl, text="Submit", width=20)
    sub.bind('<Button-1>', submitTime)
    sub.place_forget()

    # Team Abrev labels
    homeAbrevL = Label(wrestlingCtrl, text=hAbrev, width=20)
    homeAbrevL.bind('<Button-1>', changeHomeAbrev)
    homeAbrevL.place(x=homeLabelx, y=10, anchor='nw')

    homeAbrevIn = Entry(wrestlingCtrl, width=20)
    homeAbrevIn.bind('<Return>', subHomeAbrev)
    homeAbrevIn.place_forget()

    awayAbrevL = Label(wrestlingCtrl, text=aAbrev, width=20)
    awayAbrevL.bind('<Button-1>', changeAwayAbrev)
    awayAbrevL.place(x=awayLabelx, y=10, anchor='ne')

    awayAbrevIn = Entry(wrestlingCtrl, width=20)
    awayAbrevIn.bind('<Return>', subAwayAbrev)
    awayAbrevIn.place_forget()

    # Athlete Name Labels including Changing Names
    homeLabel = Label(wrestlingCtrl, text=homeTeam, width=20)
    homeLabel.bind('<Button-1>', changeHomeTeam)
    homeLabel.place(x=homeLabelx, y=teamLabely, anchor='nw')
    awayLabel = Label(wrestlingCtrl, text=awayTeam, width=20)
    awayLabel.bind('<Button-1>', changeAwayTeam)
    awayLabel.place(x=awayLabelx, y=teamLabely, anchor='ne')

    # New team Name Inputs
    homeInput = Entry(wrestlingCtrl, width=19)
    homeInput.bind('<Return>', saveHomeTeam)
    homeInput.place_forget()
    awayInput = Entry(wrestlingCtrl, width=19)
    awayInput.bind('<Return>', saveAwayTeam)
    awayInput.place_forget()

    # Score Elements
    # Score Labels
    homeScoreL = Label(wrestlingCtrl, text=00, width=20, height=7)
    homeScoreL.bind("<Button-1>", editHomeScore)
    homeScoreL.place(x=homeScoreLx, y=matchScoreLy, anchor='nw')
    awayScoreL = Label(wrestlingCtrl, text=00, width=20, height=7)
    awayScoreL.bind("<Button-1>", editAwayScore)
    awayScoreL.place(x=awayScoreLx, y=matchScoreLy, anchor='ne')

    # Edit Scores
    hEditScore = Entry(wrestlingCtrl, width=19)
    hEditScore.bind('<Return>', homeScoreOverride)
    hEditScore.place_forget()
    aEditScore = Entry(wrestlingCtrl, width=19)
    aEditScore.bind('<Return>', awayScoreOverride)
    aEditScore.place_forget()

    # Increase Score Buttons
    homeScore1 = Label(wrestlingCtrl, text='+1', width=6)
    homeScore1.bind("<Button-1>", hScore1)
    homeScore1.place(x=hscore1x, y=scorey, anchor='nw')
    homeScore2 = Label(wrestlingCtrl, text='+2', width=6)
    homeScore2.bind("<Button-1>", hScore2)
    homeScore2.place(x=hscore2x, y=scorey, anchor='nw')
    homeScore3 = Label(wrestlingCtrl, text='+3', width=6)
    homeScore3.bind("<Button-1>", hScore3)
    homeScore3.place(x=hscore3x, y=scorey, anchor='nw')

    awayScore1 = Label(wrestlingCtrl, text='+1', width=6)
    awayScore1.bind("<Button-1>", aScore1)
    awayScore1.place(x=ascore1x, y=scorey, anchor='ne')
    awayScore2 = Label(wrestlingCtrl, text='+2', width=6)
    awayScore2.bind("<Button-1>", aScore2)
    awayScore2.place(x=ascore2x, y=scorey, anchor='ne')
    awayScore3 = Label(wrestlingCtrl, text='+3', width=6)
    awayScore3.bind("<Button-1>", aScore3)
    awayScore3.place(x=ascore3x, y=scorey, anchor='ne')

    # Foul elements

    # Number of Fouls
    hTeamScoreL = Label(wrestlingCtrl, text=hTeamScore, width=12, height=2)
    hTeamScoreL.bind('<Button-1>', changehTeamScore)
    hTeamScoreL.place(x=hFoulLx, y=FoulLy, anchor='nw')
    aTeamScoreL = Label(wrestlingCtrl, text=aTeamScore, width=12, height=2)
    aTeamScoreL.bind('<Button-1>', changeaTeamScore)
    aTeamScoreL.place(x=aFoulLx, y=FoulLy, anchor='ne')

    # Foul Inputs
    hTeamScoreIn = Entry(wrestlingCtrl, width=12)
    hTeamScoreIn.bind('<Return>', submithTeamScore)
    hTeamScoreIn.place(x=hFoulLx, y=FoulLy, anchor='nw')
    hTeamScoreIn.place_forget()
    aTeamScoreIn = Entry(wrestlingCtrl, width=12)
    aTeamScoreIn.bind('<Return>', submitaTeamScore)
    aTeamScoreIn.place(x=aFoulLx, y=FoulLy, anchor='ne')
    aTeamScoreIn.place_forget()

    # Bonus Labels

    # Add Foul Buttons
    hTeamScoreAd6 = Label(wrestlingCtrl, text="+6", width=6, height=1)
    hTeamScoreAd6.bind('<Button-1>', hTeamScoreSix)
    hTeamScoreAd6.place(x=homeBonusx, y=foulAdy, anchor='n')
    aTeamScoreAd6 = Label(wrestlingCtrl, text="+6", width=6)
    aTeamScoreAd6.bind('<Button-1>', aTeamScoreSix)
    aTeamScoreAd6.place(x=awayBonusx, y=foulAdy, anchor='n')

    # Subtract Foul Buttons
    hTeamScoreAd3 = Label(wrestlingCtrl, text='+3', width=6, height=1)
    hTeamScoreAd3.bind('<Button-1>', hTeamScoreThree)
    hTeamScoreAd3.place(x=homeBonusx, y=foulSubty, anchor='n')

    aTeamScoreAd3 = Label(wrestlingCtrl, text='+3', width=6)
    aTeamScoreAd3.bind('<Button-1>', aTeamScoreThree)
    aTeamScoreAd3.place(x=awayBonusx, y=foulSubty, anchor='n')

    # Clear Team Fouls
    resetMatchLabel = Label(wrestlingCtrl, text='Reset Match Score', width=15)
    resetMatchLabel.bind('<Button-1>', resetMatchScore)
    resetMatchLabel.place(x=centerx, y=scorey, anchor='n')

    # Team Foul Labels
    hFoulLab = Label(wrestlingCtrl, text='Home Team Score', fg='#ffffff', bg='#000000')
    hFoulLab.place(x=hFoulLabx, y=foulLaby, anchor='nw')
    aFoulLab = Label(wrestlingCtrl, text='Away Team Score', fg='#ffffff', bg='#000000')
    aFoulLab.place(x=aFoulLabx, y=foulLaby, anchor='ne')

    # Period Buttons
    halfLabel = Label(wrestlingCtrl, text=half, width=5)
    halfLabel.bind('<Button-1>', changeHalf)
    halfLabel.place(x=centerx, y=teamEditScorey, anchor='n')

    # Period Input
    halfIn = Entry(wrestlingCtrl, width=5)
    halfIn.bind('<Return>', submitHalf)
    halfIn.place_forget()

    # color changing
    setHPrimary = Label(wrestlingCtrl, text="Set Home Primary Color", width=20)
    setHPrimary.bind('<Button-1>', changeHPrimary)
    setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')

    setHSecond = Label(wrestlingCtrl, text="Set Home Secondary Color", width=20)
    setHSecond.bind('<Button-1>', changeHSecond)
    setHSecond.place(x=hcolorx, y=secColory, anchor='nw')

    setAPrimary = Label(wrestlingCtrl, text="Set Away Primary Color", width=20)
    setAPrimary.bind('<Button-1>', changeAPrimary)
    setAPrimary.place(x=acolorx, y=priColory, anchor='ne')

    setASecond = Label(wrestlingCtrl, text='Set Away Secondary Color', width=20)
    setASecond.bind('<Button-1>', changeASecond)
    setASecond.place(x=acolorx, y=secColory, anchor='ne')

    hPriIn = Entry(wrestlingCtrl, width=18)
    hPriIn.bind('<Return>', subHP)
    hPriIn.place_forget()

    hSecIn = Entry(wrestlingCtrl, width=18)
    hSecIn.bind('<Return>', subHS)
    hSecIn.place_forget()

    aPriIn = Entry(wrestlingCtrl, width=18)
    aPriIn.bind('<Return>', subAP)
    aPriIn.place_forget()

    aSecIn = Entry(wrestlingCtrl, width=18)
    aSecIn.bind('<Return>', subAS)
    aSecIn.place_forget()

    openConfigLabel = Label(wrestlingCtrl, text='Open Configuration')
    openConfigLabel.bind('<Button-1>', openConfig)
    openConfigLabel.place(x=centerx, y=priColory, anchor='n')

    saveConfiglabel = Label(wrestlingCtrl, text='Save Configuration')
    saveConfiglabel.bind('<Button-1>', saveConfig)
    saveConfiglabel.place(x=centerx, y=secColory, anchor='n')

    # Weight Class Ctrl

    weightClassCtrl = Label(wrestlingCtrl, text=weightClass, width=15)
    weightClassCtrl.bind('<Button-1>', changeWeightClass)
    weightClassCtrl.place(x=centerx, y=FoulLy, anchor='n')

    weightClassIn = Entry(wrestlingCtrl, width=15)
    weightClassIn.bind('<Return>', subWeightClass)
    weightClassIn.place_forget()

    #server
    serverLabel = Label(wrestlingCtrl, text='Configure Server')
    serverLabel.bind("<Button-1>", enterPort)
    serverLabel.place(x=centerx, y=servery, anchor='n')

    portSubmit = Label(wrestlingCtrl, text='Submit')
    portSubmit.bind("<Button-1>", submitPort)
    portSubmit.place_forget()

    portEntry = Entry(wrestlingCtrl, width=7)
    portEntry.bind("<Return>", submitPort)
    portEntry.place_forget()

    portLabel = Label(wrestlingCtrl, bg='#000000', text='Port: ', fg='#ffffff')
    portLabel.place_forget()

    # WRESTLINGoverlay

    matchScoreFrameSize = 55
    teamFrameSize = 210 - matchScoreFrameSize
    swOverlayWidth = 75

    bottomy = 60
    hTeamScorex = 240
    homeFramex = hTeamScorex + matchScoreFrameSize
    homeMatchScoreFrame = homeFramex + teamFrameSize

    aTeamScorex = homeMatchScoreFrame + matchScoreFrameSize
    awayFramex = aTeamScorex + matchScoreFrameSize
    awayMatchScoreFrame = awayFramex + teamFrameSize

    timeFramex = awayMatchScoreFrame + matchScoreFrameSize
    swOverlayx = timeFramex + matchScoreFrameSize

    weightFramex = swOverlayx + swOverlayWidth

    homeFrame = Frame(wrestOverlay)
    homeFrame.configure(bg=homePrimaryColor, width=teamFrameSize, height=40)
    homeFrame.place(x=homeFramex, y=bottomy, anchor='sw')  # 293.33

    homeScoreFrame = Frame(wrestOverlay)
    homeScoreFrame.configure(bg=homeSecondColor, width=matchScoreFrameSize, height=40)
    homeScoreFrame.place(x=homeMatchScoreFrame + matchScoreFrameSize, y=bottomy, anchor='se')

    awayFrame = Frame(wrestOverlay)
    awayFrame.configure(bg=awayPrimaryColor, width=teamFrameSize, height=40)
    awayFrame.place(x=awayFramex, y=bottomy, anchor='sw')

    awayScoreFrame = Frame(wrestOverlay)
    awayScoreFrame.configure(bg=awaySecondColor, width=matchScoreFrameSize, height=40)
    awayScoreFrame.place(x=awayMatchScoreFrame + matchScoreFrameSize, y=bottomy, anchor='se')

    hTeamScoreFrame = Frame(wrestOverlay)
    hTeamScoreFrame.config(bg=homeSecondColor, width=matchScoreFrameSize, height=40)
    hTeamScoreFrame.place(x=hTeamScorex, y=bottomy, anchor='sw')

    aTeamScoreFrame = Frame(wrestOverlay)
    aTeamScoreFrame.config(bg=awaySecondColor, width=matchScoreFrameSize, height=40)
    aTeamScoreFrame.place(x=aTeamScorex, y=bottomy, anchor='sw')

    hTeamScoreOverlay = Label(hTeamScoreFrame, text=hTeamScore)
    hTeamScoreOverlay.place(x=(matchScoreFrameSize / 2), y=40, anchor='s')
    hTeamScoreOverlay['bg'] = hTeamScoreOverlay.master['bg']
    hTeamScoreOverlay.config(font=(fFont, 17), fg=yellowColor)

    hTeamNameOverlay = Label(hTeamScoreFrame, text=hAbrev)
    hTeamNameOverlay.place(x=(matchScoreFrameSize / 2), y=0, anchor='n')
    hTeamNameOverlay['bg'] = hTeamNameOverlay.master['bg']
    hTeamNameOverlay.config(font=(fFont, 11), fg='#ffffff')

    aTeamScoreOverlay = Label(aTeamScoreFrame, text=aTeamScore)
    aTeamScoreOverlay.place(x=(matchScoreFrameSize / 2), y=40, anchor='s')
    aTeamScoreOverlay['bg'] = aTeamScoreOverlay.master['bg']
    aTeamScoreOverlay.config(font=(fFont, 17), fg=yellowColor)

    aTeamNameOverlay = Label(aTeamScoreFrame, text=aAbrev)
    aTeamNameOverlay.place(x=(matchScoreFrameSize / 2), y=0, anchor='n')
    aTeamNameOverlay['bg'] = aTeamNameOverlay.master['bg']
    aTeamNameOverlay.config(font=(fFont, 11), fg='#ffffff')

    homeScorewrestOverlay = Label(homeScoreFrame, text=homeScore)
    homeScorewrestOverlay.place(x=(matchScoreFrameSize / 2), y=20, anchor='c')
    homeScorewrestOverlay['bg'] = homeScorewrestOverlay.master['bg']
    homeScorewrestOverlay.config(font=(fFont, 29), fg='#ffffff')

    awayScorewrestOverlay = Label(awayScoreFrame, text=awayScore)
    awayScorewrestOverlay.place(x=(matchScoreFrameSize / 2), y=20, anchor='c')
    awayScorewrestOverlay['bg'] = awayScorewrestOverlay.master['bg']
    awayScorewrestOverlay.config(font=(fFont, 29), fg='#ffffff')

    homeTeamwrestOverlay = Label(homeFrame, text=homeTeam)
    homeTeamwrestOverlay.place(x=10, y=21, anchor='w')
    homeTeamwrestOverlay['bg'] = homeTeamwrestOverlay.master['bg']
    homeTeamwrestOverlay.config(font=(fFont, 16), fg='#ffffff')

    awayTeamwrestOverlay = Label(awayFrame, text=awayTeam)
    awayTeamwrestOverlay.place(x=10, y=21, anchor='w')
    awayTeamwrestOverlay['bg'] = awayTeamwrestOverlay.master['bg']
    awayTeamwrestOverlay.config(font=(fFont, 16), fg='#ffffff')

    swwrestOverlay = StopWatchwrestOverlay(wrestOverlay)
    swwrestOverlay.configure(bg='#000000', width=swOverlayWidth, height=40)
    swwrestOverlay.place(x=swOverlayx, y=bottomy, anchor='sw')

    timeFrame = Frame(wrestOverlay)
    timeFrame.configure(bg='#000000', width=matchScoreFrameSize, height=40)
    timeFrame.place(x=timeFramex, y=bottomy, anchor='sw')

    halfwrestOverlay = Label(timeFrame, text=half)
    halfwrestOverlay.place(x=26, y=20, anchor='c')
    halfwrestOverlay['bg'] = halfwrestOverlay.master['bg']
    halfwrestOverlay.config(font=(fFont, 20), fg='#ffffff')

    weightFrame = Frame(wrestOverlay)
    weightFrame.config(bg='#000000', width=86, height=40)
    weightFrame.place(x=weightFramex, y=bottomy, anchor='sw')

    weightOver = Label(weightFrame, text=weightClass)
    weightOver.place(x=0, y=20, anchor='w')
    weightOver['bg'] = halfwrestOverlay.master['bg']
    weightOver.config(font=(fFont, 20), fg='#ffffff')