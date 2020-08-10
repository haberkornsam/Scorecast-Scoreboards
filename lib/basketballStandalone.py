from tkinter import *
import time
import easygui
import xml.etree.ElementTree as ET
from lib import basketballHost

centerx=300
swx=centerx
swy=10
startx=centerx
starty=40
setClockx=centerx
setClocky=70
enterTimeMx = 250
enterTimeMy = 10
enterTimeColonx = 300
enterTimeColony =12
enterTimeSx = 350
enterTimeSy = 10
homeLabelx = 10
teamLabely=40
awayLabelx = 590
homeScoreLx = 10
teamScoreLy = 100
awayScoreLx =590
teamEditScorey=145
hscore1x = 8
hscore2x = 73
hscore3x = 138
ascore1x = 600-hscore3x
ascore2x = 600-hscore2x
ascore3x = 600-hscore1x
scorey = 222
hFoulLabx = 25
aFoulLabx = 600-hFoulLabx
foulLaby = 270
hFoulLx = 10
FoulLy = 295
aFoulLx = 600-hFoulLx
homeBonusx = 165
awayBonusx = 600-homeBonusx
foulAdy = 290
foulSubty = 315
homePossx = 220
awayPossx = 600-homePossx
homeStaticTOx = 30
awayStaticTOx = 600-homeStaticTOx
staticTOy = 350
hPartTOLabelx = 10
hFullTOLabelx = 80
TOLabely = 390
aPartTOLabelx=600-hFullTOLabelx
aFullTOLabelx=600-hPartTOLabelx
hTakex = 145
aTakex = 600-hTakex
takeParty = 385
takeFully = 410
hcolorx = 15
acolorx = 600-hcolorx
servery = 425
priColory =  450
secColory = 475

fFont = "Lucida Grande"

class StopWatch(Frame):
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
        self.formatted=''
        self.l = Label(self, text=self.formatted, width=20)
        self.l.grid(row=0, column=3, columnspan=3)
        self._setTime(self._elapsedtime)



    def makeWidgets(self):
        """ Make the time label. """


    def _update(self):
        global clockFile
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
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

        self.formatted = str(minutes).zfill(2)+":"+str(seconds).zfill(2)+"."+str(hseconds).zfill(1)
        self._minutes = str(minutes).zfill(2)
        self._seconds = str(seconds).zfill(2)+"."+str(hseconds).zfill(1)
        format = str(minutes).zfill(2)+":"+str(seconds).zfill(2)
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

        self._start = time.time()
        self._setTime(self._elapsedtime)

    def getClockTime(self):
        return self._startingTime-self._elapsedtime

    def getMinutes(self):
        return self._minutes

    def getSeconds(self):
        return self._seconds

class StopWatchbballoverlay(Frame):
    """ Implements a stop watch frame widget. """

    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._startingTime = 1080
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.timeString = ''
        self.makeWidgets()

    def makeWidgets(self):
        global l, teamsHeight
        """ Make the time label. """
        l = Label(self, text=self.timeString, bg='#000000')
        self._setTime(self._elapsedtime)
        l.config(font=(fFont, 22), fg='#dbcf30')
        l.place(x=72,y=17, anchor='c')



    def _update(self):
        global clockFile
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
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

        self._start = time.time()
        self._setTime(self._elapsedtime)

    def getClockTime(self):
        return self._startingTime-self._elapsedtime


def toggleStartLabel(event):
    global runnin
    if runnin == 'Start':
        runnin = 'Stop'
        star.configure(text=runnin)
        sw.Start()
        swbballoverlay.Start()

    else:
        runnin = 'Start'
        star.configure(text=runnin)
        sw.Stop()
        swbballoverlay.Stop()

def changeTime(event):
    global runnin
    sw.Stop()
    swbballoverlay.Stop()
    runnin = "Stop"
    star.configure(text=runnin)
    sw.place_forget()
    enterTimeM.delete(0, END)
    enterTimeS.delete(0, END)
    enterTimeM.place(x=enterTimeMx, y=enterTimeMy, anchor = 'n')
    enterTimeColon.place(x=enterTimeColonx, y=enterTimeColony, anchor = 'n')
    enterTimeS.place(x=enterTimeSx, y=enterTimeSy, anchor = 'n')
    star.place_forget()
    sub.place(x=startx, y=starty, anchor='n')
    setClock.place(x=setClockx, y=setClocky, anchor ='n')

def submitTime(event):
    global runnin
    sw.setClock(enterTimeM.get(), enterTimeS.get())
    swbballoverlay.setClock(enterTimeM.get(), enterTimeS.get())
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
    homeInput.place(x=homeLabelx, y=teamLabely, anchor = 'nw')

def changeAwayTeam(event):
    awayLabel.place_forget()
    awayInput.place(x=awayLabelx, y=teamLabely, anchor = 'ne')

def saveHomeTeam(event):
    global homeTeam
    homeTeam = str(homeInput.get())
    homeInput.place_forget()
    homeLabel.configure(text=homeTeam)
    homeLabel.place(x=homeLabelx, y=teamLabely, anchor = 'nw')
    homeTeambballoverlay.configure(text=homeTeam)
    homeTeambballoverlay.update()

def saveAwayTeam(event):
    global awayTeam
    awayTeam = str(awayInput.get())
    awayInput.place_forget()
    awayLabel.configure(text=awayTeam)
    awayLabel.place(x=awayLabelx, y=teamLabely, anchor = 'ne')
    awayTeambballoverlay.configure(text=awayTeam)
    awayTeambballoverlay.update()

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
    homeScoreL.place(x=homeScoreLx, y=teamScoreLy, anchor='nw')

def awayScoreOverride(event):
    global awayScore
    awayScore = int(aEditScore.get())
    awayScoreFileUpdate()
    aEditScore.place_forget()
    awayScoreL.place(x=awayScoreLx, y=teamScoreLy, anchor='ne')

def homeScoreFileUpdate():
    global homeScore, awayScore
    homeScorebballoverlay.configure(text=homeScore)
    homeScorebballoverlay.update()
    homeScoreL.configure(text=homeScore)

