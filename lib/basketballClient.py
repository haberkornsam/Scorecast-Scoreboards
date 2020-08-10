from tkinter import *
from threading import *
from socket import *
from time import *
import easygui
import xml.etree.ElementTree as ET



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
priColory =  450
secColory = 475

class Receive(Thread):
    def __init__(self, s, app):
        Thread.__init__(self)
        self.s=s
        self.app = app

    def run(self):
        while 1:
            try:
                text = self.receiveData()
                recvText = text[0]
                if not recvText: break
                if recvText == 'Start':
                    self.app.startClockRecv()
                elif recvText == 'Stop':
                    self.app.stopClockRecv()
                    self.app.changeTimeRecv(text[1], text[2])
                elif recvText == 'ChangeTime':
                    self.timeM = text[1]
                    self.timeS = text[2]
                    self.app.changeTimeRecv(self.timeM, self.timeS)
                elif recvText == 'homeTeam':
                    self.app.changeHTeamRecv(text[1])
                elif recvText == 'awayTeam':
                    self.app.changeATeamRecv(text[1])
                elif recvText == 'homeScore':
                    self.app.changeHomeScoreRecv(text[1])
                elif recvText == 'awayScore':
                    self.app.changeAwayScoreRecv(text[1])
                elif recvText == 'homeFouls':
                    self.app.changeHomeFoulsRecv(text[1])
                elif recvText == 'awayFouls':
                    self.app.changeAwayFoulsRecv(text[1])
                elif recvText == 'half':
                    self.app.changeHalfRecv(text[1])
                elif recvText == 'homeTO':
                    self.app.changeHomeFullTORecv(text[2])
                    self.app.changeHomePartTORecv(text[1])
                elif recvText == 'awayTO':
                    self.app.changeAwayFullTORecv(text[2])
                    self.app.changeAwayPartTORecv(text[1])
                elif recvText == 'homePrimary':
                    self.app.changeHPRecv(text[1])
                elif recvText == 'homeSecondary':
                    self.app.changeHSRecv(text[1])
                elif recvText == 'awayPrimary':
                    self.app.changeAPRecv(text[1])
                elif recvText == 'awaySecondary':
                    self.app.changeASRecv(text[1])
                elif recvText == 'poss':
                    self.app.changePossRecv(text[1], text[2])
                elif recvText == 'sync':
                    self.app.changeHTeamRecv(text[1])
                    self.app.changeATeamRecv(text[2])
                    self.app.changeHomeScoreRecv(text[3])
                    self.app.changeAwayScoreRecv(text[4])
                    self.app.changeAwayFoulsRecv(text[5])
                    self.app.changeHomeFoulsRecv(text[6])
                    self.app.changeHalfRecv(text[7])
                    self.app.changeHomePartTORecv(text[8])
                    self.app.changeAwayPartTORecv(text[9])
                    self.app.changeHomeFullTORecv(text[10])
                    self.app.changeAwayFullTORecv(text[11])
                    self.app.changeHPRecv(text[12])
                    self.app.changeHSRecv(text[13])
                    self.app.changeAPRecv(text[14])
                    self.app.changeASRecv(text[15])
                    self.app.changeTimeRecv(text[16], text[17])
                    self.app.changePossRecv(text[18], text[19])
            except:
                break

    def receiveData(self):
        while True:
            datum = self.s.recv(256).decode('utf-8')
            if datum[0] == '~':
                datum = datum[1:]
                data = datum.split('`')
                return data[:-1]
            else:
                break


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
        #self.makeWidgets()
        self.l = Label(self, text=self.formatted, width=20)
        self.l.grid(row=0, column=3, columnspan=3)
        self._setTime(self._elapsedtime)



    def makeWidgets(self):
        """ Make the time label. """
        #l = Label(self, textvariable=self.timestr, width=20)
        self._setTime(self._elapsedtime)
        #l.grid(row=0, column=3, columnspan=3)


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


        self.formatted = str(minutes).zfill(2)+":"+str(seconds).zfill(2)+"."+str(hseconds).zfill(1)
        self._minutes = str(minutes).zfill(2)
        self._seconds = str(seconds).zfill(2)+"."+str(hseconds).zfill(1)
        format = str(minutes).zfill(2)+":"+str(seconds).zfill(2)
        self.timestr.set(self.formatted)
        self.l.configure(text=self.formatted)


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

