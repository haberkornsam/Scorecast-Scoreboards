from tkinter import *
from threading import *
from socket import *
from time import *
import easygui
import xml.etree.ElementTree as ET

#control values
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
matchScoreLy = 100
awayScoreLx =590
teamEditScorey=145
hscore1x = 8
hscore2x = 73
hscore3x = 138
ascore1x = 600-hscore3x
ascore2x = 600-hscore2x
ascore3x = 600-hscore1x
scorey = 222
hFoulLabx = 35
aFoulLabx = 600-hFoulLabx
foulLaby = 260
hFoulLx = 10
FoulLy = 300
aFoulLx = 600-hFoulLx
homeBonusx = 165
awayBonusx = 600-homeBonusx
foulAdy = 295
foulSubty = 320
homePossx = 215
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
priColory =  375
secColory = 400

class Receive(Thread):
    def __init__(self, s, app):
        Thread.__init__(self)
        self.s = s
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
                    if text[1]:
                        self.app.changeTimeRecv(text[1], text[2])
                elif recvText == 'ChangeTime':
                    self.app.changeTimeRecv(text[1], text[2])
                elif recvText == 'homeTeam':
                    self.app.changeHTeamRecv(text[1]) #actually the wrestlersName
                elif recvText == 'awayTeam':
                    self.app.changeATeamRecv(text[1]) #actually the wrestlers name
                elif recvText == 'homeScore':
                    self.app.changeHomeScoreRecv(text[1]) #match score
                elif recvText == 'awayScore':
                    self.app.changeAwayScoreRecv(text[1]) #match score
                elif recvText == 'hTeamScore':
                    self.app.changeHTeamScoreRecv(text[1])
                elif recvText == 'aTeamScore':
                    self.app.changeATeamScoreRecv(text[1])
                elif recvText == 'period':
                    self.app.changePeriodRecv(text[1])
                elif recvText == 'homePrimary':
                    self.app.changeHPRecv(text[1])
                elif recvText == 'homeSecondary':
                    self.app.changeHSRecv(text[1])
                elif recvText == 'awayPrimary':
                    self.app.changeAPRecv(text[1])
                elif recvText == 'awaySecondary':
                    self.app.changeASRecv(text[1])
                elif recvText == 'hAbrev':
                    self.app.changeHAbrevRecv(text[1])
                elif recvText == 'aAbrev':
                    self.app.changeAAbrevRecv(text[1])
                elif recvText == 'class':
                    self.app.changeWeightClassRecv(text[1])
                elif recvText == 'sync':
                    self.app.changeHTeamRecv(text[1])
                    self.app.changeATeamRecv(text[2])
                    self.app.changeHomeScoreRecv(text[3])
                    self.app.changeAwayScoreRecv(text[4])
                    self.app.changeHTeamScoreRecv(text[5])
                    self.app.changeATeamScoreRecv(text[6])
                    self.app.changePeriodRecv(text[7])
                    self.app.changeHPRecv(text[8])
                    self.app.changeHSRecv(text[9])
                    self.app.changeAPRecv(text[10])
                    self.app.changeASRecv(text[11])
                    self.app.changeHAbrevRecv(text[12])
                    self.app.changeAAbrevRecv(text[13])
                    self.app.changeWeightClassRecv(text[14])
                    self.app.stopClockRecv()
                    self.app.changeTimeRecv(float(text[15]), float(text[16]))


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
        self._startingTime = 120
        self._elapsedtime = 0.0
        self._running = 0
        self._minutes = 0
        self._seconds = 0
        self.timestr = StringVar()
        self.formatted=''
        self.l = Label(self, text=self.formatted, width=20)
        self.l.grid(row=0, column=3, columnspan=3)
        self._setTime(self._elapsedtime)


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
    def startClockRecv(self):
        global runnin
        runnin = 'Stop'
        self.star.configure(text = runnin)
        self.sw.Start()

    def stopClockRecv(self):
        global runnin
        runnin = 'Start'
        self.star.configure(text = runnin)
        self.sw.Stop()

    def changeHTeamRecv(self, newName):
        global homeTeam
        homeTeam = newName
        self.homeLabel.configure(text = homeTeam)

    def changeATeamRecv(self, newName):
        global awayTeam
        awayTeam = newName
        self.awayLabel.configure(text = awayTeam)

    def changeHomeScoreRecv(self, newScore):
        global homeScore
        homeScore = int(newScore)
        self.homeScoreL.configure(text = homeScore)

    def changeAwayScoreRecv(self, newScore):
        global awayScore
        awayScore = int(newScore)
        self.awayScoreL.configure(text = awayScore)

    def changeHTeamScoreRecv(self, newScore):
        global hTeamScore
        hTeamScore = int(newScore)
        self.hTeamScoreL.configure(text = hTeamScore)

    def changeATeamScoreRecv(self, newScore):
        global aTeamScore
        aTeamScore  = int(newScore)
        self.aTeamScoreL.configure(text = aTeamScore)

    def changePeriodRecv(self, newPeriod):
        global half
        half = newPeriod
        self.halfLabel.configure(text = half)

    def changeHPRecv(self, newColor):
        global homePrimaryColor
        homePrimaryColor = newColor

    def changeHSRecv(self, newColor):
        global homeSecondColor
        homeSecondColor = newColor

    def changeAPRecv(self, newColor):
        global awayPrimaryColor
        awayPrimaryColor = newColor

    def changeASRecv(self, newColor):
        global awaySecondColor
        awaySecondColor = newColor

    def changeHAbrevRecv(self, newName):
        global hAbrev
        hAbrev = newName
        self.homeAbrevL.configure(text = hAbrev)
    def changeAAbrevRecv(self, newName):
        global aAbrev
        aAbrev = newName
        self.awayAbrevL.configure(text = aAbrev)

    def changeWeightClassRecv(self, newClass):
        global weightClass
        weightClass = newClass
        self.weightClassCtrl.configure(text = weightClass)

    def changeTimeRecv(self, timeM, timeS):
        global runnin
        runnin = 'Start'
        self.sw.Stop()
        self.star.configure(text = runnin)
        self.sw.setClock(float(timeM), float(timeS))

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
            self.send('Stop', self.sw.getMinutes(), self.sw.getSeconds())

    def changeTime(self, event):
        global runnin
        self.sw.Stop()
        runnin = "Stop"
        self.star.configure(text=runnin)
        self.send('Stop', self.sw.getMinutes(), self.sw.getSeconds())
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

    def saveAwayTeam(self,event):
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
        self.homeScoreL.place(x=homeScoreLx, y=matchScoreLy, anchor='nw')

    def awayScoreOverride(self, event):
        global awayScore
        awayScore = int(self.aEditScore.get())
        self.awayScoreFileUpdate()
        self.aEditScore.place_forget()
        self.awayScoreL.place(x=awayScoreLx, y=matchScoreLy, anchor='ne')

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

    def changehTeamScore(self, event):
        self.hTeamScoreL.place_forget()
        self.hTeamScoreIn.place(x=hFoulLx, y=FoulLy, anchor='nw')

    def changeaTeamScore(self, event):
        self.aTeamScoreL.place_forget()
        self.aTeamScoreIn.place(x=aFoulLx, y=FoulLy, anchor='ne')

    def submithTeamScore(self, event):
        global hTeamScore
        self.hTeamScoreL.place(x=hFoulLx, y=FoulLy, anchor='nw')
        self.hTeamScoreIn.place_forget()
        self.hTeamScore = int(self.hTeamScoreIn.get())
        self.hTeamScoreUpdate()

    def submitaTeamScore(self, event):
        global aTeamScore
        self.aTeamScoreL.place(x=aFoulLx, y=FoulLy, anchor='ne')
        self.aTeamScoreIn.place_forget()
        aTeamScore = int(self.aTeamScoreIn.get())
        self.aTeamScoreUpdate()

    def hTeamScoreSix(self, event):
        global hTeamScore
        hTeamScore += 6
        self.hTeamScoreUpdate()

    def aTeamScoreSix(self, event):
        global aTeamScore
        aTeamScore += 6
        self.aTeamScoreUpdate()

    def hTeamScoreThree(self, event):
        global hTeamScore
        hTeamScore += 3
        self.hTeamScoreUpdate()

    def aTeamScoreThree(self, event):
        global aTeamScore
        aTeamScore += 3
        self.aTeamScoreUpdate()

    def hTeamScoreUpdate(self):
        global hTeamScore
        self.hTeamScoreL.configure(text=hTeamScore)
        self.send('hTeamScore', hTeamScore)

    def aTeamScoreUpdate(self):
        global aTeamScore
        self.aTeamScoreL.configure(text=aTeamScore)
        self.send('aTeamScore', aTeamScore)

    def resetMatchScore(self, event):
        global homeScore, awayScore
        homeScore = 0
        awayScore = 0
        self.homeScoreFileUpdate()
        self.awayScoreFileUpdate()

    def changeHalf(self, event):
        self.halfLabel.place_forget()
        self.halfIn.place(x=centerx, y=teamEditScorey, anchor='n')

    def submitHalf(self, event):
        global half
        self.halfIn.place_forget()
        self.halfLabel.place(x=centerx, y=teamEditScorey, anchor='n')
        half = str(self.halfIn.get())
        self.halfLabel.configure(text=half)
        self.send('period', half)

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
        self.send('changeHP', homePrimaryColor)

    def subHS(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        homeSecondColor = str(self.hSecIn.get())
        self.hSecIn.place_forget()
        self.setHSecond.place(x=hcolorx, y=secColory, anchor='nw')
        self.send('changeHS', homeSecondColor)

    def subAP(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        awayPrimaryColor = str(self.aPriIn.get())
        self.aPriIn.place_forget()
        self.setAPrimary.place(x=acolorx, y=priColory, anchor='ne')
        self.send('changeAP', awayPrimaryColor)

    def subAS(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        awaySecondColor = str(self.aSecIn.get())
        self.aSecIn.place_forget()
        self.setASecond.place(x=acolorx, y=secColory, anchor='ne')
        self.send('changeAS', awaySecondColor)

    def updateTeamNames(self):
        self.homeLabel.configure(text=homeTeam)
        self.awayLabel.configure(text=awayTeam)

    def changeHomeAbrev(self, event):
        self.homeAbrevL.place_forget()
        self.homeAbrevIn.place(x=homeLabelx, y=10, anchor='nw')

    def subHomeAbrev(self, event):
        global hAbrev
        hAbrev = str(self.homeAbrevIn.get())
        self.homeAbrevL.config(text=hAbrev)
        self.send('hAbrev', hAbrev)
        self.homeAbrevIn.place_forget()
        self.homeAbrevL.place(x=homeLabelx, y=10, anchor='nw')

    def changeAwayAbrev(self, event):
        self.awayAbrevL.place_forget()
        self.awayAbrevIn.place(x=awayLabelx, y=10, anchor='ne')

    def subAwayAbrev(self, event):
        global aAbrev
        aAbrev = str(self.awayAbrevIn.get())
        self.awayAbrevL.config(text=aAbrev)
        self.send('aAbrev', aAbrev)
        self.awayAbrevIn.place_forget()
        self.awayAbrevL.place(x=awayLabelx, y=10, anchor='ne')

    def abrevUpdate(self):
        self.homeAbrevL.config(text=hAbrev)
        self.awayAbrevL.config(text=aAbrev)

    def changeWeightClass(self, event):
        self.weightClassCtrl.place_forget()
        self.weightClassIn.place(x=centerx, y=FoulLy, anchor='n')

    def subWeightClass(self, event):
        global weightClass
        weightClass = str(self.weightClassIn.get())
        self.weightUpdate()
        self.weightClassCtrl.place(x=centerx, y=FoulLy, anchor='n')
        self.weightClassIn.place_forget()

    def weightUpdate(self):
        self.weightClassCtrl.config(text=weightClass)
        self.send('class', weightClass)

    def sync(self):
        global homeTeam, awayTeam, homeScore, awayScore, aTeamScore, hTeamScore, half, homePrimaryColor, \
            homeSecondColor, awayPrimaryColor, awaySecondColor, hAbrev, aAbrev, weightClass
        data = '~sync`'
        data += str(homeTeam) +'`'
        data += str(awayTeam) +'`'

        data += str(homeScore) +'`'
        data += str(awayScore) +'`'

        data += str(hTeamScore) +'`'
        data += str(aTeamScore) +'`'

        data += str(half) +'`'


        data += str(homePrimaryColor) +'`'
        data += str(homeSecondColor) +'`'

        data += str(awayPrimaryColor) +'`'
        data += str(awaySecondColor) +'`'

        data += str(hAbrev) +'`'
        data += str(aAbrev) +'`'

        data += str(weightClass) +'`'

        data += str(self.sw.getMinutes()) +'`'
        data += str(self.sw.getSeconds()) +'`'

        self.s.send(data.encode())

    def updateLabels(self):
        self.sync()
        self.updateTeamNames()
        self.homeScoreFileUpdate()
        self.awayScoreFileUpdate()
        self.hTeamScoreUpdate()
        self.aTeamScoreUpdate()
        self.weightUpdate()
        self.abrevUpdate()

    def openConfig(self, event):
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
            self.sw.setClock(int(tree[3][0].text), float(tree[3][1].text))
            weightClass = str(tree[4].text)
            self.updateLabels()

    def saveConfig(self, event):
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
        minutes1.text = str(self.sw.getMinutes())
        seconds1 = ET.SubElement(clock1, 'Seconds')
        seconds1.text = str(self.sw.getSeconds())
        weightClass1 = ET.SubElement(wrestling1, 'weightClass')
        weightClass1.text = str(weightClass)
        myData = ET.tostring(wrestling1).decode("utf-8")

        configFile = open(str(easygui.filesavebox()) + '.xml', 'w')
        configFile.write(myData)

    def __init__(self, master, s, data):
        self.s = s
        Thread.__init__(self)

        self.sw = StopWatch(master)
        self.sw.place(x=300, y=10, anchor='n')
        self.sw.setClock(float(data[15]), float(data[16]))

        # start button
        self.star = Label(master, text=runnin, width=20)
        self.star.bind('<Button-1>', self.toggleStartLabel)
        self.star.place(x=startx, y=starty, anchor='n')

        # set Clock Button
        self.setClock = Label(master, text='Set Time', width=20)
        self.setClock.bind('<Button-1>', self.changeTime)
        self.setClock.place(x=setClockx, y=setClocky, anchor='n')

        # Enter time entries
        self.enterTimeM = Entry(master, text='mm', width=5)
        self.enterTimeM.place(x=enterTimeMx, y=enterTimeMy, anchor='n')
        self.enterTimeM.place_forget()
        self.enterTimeColon = Label(master, text=':', width=3)
        self.enterTimeColon.place(x=enterTimeColonx, y=enterTimeColony, anchor='n')
        self.enterTimeColon.place_forget()
        self.enterTimeS = Entry(master, text="ss", width=5)
        self.enterTimeS.place(x=enterTimeSx, y=enterTimeSy, anchor='n')
        self.enterTimeS.place_forget()

        # submit time button
        self.sub = Label(master, text="Submit", width=20)
        self.sub.bind('<Button-1>', self.submitTime)
        self.sub.place_forget()

        # Team Abrev labels
        self.homeAbrevL = Label(master, text=hAbrev, width=20)
        self.homeAbrevL.bind('<Button-1>', self.changeHomeAbrev)
        self.homeAbrevL.place(x=homeLabelx, y=10, anchor='nw')

        self.homeAbrevIn = Entry(master, width=20)
        self.homeAbrevIn.bind('<Return>', self.subHomeAbrev)
        self.homeAbrevIn.place_forget()

        self.awayAbrevL = Label(master, text=aAbrev, width=20)
        self.awayAbrevL.bind('<Button-1>', self.changeAwayAbrev)
        self.awayAbrevL.place(x=awayLabelx, y=10, anchor='ne')

        self.awayAbrevIn = Entry(master, width=20)
        self.awayAbrevIn.bind('<Return>', self.subAwayAbrev)
        self.awayAbrevIn.place_forget()

        # Athlete Name Labels including Changing Names
        self.homeLabel = Label(master, text=homeTeam, width=20)
        self.homeLabel.bind('<Button-1>', self.changeHomeTeam)
        self.homeLabel.place(x=homeLabelx, y=teamLabely, anchor='nw')
        self.awayLabel = Label(master, text=awayTeam, width=20)
        self.awayLabel.bind('<Button-1>', self.changeAwayTeam)
        self.awayLabel.place(x=awayLabelx, y=teamLabely, anchor='ne')

        # New team Name Inputs
        self.homeInput = Entry(master, width=19)
        self.homeInput.bind('<Return>', self.saveHomeTeam)
        self.homeInput.place_forget()
        self.awayInput = Entry(master, width=19)
        self.awayInput.bind('<Return>', self.saveAwayTeam)
        self.awayInput.place_forget()

        # Score Elements
        # Score Labels
        self.homeScoreL = Label(master, text=homeScore, width=20, height=7)
        self.homeScoreL.bind("<Button-1>", self.editHomeScore)
        self.homeScoreL.place(x=homeScoreLx, y=matchScoreLy, anchor='nw')
        self.awayScoreL = Label(master, text=awayScore, width=20, height=7)
        self.awayScoreL.bind("<Button-1>", self.editAwayScore)
        self.awayScoreL.place(x=awayScoreLx, y=matchScoreLy, anchor='ne')

        # Edit Scores
        self.hEditScore = Entry(master, width=19)
        self.hEditScore.bind('<Return>', self.homeScoreOverride)
        self.hEditScore.place_forget()
        self.aEditScore = Entry(master, width=19)
        self.aEditScore.bind('<Return>', self.awayScoreOverride)
        self.aEditScore.place_forget()

        # Increase Score Buttons
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

        # Foul elements

        # Number of Fouls
        self.hTeamScoreL = Label(master, text=hTeamScore, width=12, height=2)
        self.hTeamScoreL.bind('<Button-1>', self.changehTeamScore)
        self.hTeamScoreL.place(x=hFoulLx, y=FoulLy, anchor='nw')
        self.aTeamScoreL = Label(master, text=aTeamScore, width=12, height=2)
        self.aTeamScoreL.bind('<Button-1>', self.changeaTeamScore)
        self.aTeamScoreL.place(x=aFoulLx, y=FoulLy, anchor='ne')

        # Foul Inputs
        self.hTeamScoreIn = Entry(master, width=12)
        self.hTeamScoreIn.bind('<Return>', self.submithTeamScore)
        self.hTeamScoreIn.place(x=hFoulLx, y=FoulLy, anchor='nw')
        self.hTeamScoreIn.place_forget()
        self.aTeamScoreIn = Entry(master, width=12)
        self.aTeamScoreIn.bind('<Return>', self.submitaTeamScore)
        self.aTeamScoreIn.place(x=aFoulLx, y=FoulLy, anchor='ne')
        self.aTeamScoreIn.place_forget()

        self.hTeamScoreAd6 = Label(master, text="+6", width=6, height=1)
        self.hTeamScoreAd6.bind('<Button-1>', self.hTeamScoreSix)
        self.hTeamScoreAd6.place(x=homeBonusx, y=foulAdy, anchor='n')
        self.aTeamScoreAd6 = Label(master, text="+6", width=6)
        self.aTeamScoreAd6.bind('<Button-1>', self.aTeamScoreSix)
        self.aTeamScoreAd6.place(x=awayBonusx, y=foulAdy, anchor='n')

        self.hTeamScoreAd3 = Label(master, text='+3', width=6, height=1)
        self.hTeamScoreAd3.bind('<Button-1>', self.hTeamScoreThree)
        self.hTeamScoreAd3.place(x=homeBonusx, y=foulSubty, anchor='n')

        self.aTeamScoreAd3 = Label(master, text='+3', width=6)
        self. aTeamScoreAd3.bind('<Button-1>', self.aTeamScoreThree)
        self.aTeamScoreAd3.place(x=awayBonusx, y=foulSubty, anchor='n')

        # Clear Team Fouls
        self.resetMatchLabel = Label(master, text='Reset Match Score', width=15)
        self.resetMatchLabel.bind('<Button-1>', self.resetMatchScore)
        self.resetMatchLabel.place(x=centerx, y=scorey, anchor='n')

        # Team Foul Labels
        self.hFoulLab = Label(master, text='Home Team Score', fg='#ffffff', bg='#000000')
        self.hFoulLab.place(x=hFoulLabx, y=foulLaby, anchor='nw')
        self.aFoulLab = Label(master, text='Away Team Score', fg='#ffffff', bg='#000000')
        self.aFoulLab.place(x=aFoulLabx, y=foulLaby, anchor='ne')

        # Period Buttons
        self.halfLabel = Label(master, text=half, width=5)
        self.halfLabel.bind('<Button-1>', self.changeHalf)
        self.halfLabel.place(x=centerx, y=teamEditScorey, anchor='n')

        # Period Input
        self.halfIn = Entry(master, width=5)
        self.halfIn.bind('<Return>', self.submitHalf)
        self.halfIn.place_forget()

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

        # Weight Class Ctrl

        self.weightClassCtrl = Label(master, text=weightClass, width=15)
        self.weightClassCtrl.bind('<Button-1>', self.changeWeightClass)
        self.weightClassCtrl.place(x=centerx, y=FoulLy, anchor='n')

        self.weightClassIn = Entry(master, width=15)
        self.weightClassIn.bind('<Return>', self.subWeightClass)
        self.weightClassIn.place_forget()
        Receive(s, self).start()

    def send(self, arg, value=None, value2 = None):
        data1 = '~'+arg+'`'
        if value != None:
            data1 += str(value) +'`'
        if value2 != None:
            data1 += str(value2) +'`'
        self.s.send(data1.encode())



def start(data, s):
    global runnin, homeTeam, awayTeam, hAbrev, aAbrev, hTeamScore, aTeamScore, homeScore, awayScore, half,\
        homePrimaryColor, awayPrimaryColor, homeSecondColor, awaySecondColor, weightClass

    runnin = 'Start'
    homeTeam = str(data[1])
    awayTeam = str(data[2])
    hAbrev = str(data[3])
    aAbrev = str(data[4])

    hTeamScore = int(data[5])
    aTeamScore = int(data[6])

    homeScore = int(data[7])
    awayScore = int(data[8])
    half = str(data[9])

    homePrimaryColor = str(data[10])
    homeSecondColor = str(data[11])
    awayPrimaryColor = str(data[12])
    awaySecondColor = str(data[13])
    weightClass = str(data[14])

    wrestlingCtrl = Tk()
    wrestlingCtrl.configure(bg='#000000')
    wrestlingCtrl.title("Scorecast Wrestling Scoreboard Controller")
    wrestlingCtrl.geometry('600x435')
    app = CtrlApp(wrestlingCtrl, s, data).start()

    wrestlingCtrl.mainloop()