def awayScoreFileUpdate():
    global homeScore, awayScore
    awayScorebballoverlay.configure(text=awayScore)
    awayScorebballoverlay.update()
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


def changeHomeFouls(event):
    hFoulL.place_forget()
    hFoulIn.place(x=hFoulLx, y=FoulLy, anchor='nw')

def changeAwayFouls(event):
    aFoulL.place_forget()
    aFoulIn.place(x=aFoulLx, y=FoulLy, anchor='ne')

def submitHomeFouls(event):
    global hFouls
    hFoulL.place(x=hFoulLx, y=FoulLy, anchor='nw')
    hFoulIn.place_forget()
    hFouls = int(hFoulIn.get())
    homeFoulFileUpdate()

def submitAwayFouls(event):
    global aFouls
    aFoulL.place(x=aFoulLx, y=FoulLy, anchor='ne')
    aFoulIn.place_forget()
    aFouls = int(aFoulIn.get())
    awayFoulFileUpdate()

def addHomeFoul(event):
    global hFouls
    hFouls += 1
    homeFoulFileUpdate()

def addAwayFoul(event):
    global aFouls
    aFouls += 1
    awayFoulFileUpdate()

def subHomeFoul(event):
    global hFouls
    if hFouls>0:
        hFouls-= 1
    homeFoulFileUpdate()

def subtAwayFoul(event):
    global aFouls
    if aFouls>0:
        aFouls -= 1
    awayFoulFileUpdate()

def homeFoulFileUpdate():
    global hFouls, hBonus, homeBonusState, awayBonusState
    hFoulL.configure(text=hFouls)
    hFoulL.update()
    if hFouls >= 7 and hFouls<10:
        awayBonusState='BONUS'
        homeFoulsbballoverlay.config(text='Fouls: '+str(hFouls))
        homeFoulsbballoverlay.update()
    if hFouls >= 10:
        awayBonusState = 'BONUS+'
        homeFoulsbballoverlay.config(text='')
        homeFoulsbballoverlay.update()
    if hFouls<7:
        awayBonusState=''
        homeFoulsbballoverlay.config(text='Fouls: '+str(hFouls))
        homeFoulsbballoverlay.update()
    awayBonus.configure(text=awayBonusState)
    aBonusbballoverlay.configure(text=awayBonusState)
    aBonusbballoverlay.update()

def awayFoulFileUpdate():
    global aFouls, aBonus, awayBonusState, homeBonusState
    aFoulL.configure(text=aFouls)
    aFoulL.update()
    if aFouls >= 7 and aFouls<10:
        homeBonusState='BONUS'
        awayFoulsbballoverlay.configure(text='Fouls: '+str(aFouls))
        awayFoulsbballoverlay.update()
    if aFouls >= 10:
        awayFoulsbballoverlay.configure(text='')
        awayFoulsbballoverlay.update()
        homeBonusState = 'BONUS+'
    if aFouls < 7:
        homeBonusState = ''
        awayFoulsbballoverlay.configure(text='Fouls: '+str(aFouls))
        awayFoulsbballoverlay.update()
    homeBonus.configure(text=homeBonusState)
    hBonusbballoverlay.configure(text=homeBonusState)
    hBonusbballoverlay.update()

def clearTeamFouls(event):
    global hFouls, aFouls
    hFouls=0
    aFouls=0
    homeFoulFileUpdate()
    awayFoulFileUpdate()

def changeHomePoss(event):
    global homePoss, awayPoss
    if homePoss== 'False':
        homePoss = 'True'
        awayPoss = 'False'
    elif homePoss == 'True':
        homePoss = 'False'
    updatePoss()

def changeAwayPoss(event):
    global awayPoss, homePoss
    if awayPoss=='False':
        awayPoss = 'True'
        homePoss = 'False'
    elif awayPoss == 'True':
        awayPoss = 'False'
    updatePoss()

def updatePoss():
    global awayPoss, homePoss
    if awayPoss == 'True':
        awayPossession.configure(text='Poss\n -->')
        awayPossBar.place(x=0, y=0, anchor='nw')

    if awayPoss == 'False':

        awayPossession.configure(text='Poss\n')
        awayPossBar.place_forget()
    if homePoss == 'True':

        homePossession.configure(text='Poss\n<--')
        homePossBar.place(x=0,y=0,anchor='nw')
    if homePoss=='False':

        homePossession.configure(text='Poss\n')
        homePossBar.place_forget()

def changeHalf(event):
    halfLabel.place_forget()
    halfIn.place(x=centerx, y=teamEditScorey, anchor='n')

def submitHalf(event):
    global half
    halfIn.place_forget()
    halfLabel.place(x=centerx, y=teamEditScorey, anchor='n')
    half = str(halfIn.get())
    halfLabel.configure(text=half)
    halfbballoverlay.configure(text=str(half))
    halfbballoverlay.update()


def homeTOFileUpdate():
    global homeFullTO, homePartTO, homeTOFrames, totalTO
    combTO = int(homeFullTO)+int(homePartTO)

    for i in range(totalTO):
        if i<combTO:
            homeTOFrames[i].configure(bg='#ffffff')
        else:
            homeTOFrames[i].configure(bg='#3C3F41')

    homePartTOLabel.configure(text='Partial:\n'+str(homePartTO))
    homeFullTOLabel.configure(text='Full:\n'+str(homeFullTO))

def awayTOFileUpdate():
    global awayFullTO, awayPartTO
    combTO = int(awayFullTO)+int(awayPartTO)
    for i in range(totalTO):
        if i<combTO:
            awayTOFrames[i].configure(bg='#ffffff')
        else:
            awayTOFrames[i].configure(bg='#3C3F41')
    awayPartTOLabel.configure(text='Partial:\n'+str(awayPartTO))
    awayFullTOLabel.configure(text='Full:\n'+str(awayFullTO))

def editPartHomeTO(event):
    homePartTOIn.place(x=hPartTOLabelx, y=TOLabely, anchor='nw')
    homePartTOLabel.place_forget()

def editPartAwayTO(event):
    awayPartTOIn.place(x=aPartTOLabelx, y=TOLabely, anchor='ne')
    awayPartTOLabel.place_forget()