class CtrlApp(Thread):
    def changePossRecv(self, hPoss, aPoss):
        global homePoss, awayPoss
        homePoss = hPoss
        awayPoss = aPoss

        if awayPoss=='True':
            self.awayPossession.configure(text='Poss\n -->')
        if awayPoss=='False':
            self.awayPossession.configure(text='Poss\n')
        if homePoss=='True':
            self.homePossession.configure(text='Poss\n<--')
        if homePoss=='False':
            self.homePossession.configure(text='Poss\n')

    def startClockRecv(self):
        global runnin
        runnin = 'Stop'
        self.star.configure(text=runnin)
        self.sw.Start()

    def stopClockRecv(self):
        global runnin
        runnin = 'Start'
        self.star.configure(text=runnin)
        self.sw.Stop()

    def changeTimeRecv(self, timeM, timeS):
        global runnin
        runnin = 'Start'
        self.sw.Stop()
        self.star.configure(text=runnin)
        self.sw.setClock(float(timeM), float(timeS))

    def changeHTeamRecv(self, newName):
        global homeTeam
        homeTeam = newName
        self.homeLabel.configure(text=homeTeam)

    def changeATeamRecv(self, newName):
        global awayTeam
        awayTeam = newName
        self.awayLabel.configure(text=awayTeam)

    def changeHomeScoreRecv(self, newScore):
        global homeScore
        homeScore = int(newScore)
        self.homeScoreL.configure(text=homeScore)

    def changeAwayScoreRecv(self, newScore):
        global awayScore
        awayScore = int(newScore)
        self.awayScoreL.configure(text=awayScore)

    def changeHomeFoulsRecv(self, newFouls):
        global hFouls, awayBonusState
        hFouls = int(newFouls)
        self.hFoulL.configure(text=hFouls)
        if hFouls >= 7 and hFouls < 10:
            awayBonusState = 'BONUS'
        if hFouls >= 10:
            awayBonusState = 'BONUS+'
        if hFouls < 7:
            awayBonusState = ''

        self.awayBonus.configure(text=awayBonusState)

    def changeAwayFoulsRecv(self, newFouls):
        global aFouls, homeBonusState
        aFouls = int(newFouls)
        self.aFoulL.configure(text=aFouls)
        if aFouls >= 7 and aFouls<10:
            homeBonusState = 'BONUS'
        if aFouls>=10:
            homeBonusState = 'BONUS+'
        if aFouls<7:
            homeBonusState = ''

        self.homeBonus.configure(text=homeBonusState)

    def changeHalfRecv(self, newHalf):
        global half
        half = newHalf
        self.halfLabel.configure(text=half)

    def changeHomeFullTORecv(self, newTO):
        global homeFullTO
        homeFullTO = int(newTO)
        self.homeFullTOLabel.configure(text = 'Full:\n' + str(homePartTO))


    def changeAwayFullTORecv(self, newTO):
        global awayFullTO
        awayFullTO = int(newTO)
        self.awayFullTOLabel.config(text='Full:\n' + str(awayFullTO))

    def changeHomePartTORecv(self, newTO):
        global homePartTO
        homePartTO = int(newTO)
        self.homePartTOLabel.config(text = 'Partial:\n' + str(homePartTO))

    def changeAwayPartTORecv(self, newTO):
        global awayPartTO
        awayPartTO = int(newTO)
        self.awayPartTOLabel.config(text = 'Partial:\n' + str(awayPartTO))

    def changeHPRecv(self, newColor):
        global homePrimaryColor
        homePrimaryColor=newColor

    def changeHSRecv(self, newColor):
        global homeSecondColor
        homeSecondColor = newColor

    def changeAPRecv(self, newColor):
        global awayPrimaryColor
        awayPrimaryColor = newColor

    def changeASRecv(self, newColor):
        global awaySecondColor
        awaySecondColor = newColor

    def toggleStartLabel(self, event):
        global runnin
        if runnin == 'Start':
            runnin = 'Stop'
            self.star.configure(text=runnin)
            self.sw.Start()
            self.send('Start')

        else:
            runnin = 'Start'
            self.star.configure(text=runnin)
            self.sw.Stop()
            self.send('Stop',self.sw.getMinutes(), self.sw.getSeconds())

    def changeTime(self, event):
        global runnin
        self.sw.Stop()
        self.send('Stop', self.sw.getMinutes(), self.sw.getSeconds())
        runnin = "Stop"
        self.star.configure(text=runnin)
        self.sw.place_forget()
        self.enterTimeM.delete(0, END)
        self.enterTimeS.delete(0, END)
        self.enterTimeM.place(x=enterTimeMx, y=enterTimeMy, anchor='n')
        self.enterTimeColon.place(x=enterTimeColonx, y=enterTimeColony, anchor='n')
        self.enterTimeS.place(x=enterTimeSx, y=enterTimeSy, anchor='n')
        self.star.place_forget()
        self.sub.place(x=startx, y=starty, anchor='n')
        self.setClock.place(x=setClockx, y=setClocky, anchor='n')

    def submitTime(self, event):
        global runnin
        self.sw.setClock(self.enterTimeM.get(), self.enterTimeS.get())
        self.sToEnter = self.enterTimeS.get()
        self.mToEnter = self.enterTimeM.get()
        if not self.sToEnter:
            self.sToEnter = '0'
        if not self.mToEnter:
            self.mToEnter = '0'

        self.send('ChangeTime', self.mToEnter, self.sToEnter)
        runnin = "Start"
        self.star.configure(text=runnin)
        self.enterTimeM.place_forget()
        self.enterTimeS.place_forget()
        self.enterTimeColon.place_forget()
        self.sub.place_forget()
        self.sw.place(x=swx, y=swy, anchor='n')
        self.star.place(x=startx, y=starty, anchor='n')

    def changeHomeTeam(self, event):
        self.homeLabel.place_forget()
        self.homeInput.place(x=homeLabelx, y=teamLabely, anchor='nw')

    def changeAwayTeam(self, event):
        self.awayLabel.place_forget()
        self.awayInput.place(x=awayLabelx, y=teamLabely, anchor='ne')

    def saveHomeTeam(self, event):
        global homeTeam
        homeTeam = str(self.homeInput.get())
        self.homeInput.place_forget()
        self.homeLabel.configure(text=homeTeam)
        self.send('homeTeam', homeTeam)
        self.homeLabel.place(x=homeLabelx, y=teamLabely, anchor='nw')

    def saveAwayTeam(self, event):
        global awayTeam
        awayTeam = str(self.awayInput.get())
        self.awayInput.place_forget()
        self.awayLabel.configure(text=awayTeam)
        self.send('awayTeam', awayTeam)
        self.awayLabel.place(x=awayLabelx, y=teamLabely, anchor='ne')

    def editHomeScore(self, event):
        self.homeScoreL.place_forget()
        self.hEditScore.place(x=homeScoreLx, y=teamEditScorey, anchor='nw')

    def editAwayScore(self, event):
        self.awayScoreL.place_forget()
        self.aEditScore.place(x=awayScoreLx, y=teamEditScorey, anchor='ne')

    def homeScoreOverride(self, event):
        global homeScore
        homeScore = int(self.hEditScore.get())
        self.homeScoreFileUpdate()
        self.hEditScore.place_forget()
        self.homeScoreL.place(x=homeScoreLx, y=teamScoreLy, anchor='nw')

    def awayScoreOverride(self, event):
        global awayScore
        awayScore = int(self.aEditScore.get())
        self.awayScoreFileUpdate()
        self.aEditScore.place_forget()
        self.awayScoreL.place(x=awayScoreLx, y=teamScoreLy, anchor='ne')

    def homeScoreFileUpdate(self):
        global homeScore, awayScore
        self.homeScoreL.configure(text=homeScore)
        self.send('homeScore', homeScore)

    def awayScoreFileUpdate(self):
        global homeScore, awayScore
        self.awayScoreL.configure(text=awayScore)
        self.send('awayScore', awayScore)

    def hScore1(self, event):
        global homeScore, awayScore
        homeScore += 1
        self.homeScoreFileUpdate()

    def aScore1(self, event):
        global homeScore, awayScore
        awayScore += 1
        self.awayScoreFileUpdate()

    def hScore2(self, event):
        global homeScore, awayScore
        homeScore += 2
        self.homeScoreFileUpdate()

    def aScore2(self, event):
        global homeScore, awayScore
        awayScore += 2
        self.awayScoreFileUpdate()

    def hScore3(self, event):
        global homeScore, awayScore
        homeScore += 3
        self.homeScoreFileUpdate()

    def aScore3(self, event):
        global homeScore, awayScore
        awayScore += 3
        self.awayScoreFileUpdate()

    def changeHomeFouls(self, event):
        self.hFoulL.place_forget()
        self.hFoulIn.place(x=hFoulLx, y=FoulLy, anchor='nw')

    def changeAwayFouls(self, event):
        self.aFoulL.place_forget()
        self.aFoulIn.place(x=aFoulLx, y=FoulLy, anchor='ne')

    def submitHomeFouls(self, event):
        global hFouls
        self.hFoulL.place(x=hFoulLx, y=FoulLy, anchor='nw')
        self.hFoulIn.place_forget()
        self.hFouls = int(self.hFoulIn.get())
        self.homeFoulFileUpdate()

    def submitAwayFouls(self, event):
        global aFouls
        self.aFoulL.place(x=aFoulLx, y=FoulLy, anchor='ne')
        self.aFoulIn.place_forget()
        aFouls = int(self.aFoulIn.get())
        self.awayFoulFileUpdate()

    def addHomeFoul(self, event):
        global hFouls
        hFouls += 1
        self.homeFoulFileUpdate()

    def addAwayFoul(self, event):
        global aFouls
        aFouls += 1
        self.awayFoulFileUpdate()

    def subHomeFoul(self, event):
        global hFouls
        if hFouls > 0:
            hFouls -= 1
        self.homeFoulFileUpdate()

    def subtAwayFoul(self, event):
        global aFouls
        if aFouls > 0:
            aFouls -= 1
        self.awayFoulFileUpdate()

    def homeFoulFileUpdate(self):
        global hFouls, hBonus, homeBonusState, awayBonusState
        self.hFoulL.configure(text=hFouls)
        if hFouls >= 7 and hFouls < 10:
            awayBonusState = 'BONUS'
        if hFouls >= 10:
            awayBonusState = 'BONUS+'
        if hFouls < 7:
            awayBonusState = ''
        self.awayBonus.configure(text=awayBonusState)
        self.send('homeFouls', hFouls)

    def awayFoulFileUpdate(self):
        global aFouls, aBonus, awayBonusState, homeBonusState
        self.aFoulL.configure(text=aFouls)
        if aFouls >= 7 and aFouls < 10:
            homeBonusState = 'BONUS'
        if aFouls >= 10:
            homeBonusState = 'BONUS+'
        if aFouls < 7:
            homeBonusState = ''
        self.homeBonus.configure(text=homeBonusState)
        self.send('awayFouls', aFouls)

    def clearTeamFouls(self, event):
        global hFouls, aFouls
        hFouls = 0
        aFouls = 0
        self.homeFoulFileUpdate()
        self.awayFoulFileUpdate()

    def changeHomePoss(self, event):
        global homePoss, awayPoss
        if homePoss == 'False':
            homePoss = 'True'
            awayPoss = 'False'
        elif homePoss == 'True':
            homePoss = 'False'
        self.updatePoss()

    def changeAwayPoss(self, event):
        global awayPoss, homePoss
        if awayPoss == 'False':
            awayPoss = 'True'
            homePoss = 'False'
        elif awayPoss == 'True':
            awayPoss = 'False'
        self.updatePoss()

    def updatePoss(self):
        global awayPoss, homePoss
        if awayPoss == 'True':
            self.awayPossession.configure(text='Poss\n -->')

        if awayPoss == 'False':
            self.awayPossession.configure(text='Poss\n')
        if homePoss == 'True':
            self.homePossession.configure(text='Poss\n<--')
        if homePoss == 'False':
            self.homePossession.configure(text='Poss\n')
        self.send('poss', homePoss, awayPoss)

    def changeHalf(self, event):
        self.halfLabel.place_forget()
        self.halfIn.place(x=centerx, y=teamEditScorey, anchor='n')

    def submitHalf(self, event):
        global half
        self.halfIn.place_forget()
        self.halfLabel.place(x=centerx, y=teamEditScorey, anchor='n')
        half = str(self.halfIn.get())
        self.halfLabel.configure(text=half)
        self.send('half', half)

    def homeTOFileUpdate(self):
        global homeFullTO, homePartTO

        self.homePartTOLabel.configure(text='Partial:\n' + str(homePartTO))
        self.homeFullTOLabel.configure(text='Full:\n' + str(homeFullTO))
        self.send('homeTO', homePartTO, homeFullTO)

    def awayTOFileUpdate(self):
        global awayFullTO, awayPartTO

        self.awayPartTOLabel.configure(text='Partial:\n' + str(awayPartTO))
        self.awayFullTOLabel.configure(text='Full:\n' + str(awayFullTO))
        self.send('awayTO', awayPartTO, awayFullTO)

    def editPartHomeTO(self, event):

        self.homePartTOIn.place(x=hPartTOLabelx, y=TOLabely, anchor='nw')
        self.homePartTOLabel.place_forget()

    def editPartAwayTO(self, event):
        self.awayPartTOIn.place(x=aPartTOLabelx, y=TOLabely, anchor='ne')
        self.awayPartTOLabel.place_forget()

    def editFullHomeTO(self, event):

        self.homeFullTOIn.place(x=hFullTOLabelx, y=TOLabely, anchor='nw')
        self.homeFullTOLabel.place_forget()

    def editFullAwayTO(self, event):
        self.awayFullTOIn.place(x=aFullTOLabelx, y=TOLabely, anchor='ne')
        self.awayFullTOLabel.place_forget()

    def submitPartHomeTO(self, event):
        global homePartTO
        homePartTO = int(self.homePartTOIn.get())
        self.homePartTOLabel.place(x=hPartTOLabelx, y=TOLabely, anchor='nw')
        self.homePartTOIn.place_forget()
        self.homeTOFileUpdate()

    def submitPartAwayTO(self, event):
        global awayPartTO
        awayPartTO = int(self.awayPartTOIn.get())
        self.awayPartTOLabel.place(x=aPartTOLabelx, y=TOLabely, anchor='ne')
        self.awayPartTOIn.place_forget()
        self.awayTOFileUpdate()

    def submitFullHomeTO(self, event):
        global homeFullTO
        homeFullTO = int(self.homeFullTOIn.get())
        self.homeFullTOLabel.place(x=hFullTOLabelx, y=TOLabely, anchor='nw')
        self.homeFullTOIn.place_forget()
        self.homeTOFileUpdate()

    def submitFullAwayTO(self, event):
        global awayFullTO
        awayFullTO = int(self.awayFullTOIn.get())
        self.awayFullTOLabel.place(x=aFullTOLabelx, y=TOLabely, anchor='ne')
        self.awayFullTOIn.place_forget()
        self.awayTOFileUpdate()

    def takeHomePart(self, event):
        global homePartTO
        if homePartTO > 0:
            homePartTO -= 1
        self.homeTOFileUpdate()

    def takeAwayPart(self, event):
        global awayPartTO
        if awayPartTO > 0:
            awayPartTO -= 1
        self.awayTOFileUpdate()

    def takeHomeFUll(self, event):
        global homeFullTO
        if homeFullTO > 0:
            homeFullTO -= 1
        self.homeTOFileUpdate()

    def takeAwayFull(self, event):
        global awayFullTO
        if awayFullTO > 0:
            awayFullTO -= 1
        self.awayTOFileUpdate()

    def changeHPrimary(self, event):
        self.setHPrimary.place_forget()
        self.hPriIn.place(x=hcolorx, y=priColory, anchor='nw')

    def changeHSecond(self, event):
        self.setHSecond.place_forget()
        self.hSecIn.place(x=hcolorx, y=secColory, anchor='nw')

    def changeAPrimary(self, event):
        self.setAPrimary.place_forget()
        self.aPriIn.place(x=acolorx, y=priColory, anchor='ne')

    def changeASecond(self, event):
        self.setASecond.place_forget()
        self.aSecIn.place(x=acolorx, y=secColory, anchor='ne')

    def subHP(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        homePrimaryColor = str(self.hPriIn.get())
        self.hPriIn.place_forget()
        self.setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')
        self.send('homePrimary', homePrimaryColor)

    def subHS(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        homeSecondColor = str(self.hSecIn.get())
        self.hSecIn.place_forget()
        self.setHSecond.place(x=hcolorx, y=secColory, anchor='nw')
        self.send('homeSecondary', homeSecondColor)

    def subAP(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        awayPrimaryColor = str(self.aPriIn.get())
        self.aPriIn.place_forget()
        self.setAPrimary.place(x=acolorx, y=priColory, anchor='ne')
        self.send('awayPrimary', awayPrimaryColor)

    def subAS(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        awaySecondColor = str(self.aSecIn.get())
        self.aSecIn.place_forget()
        self.setASecond.place(x=acolorx, y=secColory, anchor='ne')
        self.send('awaySecondary', awaySecondColor)

    def updateTeamNames(self):
        self.homeLabel.configure(text=homeTeam)
        self.awayLabel.configure(text=awayTeam)

    def updateLabels(self):
        self.sync()
        self.updateTeamNames()
        self.homeScoreFileUpdate()
        self.awayScoreFileUpdate()
        self.homeFoulFileUpdate()
        self.awayFoulFileUpdate()
        self.updatePoss()
        self.homeTOFileUpdate()
        self.awayTOFileUpdate()

    def sync(self):
        global homeTeam, awayTeam, homeScore, awayScore, aFouls, hFouls, half, homePartTO, awayPartTO, \
            homeFullTO, awayFullTO, homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, sw
        data = '~sync`'
        data += str(homeTeam) + '`' #1
        data += str(awayTeam) + '`' #2
        data += str(homeScore) + '`' #3
        data += str(awayScore) + '`' #4
        data += str(aFouls) + '`' #5
        data += str(hFouls) + '`' #6
        data += str(half) + '`' #7
        data += str(homePartTO) + '`' #8
        data += str(awayPartTO) + '`' #9
        data += str(homeFullTO) + '`' #10
        data += str(awayFullTO) + '`' #11
        data += str(homePrimaryColor) + '`' #12
        data += str(homeSecondColor) + '`' #13
        data += str(awayPrimaryColor) + '`' #14
        data += str(awaySecondColor) + '`' #15
        data += str(self.sw.getMinutes()) + '`' #16
        data += str(self.sw.getSeconds()) + '`' #17
        data += str(homePoss)+'`' #18
        data += str(awayPoss)+'`' #19

        self.s.send(data.encode())

    def openConfig(self, event):
        global homeTeam, awayTeam, homeScore, awayScore, aFouls, hFouls, half, homePoss, awayPoss, homePartTO, awayPartTO, \
            homeFullTO, awayFullTO, homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, sw
        tree = ET.parse(easygui.fileopenbox(filetypes=['*.xml'])).getroot()
        if (tree.tag == 'basketball'):
            homeTeam = tree[0][0].text
            homeScore = int(tree[0][1].text)
            hFouls = int(tree[0][2].text)
            homePoss = str(tree[0][3].text)
            homePartTO = int(tree[0][4].text)
            homeFullTO = int(tree[0][5].text)
            homePrimaryColor = tree[0][6].text
            homeSecondColor = tree[0][7].text
            awayTeam = tree[1][0].text
            awayScore = int(tree[1][1].text)
            aFouls = int(tree[1][2].text)
            awayPoss = str(tree[1][3].text)
            awayPartTO = int(tree[1][4].text)
            awayFullTO = int(tree[1][5].text)
            awayPrimaryColor = tree[1][6].text
            awaySecondColor = tree[1][7].text
            half = tree[2].text
            self.sw.setClock(int(tree[3][0].text), float(tree[3][1].text))
            self.updateLabels()

    def saveConfig(self, event=None):
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
        minutes1.text = str(self.sw.getMinutes())
        seconds1 = ET.SubElement(clock1, 'Seconds')
        seconds1.text = str(self.sw.getSeconds())

        myData = ET.tostring(basketball).decode("utf-8")
        configFile = open(easygui.filesavebox() + '.xml', 'w')
        configFile.write(myData)

    def __init__(self, master,ip, port, s, data):

        self.s = s



        Thread.__init__(self)
        self.sw = StopWatch(master)
        self.sw.place(x=300, y=10, anchor='n')
        self.sw.setClock(float(data[20]), float(data[21]))

        self.star = Label(master, text=runnin, width=20)
        self.star.bind('<Button-1>', self.toggleStartLabel)
        self.star.place(x=startx, y=starty, anchor='n')

        self.setClock = Label(master, text='Set Time', width=20)
        self.setClock.bind('<Button-1>', self.changeTime)
        self.setClock.place(x=setClockx, y=setClocky, anchor='n')

        self.enterTimeM = Entry(master, text='mm', width=5)
        self.enterTimeM.place(x=enterTimeMx, y=enterTimeMy, anchor='n')
        self.enterTimeM.place_forget()
        self.enterTimeColon = Label(master, text=':', width=3)
        self.enterTimeColon.place(x=enterTimeColonx, y=enterTimeColony, anchor='n')
        self.enterTimeColon.place_forget()
        self.enterTimeS = Entry(master, text="ss", width=5)
        self. enterTimeS.place(x=enterTimeSx, y=enterTimeSy, anchor='n')
        self.enterTimeS.place_forget()

        self.sub = Label(master, text="Submit", width=20)
        self.sub.bind('<Button-1>', self.submitTime)
        self.sub.place_forget()

        self.homeLabel = Label(master, text=homeTeam, width=20)
        self.homeLabel.bind('<Button-1>', self.changeHomeTeam)
        self.homeLabel.place(x=homeLabelx, y=teamLabely, anchor='nw')
        self.awayLabel = Label(master, text=awayTeam, width=20)
        self.awayLabel.bind('<Button-1>', self.changeAwayTeam)
        self.awayLabel.place(x=awayLabelx, y=teamLabely, anchor='ne')

        self.homeInput = Entry(master, width=19)
        self.homeInput.bind('<Return>', self.saveHomeTeam)
        self.homeInput.place_forget()
        self.awayInput = Entry(master, width=19)
        self.awayInput.bind('<Return>', self.saveAwayTeam)
        self.awayInput.place_forget()

        self.homeScoreL = Label(master, text=homeScore, width=20, height=7)
        self.homeScoreL.bind("<Button-1>", self.editHomeScore)
        self.homeScoreL.place(x=homeScoreLx, y=teamScoreLy, anchor='nw')
        self.awayScoreL = Label(master, text=awayScore, width=20, height=7)
        self.awayScoreL.bind("<Button-1>", self.editAwayScore)
        self.awayScoreL.place(x=awayScoreLx, y=teamScoreLy, anchor='ne')

        self.hEditScore = Entry(master, width=19)
        self.hEditScore.bind('<Return>', self.homeScoreOverride)
        self.hEditScore.place_forget()
        self.aEditScore = Entry(master, width=19)
        self.aEditScore.bind('<Return>', self.awayScoreOverride)
        self.aEditScore.place_forget()

        self.homeScore1 = Label(master, text='+1', width=6)
        self.homeScore1.bind("<Button-1>", self.hScore1)
        self.homeScore1.place(x=hscore1x, y=scorey, anchor='nw')
        self.homeScore2 = Label(master, text='+2', width=6)
        self.homeScore2.bind("<Button-1>", self.hScore2)
        self.homeScore2.place(x=hscore2x, y=scorey, anchor='nw')
        self.homeScore3 = Label(master, text='+3', width=6)
        self.homeScore3.bind("<Button-1>", self.hScore3)
        self.homeScore3.place(x=hscore3x, y=scorey, anchor='nw')

        self.awayScore1 = Label(master, text='+1', width=6)
        self.awayScore1.bind("<Button-1>", self.aScore1)
        self.awayScore1.place(x=ascore1x, y=scorey, anchor='ne')
        self.awayScore2 = Label(master, text='+2', width=6)
        self.awayScore2.bind("<Button-1>", self.aScore2)
        self.awayScore2.place(x=ascore2x, y=scorey, anchor='ne')
        self.awayScore3 = Label(master, text='+3', width=6)
        self.awayScore3.bind("<Button-1>", self.aScore3)
        self.awayScore3.place(x=ascore3x, y=scorey, anchor='ne')

        self.hFoulLab = Label(master, text='Home Fouls', fg='#ffffff', bg='#000000')
        self.hFoulLab.place(x=hFoulLabx, y=foulLaby, anchor='nw')
        self.aFoulLab = Label(master, text='Away Fouls', fg='#ffffff', bg='#000000')
        self.aFoulLab.place(x=aFoulLabx, y=foulLaby, anchor='ne')

        self.hFoulL = Label(master, text=hFouls, width=12, height=2)
        self.hFoulL.bind('<Button-1>', self.changeHomeFouls)
        self.hFoulL.place(x=hFoulLx, y=FoulLy, anchor='nw')
        self.aFoulL = Label(master, text=aFouls, width=12, height=2)
        self.aFoulL.bind('<Button-1>', self.changeAwayFouls)
        self.aFoulL.place(x=aFoulLx, y=FoulLy, anchor='ne')

        self.hFoulIn = Entry(master, width=12)
        self.hFoulIn.bind('<Return>', self.submitHomeFouls)
        self.hFoulIn.place(x=hFoulLx, y=FoulLy, anchor='nw')
        self.hFoulIn.place_forget()
        self.aFoulIn = Entry(master, width=12)
        self.aFoulIn.bind('<Return>', self.submitAwayFouls)
        self.aFoulIn.place(x=aFoulLx, y=FoulLy, anchor='ne')
        self.aFoulIn.place_forget()

        self.homeBonus = Label(master, text=homeBonusState, width=7, fg='#ffffff', bg='#000000')
        self.homeBonus.place(x=homeBonusx, y=foulLaby, anchor='n')
        self.awayBonus = Label(master, text=awayBonusState, width=7, fg='#ffffff', bg='#000000')
        self.awayBonus.place(x=awayBonusx, y=foulLaby, anchor='n')

        self.hFoulAd = Label(master, text="+1", width=6)
        self.hFoulAd.bind('<Button-1>', self.addHomeFoul)
        self.hFoulAd.place(x=homeBonusx, y=foulAdy, anchor='n')
        self.aFoulAd = Label(master, text="+1", width=6)
        self.aFoulAd.bind('<Button-1>', self.addAwayFoul)
        self.aFoulAd.place(x=awayBonusx, y=foulAdy, anchor='n')

        self.hFoulSubt = Label(master, text='-1', width=6)
        self.hFoulSubt.bind('<Button-1>', self.subHomeFoul)
        self.hFoulSubt.place(x=homeBonusx, y=foulSubty, anchor='n')

        self.aFoulSubt = Label(master, text='-1', width=6)
        self.aFoulSubt.bind('<Button-1>', self.subtAwayFoul)
        self.aFoulSubt.place(x=awayBonusx, y=foulSubty, anchor='n')

        # Clear Team Fouls
        self.clearFoulsLabel = Label(master, text='Clear Team Fouls', width=13)
        self.clearFoulsLabel.bind('<Button-1>', self.clearTeamFouls)
        self.clearFoulsLabel.place(x=centerx, y=foulSubty, anchor='c')

        self.halfLabel = Label(master, text=half, width=5)
        self.halfLabel.bind('<Button-1>', self.changeHalf)
        self.halfLabel.place(x=centerx, y=teamEditScorey, anchor='n')

        # Period Input
        self.halfIn = Entry(master, width=5)
        self.halfIn.bind('<Return>', self.submitHalf)
        self.halfIn.place_forget()

        if homePoss=='False':
            self.homePossession = Label(master, text="Poss\n", width=5)
        else:
            self.homePossession = Label(master, text="Poss\n<--", width = 5)
        self.homePossession.bind('<Button-1>', self.changeHomePoss)
        self.homePossession.place(x=homePossx, y=teamEditScorey, anchor='nw')
        if awayPoss == 'False':
            self.awayPossession = Label(master, text="Poss\n", width=5)
        else:
            self.awayPossession = Label(master, text="Poss\n-->", width=5)
        self.awayPossession.bind('<Button-1>', self.changeAwayPoss)
        self.awayPossession.place(x=awayPossx, y=teamEditScorey, anchor='ne')

        # static timeout titles
        self.homeTOLabel = Label(master, text='\nHome Timeouts', fg='#ffffff', bg='#000000')
        self.homeTOLabel.place(x=homeStaticTOx, y=staticTOy, anchor='nw')
        self.awayTOLabel = Label(master, text='\nAway Timeouts', fg='#ffffff', bg='#000000')
        self.awayTOLabel.place(x=awayStaticTOx, y=staticTOy, anchor='ne')

        # timeout updating
        self.homePartTOLabel = Label(master, text='Partial:\n' + str(homePartTO), width=6)
        self.homePartTOLabel.bind('<Button-1>', self.editPartHomeTO)
        self.homePartTOLabel.place(x=hPartTOLabelx, y=TOLabely, anchor='nw')

        self.homeFullTOLabel = Label(master, text='Full:\n' + str(homeFullTO), width=6)
        self.homeFullTOLabel.bind('<Button-1>', self.editFullHomeTO)
        self.homeFullTOLabel.place(x=hFullTOLabelx, y=TOLabely, anchor='nw')

        self.awayPartTOLabel = Label(master, text='Partial:\n' + str(awayPartTO), width=6)
        self.awayPartTOLabel.bind("<Button-1>", self.editPartAwayTO)
        self.awayPartTOLabel.place(x=aPartTOLabelx, y=TOLabely, anchor='ne')

        self.awayFullTOLabel = Label(master, text='Full:\n' + str(awayFullTO), width=6)
        self.awayFullTOLabel.bind("<Button-1>", self.editFullAwayTO)
        self.awayFullTOLabel.place(x=aFullTOLabelx, y=TOLabely, anchor='ne')

        self.homeTakePart = Label(master, text='Partial', width=6)
        self.homeTakePart.bind('<Button-1>', self.takeHomePart)
        self.homeTakePart.place(x=hTakex, y=takeParty, anchor='nw')

        self.homeTakeFull = Label(master, text='Full', width=6)
        self.homeTakeFull.bind('<Button-1>', self.takeHomeFUll)
        self.homeTakeFull.place(x=hTakex, y=takeFully, anchor='nw')

        self.awayTakePart = Label(master, text="Partial", width=6)
        self.awayTakePart.bind("<Button-1>", self.takeAwayPart)
        self.awayTakePart.place(x=aTakex, y=takeParty, anchor='ne')

        self.awayTakeFull = Label(master, text='Full', width=6)
        self.awayTakeFull.bind('<Button-1>', self.takeAwayFull)
        self.awayTakeFull.place(x=aTakex, y=takeFully, anchor='ne')

        self.homePartTOIn = Entry(master, width=4)
        self.homePartTOIn.bind('<Return>', self.submitPartHomeTO)
        self.homePartTOIn.place(x=hPartTOLabelx, y=TOLabely, anchor='nw')
        self.homePartTOIn.place_forget()

        self.awayPartTOIn = Entry(master, width=4)
        self.awayPartTOIn.bind('<Return>', self.submitPartAwayTO)
        self.awayPartTOIn.place(x=aPartTOLabelx, y=TOLabely, anchor='ne')
        self.awayPartTOIn.place_forget()

        self.homeFullTOIn = Entry(master, width=4)
        self.homeFullTOIn.bind('<Return>', self.submitFullHomeTO)
        self.homeFullTOIn.place(x=hFullTOLabelx, y=TOLabely, anchor='nw')
        self.homeFullTOIn.place_forget()

        self.awayFullTOIn = Entry(master, width=4)
        self.awayFullTOIn.bind('<Return>', self.submitFullAwayTO)
        self.awayFullTOIn.place(x=aFullTOLabelx, y=TOLabely, anchor='ne')
        self.awayFullTOIn.place_forget()

        # color changing
        self.setHPrimary = Label(master, text="Set Home Primary Color", width=20)
        self.setHPrimary.bind('<Button-1>', self.changeHPrimary)
        self.setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')

        self.setHSecond = Label(master, text="Set Home Secondary Color", width=20)
        self.setHSecond.bind('<Button-1>', self.changeHSecond)
        self.setHSecond.place(x=hcolorx, y=secColory, anchor='nw')

        self.setAPrimary = Label(master, text="Set Away Primary Color", width=20)
        self.setAPrimary.bind('<Button-1>', self.changeAPrimary)
        self.setAPrimary.place(x=acolorx, y=priColory, anchor='ne')

        self.setASecond = Label(master, text='Set Away Secondary Color', width=20)
        self.setASecond.bind('<Button-1>', self.changeASecond)
        self.setASecond.place(x=acolorx, y=secColory, anchor='ne')

        self.hPriIn = Entry(master, width=18)
        self.hPriIn.bind('<Return>', self.subHP)
        self.hPriIn.place_forget()

        self.hSecIn = Entry(master, width=18)
        self.hSecIn.bind('<Return>', self.subHS)
        self.hSecIn.place_forget()

        self.aPriIn = Entry(master, width=18)
        self.aPriIn.bind('<Return>', self.subAP)
        self.aPriIn.place_forget()

        self.aSecIn = Entry(master, width=18)
        self.aSecIn.bind('<Return>', self.subAS)
        self.aSecIn.place_forget()

        self.openConfigLabel = Label(master, text='Open Configuration')
        self.openConfigLabel.bind('<Button-1>', self.openConfig)
        self.openConfigLabel.place(x=centerx, y=priColory, anchor='n')

        self.saveConfiglabel = Label(master, text='Save Configuration')
        self.saveConfiglabel.bind('<Button-1>', self.saveConfig)
        self.saveConfiglabel.place(x=centerx, y=secColory, anchor='n')

        Receive(s, self).start()


    def send(self, arg, value=None, value2 = None):
        data1 = '~'+arg+'`'
        if value != None:
            data1 += str(value) +'`'
        if value2 != None:
            data1 += str(value2) +'`'
        self.s.send(data1.encode())



def start(ip, port, s, data):
    global runnin, homeTeam, awayTeam, homeScore, awayScore, hFouls, aFouls, homeBonusState,awayBonusState, half, \
        homePoss, awayPoss, homePartTO, homeFullTO, awayPartTO, awayFullTO, homePrimaryColor, homeSecondColor, \
        awayPrimaryColor, awaySecondColor

    runnin = 'Start'
    homeTeam = str(data[1])
    awayTeam = str(data[2])
    homeScore = int(data[3])
    awayScore = int(data[4])
    hFouls = int(data[5])
    aFouls = int(data[6])
    homeBonusState = str(data[7])
    awayBonusState = str(data[8])
    half = str(data[9])
    homePoss = str(data[10])
    awayPoss = str(data[11])
    homePartTO = int(data[12])
    homeFullTO = int(data[13])
    awayPartTO = int(data[14])
    awayFullTO = int(data[15])
    homePrimaryColor = str(data[16])
    homeSecondColor = str(data[17])
    awayPrimaryColor = str(data[18])
    awaySecondColor = str(data[19])


    basketballCtrl = Tk()
    basketballCtrl.configure(bg='#000000')
    basketballCtrl.title("Scorecast Basketball Scoreboard Controller")
    basketballCtrl.geometry('600x510')
    app = CtrlApp(basketballCtrl, ip, port, s, data).start()

    basketballCtrl.mainloop()