def editFullHomeTO(event):
    homeFullTOIn.place(x=hFullTOLabelx, y=TOLabely, anchor='nw')
    homeFullTOLabel.place_forget()

def editFullAwayTO(event):
    awayFullTOIn.place(x=aFullTOLabelx, y=TOLabely, anchor='ne')
    awayFullTOLabel.place_forget()

def submitPartHomeTO(event):
    global homePartTO
    homePartTO = int(homePartTOIn.get())
    homePartTOLabel.place(x=hPartTOLabelx, y=TOLabely, anchor='nw')
    homePartTOIn.place_forget()
    homeTOFileUpdate()

def submitPartAwayTO(event):
    global awayPartTO
    awayPartTO = int(awayPartTOIn.get())
    awayPartTOLabel.place(x=aPartTOLabelx, y=TOLabely, anchor='ne')
    awayPartTOIn.place_forget()
    awayTOFileUpdate()

def submitFullHomeTO(event):
    global homeFullTO
    homeFullTO = int(homeFullTOIn.get())
    homeFullTOLabel.place(x=hFullTOLabelx, y=TOLabely, anchor='nw')
    homeFullTOIn.place_forget()
    homeTOFileUpdate()

def submitFullAwayTO(event):
    global awayFullTO
    awayFullTO=int(awayFullTOIn.get())
    awayFullTOLabel.place(x=aFullTOLabelx, y=TOLabely, anchor='ne')
    awayFullTOIn.place_forget()
    awayTOFileUpdate()

def takeHomePart(event):
    global homePartTO
    if homePartTO > 0:
        homePartTO -= 1
    homeTOFileUpdate()

def takeAwayPart(event):
    global awayPartTO
    if awayPartTO > 0:
        awayPartTO -=1
    awayTOFileUpdate()

def takeHomeFUll(event):
    global homeFullTO
    if homeFullTO > 0:
        homeFullTO -= 1
    homeTOFileUpdate()

def takeAwayFull(event):
    global awayFullTO
    if awayFullTO > 0:
        awayFullTO -= 1
    awayTOFileUpdate()


def changeHPrimary(event):
    setHPrimary.place_forget()
    hPriIn.place(x=hcolorx, y=priColory, anchor='nw')
def changeHSecond(event):
    setHSecond.place_forget()
    hSecIn.place(x=hcolorx, y=secColory, anchor='nw')
def changeAPrimary(event):
    setAPrimary.place_forget()
    aPriIn.place(x=acolorx, y=priColory, anchor = 'ne')
def changeASecond(event):
    setASecond.place_forget()
    aSecIn.place(x=acolorx, y=secColory, anchor='ne')
def subHP(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    homePrimaryColor = str(hPriIn.get())
    if (homePrimaryColor[0]!='#'):
        homePrimaryColor='#'+homePrimaryColor
    if (len(homePrimaryColor)!=7):
        return
    try:
        homeFrame.configure(bg=homePrimaryColor)
    except:
        return
    homeTeambballoverlay['bg'] = homeTeambballoverlay.master['bg']
    hPriIn.place_forget()
    setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')
def subHS(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    homeSecondColor = str(hSecIn.get())
    if homeSecondColor[0]!='#':
        homeSecondColor='#'+homeSecondColor
    if len(homeSecondColor)!=7:
        return
    try:
        homeScoreFrame.configure(bg=homeSecondColor)
    except:
        return

    homeScorebballoverlay['bg'] = homeScorebballoverlay.master['bg']
    hSecIn.place_forget()
    setHSecond.place(x=hcolorx, y=secColory, anchor='nw')

def subAP(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    awayPrimaryColor = str(aPriIn.get())
    if (awayPrimaryColor[0]!='#'):
        awayPrimaryColor='#'+awayPrimaryColor
    if len(awayPrimaryColor) != 7:
        return
    try:
        awayFrame.configure(bg=awayPrimaryColor)
    except:
        return
    awayTeambballoverlay['bg']=awayTeambballoverlay.master['bg']
    aPriIn.place_forget()
    setAPrimary.place(x=acolorx, y=priColory, anchor = 'ne')

def subAS(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    awaySecondColor = str(aSecIn.get())
    if (awaySecondColor[0]!='#'):
        awaySecondColor='#'+awaySecondColor
    if (len(awaySecondColor)!=7):
        return
    try:
        awayScoreFrame.configure(bg=awaySecondColor)
    except:
        return
    awayScorebballoverlay.configure(bg=awaySecondColor)
    aSecIn.place_forget()
    setASecond.place(x=acolorx, y=secColory, anchor='ne')

def updateTeamNames():
    homeLabel.configure(text=homeTeam)
    homeTeambballoverlay.configure(text=homeTeam)
    awayLabel.configure(text=awayTeam)
    awayTeambballoverlay.configure(text=awayTeam)

def updateColors():
    homeFrame.configure(bg=homePrimaryColor)
    homeTeambballoverlay['bg'] = homeTeambballoverlay.master['bg']
    homeScoreFrame.configure(bg=homeSecondColor)
    homeScorebballoverlay['bg'] = homeScorebballoverlay.master['bg']
    awayFrame.configure(bg=awayPrimaryColor)
    awayTeambballoverlay['bg'] = awayTeambballoverlay.master['bg']
    awayScoreFrame.configure(bg=awaySecondColor)
    awayScorebballoverlay.configure(bg=awaySecondColor)



def updateLabels():
    updateTeamNames()
    homeScoreFileUpdate()
    awayScoreFileUpdate()
    homeFoulFileUpdate()
    awayFoulFileUpdate()
    updatePoss()
    homeTOFileUpdate()
    awayTOFileUpdate()
    updateColors()




def openConfig(event=None):
    global homeTeam, awayTeam, homeScore, awayScore, aFouls, hFouls, half, homePoss, awayPoss, homePartTO, awayPartTO, \
        homeFullTO, awayFullTO,homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, sw
    tree = ET.parse(easygui.fileopenbox(filetypes = ['*.xml'])).getroot()
    if(tree.tag=='basketball'):
        homeTeam=tree[0][0].text
        homeScore=int(tree[0][1].text)
        hFouls=int(tree[0][2].text)
        homePoss=str(tree[0][3].text)
        homePartTO=int(tree[0][4].text)
        homeFullTO=int(tree[0][5].text)
        homePrimaryColor=tree[0][6].text
        homeSecondColor=tree[0][7].text
        awayTeam=tree[1][0].text
        awayScore = int(tree[1][1].text)
        aFouls = int(tree[1][2].text)
        awayPoss = str(tree[1][3].text)
        awayPartTO = int(tree[1][4].text)
        awayFullTO = int(tree[1][5].text)
        awayPrimaryColor = tree[1][6].text
        awaySecondColor = tree[1][7].text
        half = tree[2].text
        sw.setClock(int(tree[3][0].text), float(tree[3][1].text))
        swbballoverlay.setClock(int(tree[3][0].text), float(tree[3][1].text))
        updateLabels()


def saveConfig(event=None):
    global homeTeam, awayTeam, homeScore, awayScore, aFouls, hFouls, half, homePoss, awayPoss, homePartTO, awayPartTO, \
        homeFullTO, awayFullTO, homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, sw
    basketball = ET.Element('basketball')
    homeTeam1 = ET.SubElement(basketball, 'homeTeam')
    hname1 = ET.SubElement(homeTeam1, 'name')
    hname1.text = str(homeTeam)
    hscore1 = ET.SubElement(homeTeam1, 'score')
    hscore1.text = str(homeScore)
    hfouls1 = ET.SubElement(homeTeam1, 'fouls')
    hfouls1.text = str(hFouls)
    hPoss1 = ET.SubElement(homeTeam1, 'possession')
    hPoss1.text = str(homePoss)
    hPart1 = ET.SubElement(homeTeam1, 'partialTimeOuts')
    hPart1.text = str(homePartTO)
    hFull1 = ET.SubElement(homeTeam1, 'fullTimeOuts')
    hFull1.text = str(homeFullTO)
    hpriColor1 = ET.SubElement(homeTeam1, 'primaryColor')
    hpriColor1.text = str(homePrimaryColor)
    hsecColor1 = ET.SubElement(homeTeam1, 'secondaryColor')
    hsecColor1.text = str(homeSecondColor)

    awayTeam1 = ET.SubElement(basketball, 'awayTeam')
    aname1 = ET.SubElement(awayTeam1, 'name')
    aname1.text = str(awayTeam)
    ascore1 = ET.SubElement(awayTeam1, 'score')
    ascore1.text = str(awayScore)
    afouls1 = ET.SubElement(awayTeam1, 'fouls')
    afouls1.text = str(aFouls)
    aPoss1 = ET.SubElement(awayTeam1, 'possession')
    aPoss1.text = str(awayPoss)
    aPart1 = ET.SubElement(awayTeam1, 'partialTimeOuts')
    aPart1.text = str(awayPartTO)
    aFull1 = ET.SubElement(awayTeam1, 'fullTimeOuts')
    aFull1.text = str(awayFullTO)
    apriColor1 = ET.SubElement(awayTeam1, 'primaryColor')
    apriColor1.text = str(awayPrimaryColor)
    asecColor1 = ET.SubElement(awayTeam1, 'secondaryColor')
    asecColor1.text = str(awaySecondColor)

    half1 = ET.SubElement(basketball, 'Half')
    half1.text = str(half)
    clock1 = ET.SubElement(basketball, 'Clock')
    minutes1 = ET.SubElement(clock1, 'Minutes')
    minutes1.text = str(sw.getMinutes())
    seconds1 = ET.SubElement(clock1, 'Seconds')
    seconds1.text = str(sw.getSeconds())

    myData = ET.tostring(basketball).decode("utf-8")
    configFile = open(easygui.filesavebox() + '.xml', 'w')
    configFile.write(myData)


def submitPort(event):
    port = int(portIn.get())
    try:
        if port<1000 or port>10000:
            return
    except:
        return
    data = []
    data.append(homeTeam)
    data.append(awayTeam)
    data.append(homeScore)
    data.append(awayScore)
    data.append(hFouls)
    data.append(aFouls)
    data.append(homeBonusState)
    data.append(awayBonusState)
    data.append(half)
    data.append(homePoss)
    data.append(awayPoss)
    data.append(homePartTO)
    data.append(homeFullTO)
    data.append(awayPartTO)
    data.append(awayFullTO)
    data.append(homePrimaryColor)
    data.append(homeSecondColor)
    data.append(awayPrimaryColor)
    data.append(awaySecondColor)
    data.append(sw.getMinutes())
    data.append(sw.getSeconds())
    data.append(totalTO)

    bballoverlay.destroy()
    basketballCtrl.destroy()
    serverSet.destroy()
    basketballHost.start(port, data)

overlayWindowWidth = 1280
overlayWindowHeight = 120

def quitProgram(event=None):
    basketballCtrl.destroy()
    bballoverlay.destroy()


def openServerSettings(event=None):
    global portIn, serverSet
    serverSet = Tk()
    serverSet.configure(bg='#000000')
    serverSet.title("Scorecast Server")
    serverSet.geometry("130x100")

    Label(serverSet, text='Server', fg='#ffffff', bg='#000000').place(x=130/2, y=15, anchor='c')

    portSubmit=Label(serverSet, text='Start')
    portSubmit.bind("<Button-1>", submitPort)
    portSubmit.place(x=130/2, y=80, anchor='c')

    portIn=Entry(serverSet, width=7)
    portIn.bind("<Return>", submitPort)
    portIn.place(x=85, y=50, anchor='c')

    portLabel=Label(serverSet, bg='#000000', text='Port: ', fg='#ffffff')
    portLabel.place(x=25, y=50, anchor='c')



def start(data = None):
    global runnin, clockFile, sw, enterTimeM, star, sub, submit, enterTimeS, setClock, enterTimeColon, \
        homeLabel, homeTeam, awayLabel, awayTeam, homeSave, awaySave, homeInput, awayInput, homeScoreL, awayScoreL, \
        homeScore, awayScore, homeScore1, homeScore2, homeScore3, awayScore1, awayScore2, awayScore3, hEditScore, \
        aEditScore, awayEditScoreSave, homeEditScoreSave, hFoulL, hFouls, aFoulL, aFouls, hFoulIn, hFoulSubm, hBonus, \
        aFoulIn, aFoulSubm, homeBonusState, awayBonusState, homeBonus, awayBonus, half, halfLabel, halfIn, homePoss, \
        awayPoss, homePossession, awayPossession, homePartTO, awayPartTO, homeFullTO, awayFullTO, homePartTOLabel, \
        homePartTOIn, awayPartTOLabel, homeFullTOLabel, homeFullTOIn, awayFullTOLabel, awayPartTOIn, awayFullTOIn, \
        swbballoverlay, homeTeambballoverlay, awayTeambballoverlay, homeScorebballoverlay, awayScorebballoverlay, homeFoulsCnt, awayFoulsCnt, \
        hBonusbballoverlay, aBonusbballoverlay, halfbballoverlay, homeTO1, homeTO2, homeTO3, homeTO4, homeTO5, awayTO1, awayTO2, \
        awayTO3, awayTO4, awayTO5, setHPrimary, setHSecond, setAPrimary, setASecond, hSecIn, hPriIn, aSecIn, aPriIn, \
        homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, homeFrame, awayFrame, homeScoreFrame, \
        awayScoreFrame, portEntry, portLabel, portSubmit, serverLabel, basketballCtrl, bballoverlay, homeFoulsbballoverlay, \
        awayFoulsbballoverlay, teamsHeight, homeTOFrames, awayTOFrames, totalTO, homePossBar, awayPossBar
    basketballCtrl = Tk()
    basketballCtrl.configure(bg='#000000')
    basketballCtrl.title("Scorecast Basketball Scoreboard Controller")
    basketballCtrl.geometry('600x510')
    bballoverlay = Tk()
    bballoverlay.configure(bg='#00ff00')
    bballoverlay.geometry('1280x120')
    bballoverlay.title('Scorecast Basketball Scoreboard')
    sw = StopWatch(basketballCtrl)
    sw.place(x=300, y=10, anchor='n')


    if data == None:
    # default variables
        runnin = 'Start'
        homeTeam = 'HOME'
        awayTeam = 'VISITOR'
        homeScore = 0
        awayScore = 0
        hFouls = 0
        aFouls = 0
        homeBonusState = ''
        awayBonusState = ''
        half = '1st Half'
        homePoss = 'False'
        awayPoss = 'False'
        homePartTO = 2
        homeFullTO = 3
        awayPartTO = 2
        awayFullTO = 3

        totalTO = 5

        homePrimaryColor = '#c1a551'
        homeSecondColor = '#877338'
        awayPrimaryColor = '#110b5d'
        awaySecondColor = '#0d084a'

    else:
        runnin = 'Start'
        homeTeam = data[0]
        awayTeam = data[1]
        homeScore = data[2]
        awayScore = data[3]
        hFouls = data[4]
        aFouls = data[5]
        homeBonusState = data[6]
        awayBonusState = data[7]
        half = data[8]
        homePoss = data[9]
        awayPoss = data[10]
        homePartTO = data[11]
        homeFullTO = data[12]
        awayPartTO = data[13]
        awayFullTO = data[14]
        totalTO = data[15]
        homePrimaryColor = data[16]
        homeSecondColor = data[17]
        awayPrimaryColor = data[18]
        awaySecondColor = data[19]

        #add clock stuff


    yellowColor='#dbcf30'

    # start button
    star = Label(basketballCtrl, text=runnin, width=20)
    star.bind('<Button-1>', toggleStartLabel)
    star.place(x=startx, y=starty, anchor='n')

    # set Clock Button
    setClock = Label(basketballCtrl, text='Set Time', width=20)
    setClock.bind('<Button-1>', changeTime)
    setClock.place(x=setClockx, y=setClocky, anchor='n')

    # Enter time entries
    enterTimeM = Entry(basketballCtrl, text='mm', width=5)
    enterTimeM.place(x=enterTimeMx, y=enterTimeMy, anchor='n')
    enterTimeM.place_forget()
    enterTimeColon = Label(basketballCtrl, text=':', width=3)
    enterTimeColon.place(x=enterTimeColonx, y=enterTimeColony, anchor='n')
    enterTimeColon.place_forget()
    enterTimeS = Entry(basketballCtrl, text="ss", width=5)
    enterTimeS.place(x=enterTimeSx, y=enterTimeSy, anchor='n')
    enterTimeS.place_forget()

    # submit time button
    sub = Label(basketballCtrl, text="Submit", width=20)
    sub.bind('<Button-1>', submitTime)
    sub.place_forget()

    # Team Name Labels including Changing Names
    homeLabel = Label(basketballCtrl, text=homeTeam, width=20)
    homeLabel.bind('<Button-1>', changeHomeTeam)
    homeLabel.place(x=homeLabelx, y=teamLabely, anchor='nw')
    awayLabel = Label(basketballCtrl, text=awayTeam, width=20)
    awayLabel.bind('<Button-1>', changeAwayTeam)
    awayLabel.place(x=awayLabelx, y=teamLabely, anchor='ne')

    # New team Name Inputs
    homeInput = Entry(basketballCtrl, width=19)
    homeInput.bind('<Return>', saveHomeTeam)
    homeInput.place_forget()
    awayInput = Entry(basketballCtrl, width=19)
    awayInput.bind('<Return>', saveAwayTeam)
    awayInput.place_forget()

    # Score Elements
    # Score Labels
    homeScoreL = Label(basketballCtrl, text=00, width=20, height=7)
    homeScoreL.bind("<Button-1>", editHomeScore)
    homeScoreL.place(x=homeScoreLx, y=teamScoreLy, anchor='nw')
    awayScoreL = Label(basketballCtrl, text=00, width=20, height=7)
    awayScoreL.bind("<Button-1>", editAwayScore)
    awayScoreL.place(x=awayScoreLx, y=teamScoreLy, anchor='ne')

    # Edit Scores
    hEditScore = Entry(basketballCtrl, width=19)
    hEditScore.bind('<Return>', homeScoreOverride)
    hEditScore.place_forget()
    aEditScore = Entry(basketballCtrl, width=19)
    aEditScore.bind('<Return>', awayScoreOverride)
    aEditScore.place_forget()

    # Increase Score Buttons
    homeScore1 = Label(basketballCtrl, text='+1', width=6)
    homeScore1.bind("<Button-1>", hScore1)
    homeScore1.place(x=hscore1x, y=scorey, anchor='nw')
    homeScore2 = Label(basketballCtrl, text='+2', width=6)
    homeScore2.bind("<Button-1>", hScore2)
    homeScore2.place(x=hscore2x, y=scorey, anchor='nw')
    homeScore3 = Label(basketballCtrl, text='+3', width=6)
    homeScore3.bind("<Button-1>", hScore3)
    homeScore3.place(x=hscore3x, y=scorey, anchor='nw')

    awayScore1 = Label(basketballCtrl, text='+1', width=6)
    awayScore1.bind("<Button-1>", aScore1)
    awayScore1.place(x=ascore1x, y=scorey, anchor='ne')
    awayScore2 = Label(basketballCtrl, text='+2', width=6)
    awayScore2.bind("<Button-1>", aScore2)
    awayScore2.place(x=ascore2x, y=scorey, anchor='ne')
    awayScore3 = Label(basketballCtrl, text='+3', width=6)
    awayScore3.bind("<Button-1>", aScore3)
    awayScore3.place(x=ascore3x, y=scorey, anchor='ne')

    # Foul elements
    # Team Foul Labels
    hFoulLab = Label(basketballCtrl, text='Home Fouls', fg='#ffffff', bg='#000000')
    hFoulLab.place(x=hFoulLabx, y=foulLaby, anchor='nw')
    aFoulLab = Label(basketballCtrl, text='Away Fouls', fg='#ffffff', bg='#000000')
    aFoulLab.place(x=aFoulLabx, y=foulLaby, anchor='ne')

    # Number of Fouls
    hFoulL = Label(basketballCtrl, text=hFouls, width=12, height=2)
    hFoulL.bind('<Button-1>', changeHomeFouls)
    hFoulL.place(x=hFoulLx, y=FoulLy, anchor='nw')
    aFoulL = Label(basketballCtrl, text=aFouls, width=12, height=2)
    aFoulL.bind('<Button-1>', changeAwayFouls)
    aFoulL.place(x=aFoulLx, y=FoulLy, anchor='ne')

    # Foul Inputs
    hFoulIn = Entry(basketballCtrl, width=12)
    hFoulIn.bind('<Return>', submitHomeFouls)
    hFoulIn.place(x=hFoulLx, y=FoulLy, anchor='nw')
    hFoulIn.place_forget()
    aFoulIn = Entry(basketballCtrl, width=12)
    aFoulIn.bind('<Return>', submitAwayFouls)
    aFoulIn.place(x=aFoulLx, y=FoulLy, anchor='ne')
    aFoulIn.place_forget()

    # Bonus Labels
    homeBonus = Label(basketballCtrl, text=homeBonusState, width=7, fg='#ffffff', bg='#000000')
    homeBonus.place(x=homeBonusx, y=foulLaby, anchor='n')
    awayBonus = Label(basketballCtrl, text=awayBonusState, width=7, fg='#ffffff', bg='#000000')
    awayBonus.place(x=awayBonusx, y=foulLaby, anchor='n')

    # Add Foul Buttons
    hFoulAd = Label(basketballCtrl, text="+1", width=6)
    hFoulAd.bind('<Button-1>', addHomeFoul)
    hFoulAd.place(x=homeBonusx, y=foulAdy, anchor='n')
    aFoulAd = Label(basketballCtrl, text="+1", width=6)
    aFoulAd.bind('<Button-1>', addAwayFoul)
    aFoulAd.place(x=awayBonusx, y=foulAdy, anchor='n')

    # Subtract Foul Buttons
    hFoulSubt = Label(basketballCtrl, text='-1', width=6)
    hFoulSubt.bind('<Button-1>', subHomeFoul)
    hFoulSubt.place(x=homeBonusx, y=foulSubty, anchor='n')

    aFoulSubt = Label(basketballCtrl, text='-1', width=6)
    aFoulSubt.bind('<Button-1>', subtAwayFoul)
    aFoulSubt.place(x=awayBonusx, y=foulSubty, anchor='n')

    # Clear Team Fouls
    clearFoulsLabel = Label(basketballCtrl, text='Clear Team Fouls', width=13)
    clearFoulsLabel.bind('<Button-1>', clearTeamFouls)
    clearFoulsLabel.place(x=centerx, y=foulSubty, anchor='c')

    # Period Buttons
    halfLabel = Label(basketballCtrl, text=half, width=5)
    halfLabel.bind('<Button-1>', changeHalf)
    halfLabel.place(x=centerx, y=teamEditScorey, anchor='n')

    # Period Input
    halfIn = Entry(basketballCtrl, width=5)
    halfIn.bind('<Return>', submitHalf)
    halfIn.place_forget()

    # possession buttons
    homePossession = Label(basketballCtrl, text="Poss\n", width=5)
    homePossession.bind('<Button-1>', changeHomePoss)
    homePossession.place(x=homePossx, y=teamEditScorey, anchor='nw')

    awayPossession = Label(basketballCtrl, text="Poss\n", width=5)
    awayPossession.bind('<Button-1>', changeAwayPoss)
    awayPossession.place(x=awayPossx, y=teamEditScorey, anchor='ne')

    # static timeout titles
    homeTOLabel = Label(basketballCtrl, text='\nHome Timeouts', fg='#ffffff', bg='#000000')
    homeTOLabel.place(x=homeStaticTOx, y=staticTOy, anchor='nw')
    awayTOLabel = Label(basketballCtrl, text='\nAway Timeouts', fg='#ffffff', bg='#000000')
    awayTOLabel.place(x=awayStaticTOx, y=staticTOy, anchor='ne')

    # timeout updating
    homePartTOLabel = Label(basketballCtrl, text='Partial:\n' + str(homePartTO), width=6)
    homePartTOLabel.bind('<Button-1>', editPartHomeTO)
    homePartTOLabel.place(x=hPartTOLabelx, y=TOLabely, anchor='nw')

    homeFullTOLabel = Label(basketballCtrl, text='Full:\n' + str(homeFullTO), width=6)
    homeFullTOLabel.bind('<Button-1>', editFullHomeTO)
    homeFullTOLabel.place(x=hFullTOLabelx, y=TOLabely, anchor='nw')

    awayPartTOLabel = Label(basketballCtrl, text='Partial:\n' + str(awayPartTO), width=6)
    awayPartTOLabel.bind("<Button-1>", editPartAwayTO)
    awayPartTOLabel.place(x=aPartTOLabelx, y=TOLabely, anchor='ne')

    awayFullTOLabel = Label(basketballCtrl, text='Full:\n' + str(awayFullTO), width=6)
    awayFullTOLabel.bind("<Button-1>", editFullAwayTO)
    awayFullTOLabel.place(x=aFullTOLabelx, y=TOLabely, anchor='ne')

    homeTakePart = Label(basketballCtrl, text='Partial', width=6)
    homeTakePart.bind('<Button-1>', takeHomePart)
    homeTakePart.place(x=hTakex, y=takeParty, anchor='nw')

    homeTakeFull = Label(basketballCtrl, text='Full', width=6)
    homeTakeFull.bind('<Button-1>', takeHomeFUll)
    homeTakeFull.place(x=hTakex, y=takeFully, anchor='nw')

    awayTakePart = Label(basketballCtrl, text="Partial", width=6)
    awayTakePart.bind("<Button-1>", takeAwayPart)
    awayTakePart.place(x=aTakex, y=takeParty, anchor='ne')

    awayTakeFull = Label(basketballCtrl, text='Full', width=6)
    awayTakeFull.bind('<Button-1>', takeAwayFull)
    awayTakeFull.place(x=aTakex, y=takeFully, anchor='ne')

    homePartTOIn = Entry(basketballCtrl, width=4)
    homePartTOIn.bind('<Return>', submitPartHomeTO)
    homePartTOIn.place(x=hPartTOLabelx, y=TOLabely, anchor='nw')
    homePartTOIn.place_forget()

    awayPartTOIn = Entry(basketballCtrl, width=4)
    awayPartTOIn.bind('<Return>', submitPartAwayTO)
    awayPartTOIn.place(x=aPartTOLabelx, y=TOLabely, anchor='ne')
    awayPartTOIn.place_forget()

    homeFullTOIn = Entry(basketballCtrl, width=4)
    homeFullTOIn.bind('<Return>', submitFullHomeTO)
    homeFullTOIn.place(x=hFullTOLabelx, y=TOLabely, anchor='nw')
    homeFullTOIn.place_forget()

    awayFullTOIn = Entry(basketballCtrl, width=4)
    awayFullTOIn.bind('<Return>', submitFullAwayTO)
    awayFullTOIn.place(x=aFullTOLabelx, y=TOLabely, anchor='ne')
    awayFullTOIn.place_forget()

    # color changing
    setHPrimary = Label(basketballCtrl, text="Set Home Primary Color", width=20)
    setHPrimary.bind('<Button-1>', changeHPrimary)
    setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')

    setHSecond = Label(basketballCtrl, text="Set Home Secondary Color", width=20)
    setHSecond.bind('<Button-1>', changeHSecond)
    setHSecond.place(x=hcolorx, y=secColory, anchor='nw')

    setAPrimary = Label(basketballCtrl, text="Set Away Primary Color", width=20)
    setAPrimary.bind('<Button-1>', changeAPrimary)
    setAPrimary.place(x=acolorx, y=priColory, anchor='ne')

    setASecond = Label(basketballCtrl, text='Set Away Secondary Color', width=20)
    setASecond.bind('<Button-1>', changeASecond)
    setASecond.place(x=acolorx, y=secColory, anchor='ne')

    hPriIn = Entry(basketballCtrl, width=18)
    hPriIn.bind('<Return>', subHP)
    hPriIn.place_forget()

    hSecIn = Entry(basketballCtrl, width=18)
    hSecIn.bind('<Return>', subHS)
    hSecIn.place_forget()

    aPriIn = Entry(basketballCtrl, width=18)
    aPriIn.bind('<Return>', subAP)
    aPriIn.place_forget()

    aSecIn = Entry(basketballCtrl, width=18)
    aSecIn.bind('<Return>', subAS)
    aSecIn.place_forget()





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








    homeFrame = Frame(bballoverlay)
    homeFrame.configure(bg=homePrimaryColor, width=teamFrameWidth, height=teamsHeight)
    homeFrame.place(x=homeTeamx, y=centerLine, anchor='sw')  # 293.33

    homeScoreFrame = Frame(bballoverlay)
    homeScoreFrame.configure(bg=homeSecondColor, width=scoreFrameWidth, height=teamsHeight)
    homeScoreFrame.place(x=homeScorex, y=centerLine, anchor='sw')

    awayFrame = Frame(bballoverlay)
    awayFrame.configure(bg=awayPrimaryColor, width=teamFrameWidth, height=teamsHeight)
    awayFrame.place(x=awayTeamx, y=centerLine, anchor='sw')

    awayScoreFrame = Frame(bballoverlay)
    awayScoreFrame.configure(bg=awaySecondColor, width=scoreFrameWidth, height=teamsHeight)
    awayScoreFrame.place(x=awayScorex, y=centerLine, anchor='sw')

    periodFrame = Frame(bballoverlay)
    periodFrame.configure(bg='#000000', width=periodFrameWidth, height=teamsHeight)
    periodFrame.place(x=periodFramex, y=centerLine, anchor='sw')


    swbballoverlay = StopWatchbballoverlay(bballoverlay)
    swbballoverlay.configure(bg='#000000', width=timeFrameWidth, height=teamsHeight)
    swbballoverlay.place(x=timeFramex, y=centerLine, anchor='sw')

    foulFrame=Frame(bballoverlay)
    foulFrame.configure(bg='#000000', width=overlayWidth, height=extrasHeight)  # '#473c34'
    foulFrame.place(x=homeTeamx, y=centerLine, anchor='nw')


    homeScorebballoverlay = Label(homeScoreFrame, text=homeScore)
    homeScorebballoverlay.place(x=scoreFrameWidth/2, y=((teamsHeight+possBarHeight)/2), anchor='c')
    homeScorebballoverlay['bg'] = homeScorebballoverlay.master['bg']
    homeScorebballoverlay.config(font=(fFont, 27), fg='#ffffff')

    homePossBar=Frame(homeScoreFrame)
    homePossBar.config(bg=yellowColor, width=scoreFrameWidth, height=possBarHeight)
    if (homePoss=='True'):
        homePossBar.place(x=0, y=0, anchor='nw')

    awayScorebballoverlay = Label(awayScoreFrame, text=awayScore)
    awayScorebballoverlay.place(x=scoreFrameWidth/2, y=((teamsHeight+possBarHeight)/2), anchor='c')
    awayScorebballoverlay['bg'] = awayScorebballoverlay.master['bg']
    awayScorebballoverlay.config(font=(fFont, 27), fg='#ffffff')


    awayPossBar = Frame(awayScoreFrame)
    awayPossBar.configure(bg=yellowColor, width=scoreFrameWidth, height=possBarHeight)
    if(awayPoss=='True'):
        awayPossBar.place(x=0,y=0,anchor='nw')


    homeTeambballoverlay = Label(homeFrame, text=homeTeam)
    homeTeambballoverlay.place(x=20, y=teamsHeight/2, anchor='w')
    homeTeambballoverlay['bg'] = homeTeambballoverlay.master['bg']
    homeTeambballoverlay.config(font=(fFont, 18), fg='#ffffff')

    awayTeambballoverlay = Label(awayFrame, text=awayTeam)
    awayTeambballoverlay.place(x=20, y=teamsHeight/2, anchor='w')
    awayTeambballoverlay['bg'] = awayTeambballoverlay.master['bg']
    awayTeambballoverlay.config(font=(fFont, 18), fg='#ffffff')

    homeFoulsbballoverlay = Label(foulFrame, text='Fouls: '+str(hFouls), fg='#ffffff')
    homeFoulsbballoverlay.place(x=homeFoulxOverlay, y=extrasY, anchor='c')
    homeFoulsbballoverlay['bg'] = '#000000'
    homeFoulsbballoverlay.config(font=(fFont, 12), fg='#ffffff')


    awayFoulsbballoverlay = Label(foulFrame, text='Fouls: '+str(aFouls))
    awayFoulsbballoverlay.place(x=awayFoulxOverlay, y=extrasY, anchor='c')
    awayFoulsbballoverlay['bg'] = '#000000'
    awayFoulsbballoverlay.config(font=(fFont, 12), fg='#ffffff')


    halfbballoverlay = Label(periodFrame, text=half)
    halfbballoverlay.place(x=20, y=teamsHeight/2, anchor='w')
    halfbballoverlay['bg'] = halfbballoverlay.master['bg']
    halfbballoverlay.config(font=(fFont, 20), fg='#ffffff')

    hBonusbballoverlay = Label(foulFrame, text=homeBonusState)
    hBonusbballoverlay.place(x=homeBonusxOverlay, y=extrasY, anchor='c')
    hBonusbballoverlay.config(font=(fFont, 12), fg='#dbcf30')
    hBonusbballoverlay['bg'] = hBonusbballoverlay.master['bg']

    aBonusbballoverlay = Label(foulFrame, text=awayBonusState)
    aBonusbballoverlay.place(x=awayBonusxOverlay, y=extrasY, anchor='c')
    aBonusbballoverlay.config(font=(fFont, 12), fg='#dbcf30')
    aBonusbballoverlay['bg'] = aBonusbballoverlay.master['bg']

    toBarWidth=((teamFrameWidth-scoreFrameWidth)/totalTO)-5

    if toBarWidth>35:
        toBarWidth=35

    homeToBarStart=((teamFrameWidth-scoreFrameWidth)/2)-((toBarWidth+3)*(totalTO/2))


    homeTOFrames = []

    for i in range(totalTO):
        toBar=Frame(foulFrame)
        toBar.config(width=toBarWidth, height=possBarHeight)
        if i<homeFullTO+homePartTO:
            toBar.configure(bg='#ffffff')
        else:
            toBar.configure(bg='#3C3F41')
        toBar.place(x=homeToBarStart+((toBarWidth+5)*i), y=extrasY, anchor='w')
        homeTOFrames.append(toBar)


    awayToBarStart=homeToBarStart+teamFrameWidth+scoreFrameWidth+2

    awayTOFrames = []

    for i in range(totalTO):
        toBar = Frame(foulFrame)
        toBar.config(width=toBarWidth, height=possBarHeight)
        if i<awayFullTO+awayPartTO:
            toBar.configure(bg='#ffffff')
        else:
            toBar.configure(bg='#3C3F41')
        toBar.place(x=awayToBarStart+((toBarWidth+5)*i), y=extrasY, anchor='w')
        awayTOFrames.append(toBar)

    if data != None:
        sw.setClock(data[20],data[21])
        swbballoverlay.setClock(data[20], data[21])

    #menubar
    menubar=Menu(basketballCtrl)
    fileMenu=Menu(menubar, tearoff=0)
    fileMenu.add_command(label='Save Configuration', command=saveConfig)
    fileMenu.add_command(label='Open Configuration', command=openConfig)
    fileMenu.add_separator()
    fileMenu.add_command(label='Quit', command=quitProgram)

    serverMenu=Menu(menubar, tearoff=0)
    serverMenu.add_command(label='Start Server', command=openServerSettings)

    menubar.add_cascade(label='File', menu=fileMenu)
    menubar.add_cascade(label='Server', menu=serverMenu)
    basketballCtrl.config(menu=menubar)
