from tkinter import *
from threading import *
from socket import *
import easygui
import xml.etree.ElementTree as ET

windowWidth = 550

centerx = windowWidth / 2
homeLabelx = 10

teamLabely = 10
inningLabely = teamLabely + 30
inInningy = inningLabely + 32
baseCtrlCanvy = inInningy + 70
subBasey = baseCtrlCanvy + 40

teamScoreLy = teamLabely + 95
scorey = teamScoreLy + 77
clearCounty = scorey+50
countLy = clearCounty + 25
ballStrikey = countLy + 25
outy = ballStrikey + 25
outStaticy = outy + 25
priColory = outy
configy = outStaticy

windowHeight = configy + 20

awayLabelx = windowWidth - homeLabelx
homeScoreLx = 10
awayScoreLx = windowWidth - homeScoreLx

scoreOffset = 48
addScoreWidth = 4
hscore1x = 10
hscore2x = hscore1x + scoreOffset
hscore3x = hscore2x + scoreOffset
hscore4x = hscore3x + scoreOffset

ascore1x = windowWidth - hscore4x
ascore2x = windowWidth - hscore3x
ascore3x = windowWidth - hscore2x
ascore4x = windowWidth - hscore1x

hcolorx = 10
acolorx = windowWidth - hcolorx
openconfigx = 10
saveconfigx = windowWidth - openconfigx

ctrlBaseSize = 13
ctrlBaseOffset = 7

baseCtrlWidth = 60
baseCtrlHeight = 60

firstCtrlx = (baseCtrlWidth / 2) + 3
firstCtrly = (baseCtrlHeight / 2) + ctrlBaseOffset
secondCtrlx = baseCtrlWidth / 2
secondCtrly = (baseCtrlHeight / 2) - 3 + ctrlBaseOffset
thirdCtrlx = (baseCtrlWidth / 2) - 3
thirdCtrly = (baseCtrlHeight / 2) + ctrlBaseOffset

firstCtrlPts = [firstCtrlx + ctrlBaseSize, firstCtrly - ctrlBaseSize, firstCtrlx + ctrlBaseSize + ctrlBaseSize,
                       firstCtrly, firstCtrlx + ctrlBaseSize, firstCtrly + ctrlBaseSize, firstCtrlx, firstCtrly]
secondCtrlPts = [secondCtrlx, secondCtrly - ctrlBaseSize - ctrlBaseSize, secondCtrlx + ctrlBaseSize,
                     secondCtrly - ctrlBaseSize, secondCtrlx, secondCtrly, secondCtrlx - ctrlBaseSize, secondCtrly - ctrlBaseSize]
thirdCtrlPts = [thirdCtrlx - ctrlBaseSize, thirdCtrly - ctrlBaseSize, thirdCtrlx, thirdCtrly, thirdCtrlx - ctrlBaseSize,
                    thirdCtrly + ctrlBaseSize,thirdCtrlx - ctrlBaseSize - ctrlBaseSize, thirdCtrly]

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

                if recvText == 'homeTeam':
                    self.app.changeHomeTeamRecv(text[1])
                elif recvText == 'awayTeam':
                    self.app.changeAwayTeamRecv(text[1])
                elif recvText == 'homeScore':
                    self.app.changeHomeScoreRecv(text[1])
                elif recvText == 'awayScore':
                    self.app.changeAwayScoreRecv(text[1])
                elif recvText == 'changeInning':
                    self.app.changeInningRecv(text[1])
                    self.app.changeTopBottomRecv(text[2])
                    self.app.activateFirstRecv(text[3])
                    self.app.activateSecondRecv(text[4])
                    self.app.activateThirdRecv(text[5])
                    self.app.changeCountRecv(text[6], text[7])
                    self.app.changeOutsRecv(text[8], text[9])
                elif recvText == 'changeBases':
                    self.app.activateFirstRecv(text[1])
                    self.app.activateSecondRecv(text[2])
                    self.app.activateThirdRecv(text[3])
                elif recvText == 'changeAP':
                    self.app.changeAPRecv(text[1])
                elif recvText == 'changeHP':
                    self.app.changeHPRecv(text[1])
                elif recvText == 'count':
                    self.app.changeCountRecv(text[2], text[1])
                elif recvText == 'changeOuts':
                    self.app.changeOutsRecv(text[1], text[2])
                    self.app.changeCountRecv(text[4], text[3])
                elif recvText == 'sync':
                    self.app.changeHomeTeamRecv(text[1])
                    self.app.changeAwayTeamRecv(text[2])
                    self.app.changeHomeScoreRecv(text[3])
                    self.app.changeAwayScoreRecv(text[4])
                    self.app.changeInningRecv(text[5])
                    self.app.changeTopBottomRecv(text[6])
                    self.app.activateFirstRecv(text[7])
                    self.app.activateSecondRecv(text[8])
                    self.app.activateThirdRecv(text[9])
                    self.app.changeOutsRecv(text[10], text[11])
                    self.app.changeCountRecv(text[12], text[13])
                    self.app.changeHPRecv(text[14])
                    self.app.changeAPRecv(text[15])

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

class CtrlApp(Thread):
    def changeHPRecv(self, newColor):
        global homePrimaryColor
        homePrimaryColor = newColor

    def changeAPRecv(self, newColor):
        global awayPrimaryColor
        awayPrimaryColor = newColor

    def changeCountRecv(self, newStrikes, newBalls):
        global balls, strikes
        balls = int(newBalls)
        strikes = int(newStrikes)
        self.countL.configure(text = str(balls)+'-'+str(strikes))

    def changeOutsRecv(self, newOuts, word):
        global outs, outOuts
        outs = int(newOuts)
        outOuts = word
        self.outStaticL.configure(text=str(outs)+' ' + outOuts)

    def activateFirstRecv(self, newBool):
        global firstActive
        firstActive = newBool
        if (firstActive == 'true'):
            self.baseCtrlCanvas.itemconfig('firstCtrlBase', fill=yellowColor, outline=yellowColor)
        elif (firstActive == 'false'):
            self.baseCtrlCanvas.itemconfig('firstCtrlBase', fill='#000000', outline='#ffffff')

    def activateSecondRecv(self, newBool):
        global secondActive
        secondActive = newBool
        if (secondActive == 'true'):
            self.baseCtrlCanvas.itemconfig('secondCtrlBase', fill=yellowColor, outline=yellowColor)
        elif (secondActive == 'false'):
            self.baseCtrlCanvas.itemconfig('secondCtrlBase', fill='#000000', outline='#ffffff')

    def activateThirdRecv(self, newBool):
        global thirdActive
        thirdActive = newBool
        if (thirdActive == 'true'):
            self.baseCtrlCanvas.itemconfig('thirdCtrlBase', fill=yellowColor, outline=yellowColor)
        elif (thirdActive == 'false'):
            self.baseCtrlCanvas.itemconfig('thirdCtrlBase', fill='#000000', outline='#ffffff')



    def changeHomeScoreRecv(self, newScore):
        global homeScore
        homeScore = int(newScore)
        self.homeScoreL.configure(text=homeScore)

    def changeAwayScoreRecv(self, newScore):
        global awayScore
        awayScore = int(newScore)
        self.awayScoreL.configure(text=awayScore)

    def changeInningRecv(self, newInning):
        global inning
        inning = int(newInning)
        self.inningLabel.configure(text=inning)

    def changeTopBottomRecv(self, newValue):
        global topBottom
        topBottom = newValue
        if topBottom == "top":
            self.topBottomL.coords('ctrlArrow', self.upCtrlArrow)
        elif topBottom == 'bottom':
            self.topBottomL.coords('ctrlArrow', self.downCtrlArrow)

    def changeHomeTeamRecv(self, newTeam):
        global homeTeam
        homeTeam = newTeam
        self.homeLabel.configure(text=homeTeam)

    def changeAwayTeamRecv(self, newTeam):
        global awayTeam
        awayTeam = newTeam
        self.awayLabel.configure(text = awayTeam)



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
        self.homeLabel.place(x=homeLabelx, y=teamLabely, anchor='nw')
        self.send('homeTeam', homeTeam)

    def saveAwayTeam(self, event):
        global awayTeam
        awayTeam = str(self.awayInput.get())
        self.awayInput.place_forget()
        self.awayLabel.configure(text=awayTeam)
        self.awayLabel.place(x=awayLabelx, y=teamLabely, anchor='ne')
        self.send('awayTeam', awayTeam)

    def editHomeScore(self, event):
        self.homeScoreL.place_forget()
        self.hEditScore.place(x=homeScoreLx, y=teamScoreLy, anchor='w')

    def editAwayScore(self, event):
        self.awayScoreL.place_forget()
        self.aEditScore.place(x=awayScoreLx, y=teamScoreLy, anchor='e')

    def homeScoreOverride(self, event):
        global homeScore
        homeScore = int(self.hEditScore.get())
        self.homeScoreFileUpdate()
        self.hEditScore.place_forget()
        self.homeScoreL.place(x=homeScoreLx, y=teamScoreLy, anchor='w')

    def awayScoreOverride(self, event):
        global awayScore
        awayScore = int(self.aEditScore.get())
        self.awayScoreFileUpdate()
        self.aEditScore.place_forget()
        self.awayScoreL.place(x=awayScoreLx, y=teamScoreLy, anchor='e')

    def homeScoreFileUpdate(self):
        global homeScore, awayScore
        self.send('homeScore', homeScore)
        self.homeScoreL.configure(text=homeScore)

    def awayScoreFileUpdate(self):
        global homeScore, awayScore
        self.send('awayScore', awayScore)
        self.awayScoreL.configure(text=awayScore)

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

    def hScore4(self, event):
        global homeScore
        homeScore += 4
        self.homeScoreFileUpdate()

    def aScore4(self, event):
        global awayScore
        awayScore += 4
        self.awayScoreFileUpdate()

    def changeinning(self, event):
        self.inningLabel.place_forget()
        self.inningIn.place(x=centerx, y=teamScoreLy, anchor='n')

    def increaseInning(self, event):
        global inning, topBottom
        inning += 1
        topBottom = 'top'
        self.updateInning()

    def changeTopBottom(self, event):
        global topBottom, inning, outs
        outs = 3
        self.updateOuts()

    def updateInning(self):
        global inning, topBottom, firstActive, secondActive, thirdActive, outs, outOuts, balls, strikes
        self.inningLabel.config(text=inning)
        if topBottom == 'top':
            self.topBottomL.coords('ctrlArrow', self.upCtrlArrow)

        elif topBottom == 'bottom':
            self.topBottomL.coords('ctrlArrow', self.downCtrlArrow)

        balls = 0
        strikes = 0
        outs = 0
        outOuts = 'Out'
        firstActive = 'false'
        secondActive = 'false'
        thirdActive = 'false'
        self.send('changeInning', inning, [topBottom, firstActive, secondActive, thirdActive, balls, strikes, outs, outOuts])
        self.updateBases()
        self.clearCount()

    def safeUpdateInning(self):
        global inning, topBottom, firstActive, secondActive, thirdActive
        self.inningLabel.config(text=inning)
        if topBottom == 'top':
            self.topBottomL.coords('ctrlArrow', self.upCtrlArrow)

        elif topBottom == 'bottom':
            self.topBottomL.coords('ctrlArrow', self.downCtrlArrow)

        self.send('changeInning', inning, [topBottom, firstActive, secondActive, thirdActive, balls, strikes, outs, outOuts])

    def submitinning(self, event):
        global inning
        self.inningIn.place_forget()
        self.inningLabel.place(x=centerx, y=teamScoreLy, anchor='n')
        inning = int(self.inningIn.get())
        self.inningLabel.configure(text=str(inning))
        self.send('changeInning', inning, [topBottom, firstActive, secondActive, thirdActive, balls, strikes, outs, outOuts])


    def activateFirst(self, event):
        global firstActive
        if (firstActive == 'true'):
            self.baseCtrlCanvas.itemconfig('firstCtrlBase', fill='#000000', outline='#ffffff')
            firstActive = 'false'
        elif (firstActive == 'false'):
            self.baseCtrlCanvas.itemconfig('firstCtrlBase', fill=yellowColor, outline=yellowColor)
            firstActive = 'true'

    def activateSecond(self, event):
        global secondActive
        if (secondActive == 'true'):
            self.baseCtrlCanvas.itemconfig('secondCtrlBase', fill='#000000', outline='#ffffff')
            secondActive = 'false'
        elif (secondActive == 'false'):
            self.baseCtrlCanvas.itemconfig('secondCtrlBase', fill=yellowColor, outline=yellowColor)
            secondActive = 'true'

    def activateThird(self, event):
        global thirdActive
        if (thirdActive == 'true'):
            self.baseCtrlCanvas.itemconfig('thirdCtrlBase', fill='#000000', outline='#ffffff')
            thirdActive = 'false'
        elif (thirdActive == 'false'):
            self.baseCtrlCanvas.itemconfig('thirdCtrlBase', fill=yellowColor, outline=yellowColor)
            thirdActive = 'true'

    def submitBases(self, event):
        self.updateBases()

    def updateBases(self):
        if (firstActive == 'true'):
            self.baseCtrlCanvas.itemconfig('firstCtrlBase', fill=yellowColor, outline=yellowColor)
        elif (firstActive == 'false'):
            self.baseCtrlCanvas.itemconfig('firstCtrlBase', fill='#000000', outline='#ffffff')
        if (secondActive == 'true'):
            self.baseCtrlCanvas.itemconfig('secondCtrlBase', fill=yellowColor, outline=yellowColor)
        elif (secondActive == 'false'):
            self.baseCtrlCanvas.itemconfig('secondCtrlBase', fill='#000000', outline='#ffffff')
        if (thirdActive == 'true'):
            self.baseCtrlCanvas.itemconfig('thirdCtrlBase', fill=yellowColor, outline=yellowColor)
        elif (thirdActive == 'false'):
            self.baseCtrlCanvas.itemconfig('thirdCtrlBase', fill='#000000', outline='#ffffff')
        self.send('changeBases', firstActive, [secondActive, thirdActive])

    def changeCount(self, event):
        global ballIn, strikeIn, countL
        self.countL.place_forget()
        self.ballIn.place(x=centerx - 6, y=countLy, anchor='e')
        self.strikeIn.place(x=centerx - 3, y=countLy, anchor='w')

    def submitCount(self, event):
        global ballIn, strikeIn, countL, strikes, balls
        if (self.ballIn.get() != ''):
            balls = int(self.ballIn.get())
        if (self.strikeIn.get() != ''):
            strikes = int(self.strikeIn.get())
        self.ballIn.place_forget()
        self.strikeIn.place_forget()
        self.updateCount()
        self.countL.place(x=centerx, y=countLy, anchor='c')

    def addBall(self, event):
        global balls, firstActive, secondActive, thirdActive, homeScore, awayScore
        if (balls == 3):
            self.clearCount()
            if (firstActive == 'false'):
                firstActive = 'true'
            elif (secondActive == 'false'):
                secondActive = 'true'
            elif (thirdActive == 'false'):
                thirdActive = 'true'
            else:
                if (topBottom == 'top'):
                    homeScore += 1
                    self.homeScoreFileUpdate()
                elif (topBottom == 'bottom'):
                    awayScore += 1
                    self.awayScoreFileUpdate()
            self.updateBases()
        else:
            balls += 1
        self.updateCount()

    def addStrike(self, event):
        global strikes, balls, outs
        if (strikes == 2):
            self.clearCount()
            outs += 1
            self.updateOuts()
        else:
            strikes += 1
        self.updateCount()

    def clearCount(self):
        global balls, strikes
        balls = 0
        strikes = 0
        self.updateCount()

    def resetCount(self, event):
        self.clearCount()

    def addOut(self, event):
        global outs

        outs += 1
        self.clearCount()
        self.updateOuts()

    def outInput(self, event):
        global outStaticL, outIn
        self.outStaticL.place_forget()
        self.outIn.place(x=centerx, y=outStaticy, anchor='c')

    def outInSub(self, event):
        global outs, outStaticL, outIn
        outs = int(self.outIn.get())
        self.outIn.place_forget()
        self.outStaticL.place(x=centerx, y=outStaticy, anchor='c')
        self.updateOuts()

    def updateOuts(self):
        global topBottom, outs, inning, outStaticL, outOuts, firstActive, secondActive, thirdActive
        if (outs >= 3):
            if (topBottom == 'top'):
                topBottom = 'bottom'
            elif (topBottom == 'bottom'):
                topBottom = 'top'
                inning += 1

            outs = 0
            outOuts = 'Out'
            firstActive = 'false'
            secondActive = 'false'
            thirdActive = 'false'
            self.updateInning()
        elif (outs == 2):
            outOuts = 'Outs'
            self.send('changeOuts', outs, [outOuts, balls, strikes])
        else:
            outOuts = 'Out'
            self.send('changeOuts', outs, [outOuts, balls, strikes])
        self.outStaticL.config(text=str(outs) + ' ' + outOuts)

    def updateCount(self):
        global countL, balls, strikes
        self.countL.config(text=str(balls) + '-' + str(strikes))
        self.send('count', balls, [strikes])

    def changeHPrimary(self, event):
        self.setHPrimary.place_forget()
        self.hPriIn.place(x=hcolorx, y=priColory, anchor='w')

    def changeAPrimary(self, event):
        self.setAPrimary.place_forget()
        self.aPriIn.place(x=acolorx, y=priColory, anchor='e')

    def subHP(self, event):
        global homePrimaryColor

        homePrimaryColor = str(self.hPriIn.get())
        self.send('changeHP', homePrimaryColor)
        self.hPriIn.place_forget()
        self.setHPrimary.place(x=hcolorx, y=priColory, anchor='w')

    def subAP(self, event):
        global awayPrimaryColor

        awayPrimaryColor = str(self.aPriIn.get())
        self.send('changeAP', awayPrimaryColor)
        self.aPriIn.place_forget()
        self.setAPrimary.place(x=acolorx, y=priColory, anchor='e')

    def updateTeamNames(self):
        self.homeLabel.configure(text=homeTeam)
        self.awayLabel.configure(text=awayTeam)

    def sync(self):
        data = '~sync`'
        data += str(homeTeam)+'`'
        data += str(awayTeam)+'`'
        data += str(homeScore)+'`'
        data += str(awayScore)+'`'
        data += str(inning)+'`'
        data += str(topBottom)+'`'
        data += str(firstActive)+'`'
        data += str(secondActive)+'`'
        data += str(thirdActive)+'`'
        data += str(outs)+'`'
        data += str(outOuts)+'`'
        data += str(strikes)+'`'
        data += str(balls)+'`'
        data += str(homePrimaryColor)+'`'
        data += str(awayPrimaryColor)+'`'
        self.s.send(data.encode())


    def updateLabels(self):
        self.sync()
        self.updateTeamNames()
        self.homeScoreFileUpdate()
        self.awayScoreFileUpdate()
        self.updateCount()
        self.safeUpdateInning()
        self.updateOuts()
        self.updateBases()

    def openConfig(self, event):
        global homeTeam, awayTeam, homeScore, awayScore, inning, homePrimaryColor, awayPrimaryColor, topBottom, outs, \
            balls, strikes, firstActive, secondActive, thirdActive

        tree = ET.parse(easygui.fileopenbox(filetypes=['*.xml'])).getroot()
        if (tree.tag == 'baseball'):
            homeTeam = str(tree[0][0].text)
            homeScore = int(tree[0][1].text)
            homePrimaryColor = str(tree[0][2].text)

            awayTeam = str(tree[1][0].text)
            awayScore = int(tree[1][1].text)
            awayPrimaryColor = str(tree[1][2].text)

            inning = int(tree[2].text)
            topBottom = str(tree[3].text)
            outs = int(tree[4].text)
            balls = int(tree[5].text)
            strikes = int(tree[6].text)
            firstActive = str(tree[7].text)
            secondActive = str(tree[8].text)
            thirdActive = str(tree[9].text)

            self.updateLabels()

    def saveConfig(self, event):
        global homeTeam, awayTeam, homeScore, awayScore, inning, homePrimaryColor, awayPrimaryColor, topBottom, outs, \
            balls, strikes, firstActive, secondActive, thirdActive
        baseball = ET.Element('baseball')
        homeTeam1 = ET.SubElement(baseball, 'homeTeam')
        hname1 = ET.SubElement(homeTeam1, 'name')
        hname1.text = str(homeTeam)
        hscore1 = ET.SubElement(homeTeam1, 'score')
        hscore1.text = str(homeScore)
        hPrimary1 = ET.SubElement(homeTeam1, 'primaryColor')
        hPrimary1.text = str(homePrimaryColor)

        awayTeam1 = ET.SubElement(baseball, 'awayTeam')
        aname1 = ET.SubElement(awayTeam1, 'name')
        aname1.text = str(awayTeam)
        ascore1 = ET.SubElement(awayTeam1, 'score')
        ascore1.text = str(awayScore)
        aPrimary1 = ET.SubElement(awayTeam1, 'primaryColor')
        aPrimary1.text = str(awayPrimaryColor)

        inning1 = ET.SubElement(baseball, 'inning')
        inning1.text = str(inning)
        topBottom1 = ET.SubElement(baseball, 'topOrBottom')
        topBottom1.text = str(topBottom)
        outs1 = ET.SubElement(baseball, 'outs')
        outs1.text = str(outs)
        balls1 = ET.SubElement(baseball, 'balls')
        balls1.text = str(balls)
        strikes1 = ET.SubElement(baseball, 'strikes')
        strikes1.text = str(strikes)
        first1 = ET.SubElement(baseball, 'ActiveFirst')
        first1.text = str(firstActive)
        second1 = ET.SubElement(baseball, 'ActiveSecond')
        second1.text = str(secondActive)
        third1 = ET.SubElement(baseball, 'ActiveThird')
        third1.text = str(thirdActive)

        myData = ET.tostring(baseball).decode("utf-8")
        configFile = open(easygui.filesavebox() + '.xml', 'w')
        configFile.write(myData)

    def __init__(self, master, s, data):
        self.s = s
        Thread.__init__(self)
        # Team Name Labels including Changing Names
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
        self.homeScoreL.place(x=homeScoreLx, y=teamScoreLy, anchor='w')
        self.awayScoreL = Label(master, text=awayScore, width=20, height=7)
        self.awayScoreL.bind("<Button-1>", self.editAwayScore)
        self.awayScoreL.place(x=awayScoreLx, y=teamScoreLy, anchor='e')

        # Edit Scores
        self.hEditScore = Entry(master, width=19)
        self.hEditScore.bind('<Return>', self.homeScoreOverride)
        self.hEditScore.place_forget()
        self.aEditScore = Entry(master, width=19)
        self.aEditScore.bind('<Return>', self.awayScoreOverride)
        self.aEditScore.place_forget()

        # Increase Score Buttons
        self.homeScore1 = Label(master, text='+1', width=addScoreWidth)
        self.homeScore1.bind("<Button-1>", self.hScore1)
        self.homeScore1.place(x=hscore1x, y=scorey, anchor='nw')
        self.homeScore2 = Label(master, text='+2', width=addScoreWidth)
        self.homeScore2.bind("<Button-1>", self.hScore2)
        self.homeScore2.place(x=hscore2x, y=scorey, anchor='nw')
        self.homeScore3 = Label(master, text='+3', width=addScoreWidth)
        self.homeScore3.bind("<Button-1>", self.hScore3)
        self.homeScore3.place(x=hscore3x, y=scorey, anchor='nw')
        self.homeScore4 = Label(master, text='+4', width=addScoreWidth)
        self.homeScore4.bind('<Button-1>', self.hScore4)
        self.homeScore4.place(x=hscore4x, y=scorey, anchor='nw')

        self.awayScore1 = Label(master, text='+1', width=addScoreWidth)
        self.awayScore1.bind("<Button-1>", self.aScore1)
        self.awayScore1.place(x=ascore1x, y=scorey, anchor='ne')
        self.awayScore2 = Label(master, text='+2', width=addScoreWidth)
        self.awayScore2.bind("<Button-1>", self.aScore2)
        self.awayScore2.place(x=ascore2x, y=scorey, anchor='ne')
        self.awayScore3 = Label(master, text='+3', width=addScoreWidth)
        self.awayScore3.bind("<Button-1>", self.aScore3)
        self.awayScore3.place(x=ascore3x, y=scorey, anchor='ne')
        self.awayScore4 = Label(master, text='+4', width=addScoreWidth)
        self.awayScore4.bind('<Button-1>', self.aScore4)
        self.awayScore4.place(x=ascore4x, y=scorey, anchor='ne')

        # Inning Buttons

        self.inningStatic = Label(master, text='Inning', width=5, bg='#000000', fg='#ffffff')
        self.inningStatic.place(x=centerx, y=inningLabely - 5, anchor='s')

        self.inningLabel = Label(master, text=inning, width=5)
        self.inningLabel.bind('<Button-1>', self.changeinning)
        self.inningLabel.place(x=centerx, y=inningLabely, anchor='n')

        # Inning Input
        self.inningIn = Entry(master, width=5)
        self.inningIn.bind('<Return>', self.submitinning)
        self.inningIn.place_forget()

        self.inInning = Label(master, text='+', width=2)
        self.inInning.bind('<Button-1>', self.increaseInning)
        self.inInning.place(x=centerx + 1, y=inInningy, anchor='ne')

        self.bottomLCanW = 16
        self.bottomLCanH = 16

        self.upCtrlArrow = [self.bottomLCanW / 2, 3, self.bottomLCanW - 3, self.bottomLCanH - 3, 0 + 3,
                            self.bottomLCanH - 3]
        self.downCtrlArrow = [3, 3, self.bottomLCanW - 3, 3, self.bottomLCanW / 2, self.bottomLCanH - 3]

        self.topBottomL = Canvas(master, width=self.bottomLCanW, height=self.bottomLCanH, highlightthickness=0,
                                 bg="#000000")
        self.topBottomL.bind('<Button-1>', self.changeTopBottom)
        self.topBottomL.place(x=centerx + 7, y=inInningy + 5, anchor='nw')


        if topBottom == 'top':
            self.topBottomL.create_polygon(self.upCtrlArrow, outline="#ffffff", width=3, tags='ctrlArrow', fill='#ffffff')
        else:
            self.topBottomL.create_polygon(self.downCtrlArrow, outline="#ffffff", width = 3, tags = 'ctrlArrow', fill = '#ffffff')
        self.baseCtrlCanvas = Canvas(master)
        self.baseCtrlCanvas.config(width=baseCtrlWidth, height=baseCtrlHeight, highlightthickness=0, bg='#000000')

        self.baseCtrlCanvas.place(x=centerx, y=baseCtrlCanvy, anchor='c')
        self.baseCtrlCanvas.create_polygon(firstCtrlPts, outline='#ffffff', width=1, tags=('firstCtrlBase'))
        self.baseCtrlCanvas.create_polygon(secondCtrlPts, outline='#ffffff', width=1, tags=('secondCtrlBase'))
        self.baseCtrlCanvas.create_polygon(thirdCtrlPts, outline='#ffffff', width=1, tags=('thirdCtrlBase'))

        if firstActive == 'true':
            self.baseCtrlCanvas.itemconfigure('firstCtrlBase', fill=yellowColor, outline='#000000')
        if secondActive == 'true':
            self.baseCtrlCanvas.itemconfigure('secondCtrlBase', fill=yellowColor, outline='#000000')
        if thirdActive == 'true':
            self.baseCtrlCanvas.itemconfigure('thirdCtrlBase', fill = yellowColor, outline='#000000')

        self.baseCtrlCanvas.tag_bind('firstCtrlBase', '<Button-1>', self.activateFirst)
        self.baseCtrlCanvas.tag_bind('secondCtrlBase', '<Button-1>', self.activateSecond)
        self.baseCtrlCanvas.tag_bind('thirdCtrlBase', '<Button-1>', self.activateThird)

        self.submitBaseL = Label(master, text='SAVE', width=10)
        self.submitBaseL.bind('<Button-1>', self.submitBases)
        self.submitBaseL.place(x=centerx, y=subBasey, anchor='n')

        self.clearL = Label(master, text='Reset Count', width=10)
        self.clearL.bind('<Button-1>', self.resetCount)
        self.clearL.place(x=centerx, y=clearCounty, anchor='c')

        self.countL = Label(master, text=str(balls) + '-' + str(strikes), width=10)
        self.countL.bind('<Button-1>', self.changeCount)
        self.countL.place(x=centerx, y=countLy, anchor='c')

        self.ballIn = Entry(master, width=4)
        self.ballIn.bind('<Return>', self.submitCount)
        self.ballIn.place(x=centerx - 6, y=countLy, anchor='e')
        self.ballIn.place_forget()

        self.strikeIn = Entry(master, width=5)
        self.strikeIn.bind('<Return>', self.submitCount)
        self.strikeIn.place(x=centerx - 3, y=countLy, anchor='w')
        self.strikeIn.place_forget()

        self.ballL = Label(master, text='BALL', width=4)
        self.ballL.bind('<Button-1>', self.addBall)
        self.ballL.place(x=centerx - 6, y=ballStrikey, anchor='e')

        self.strikeL = Label(master, text='STRIKE', width=5)
        self.strikeL.bind('<Button-1>', self.addStrike)
        self.strikeL.place(x=centerx - 3, y=ballStrikey, anchor='w')

        self.outL = Label(master, text='OUT', width=10)
        self.outL.bind('<Button-1>', self.addOut)
        self.outL.place(x=centerx, y=outy, anchor='c')

        self.outStaticL = Label(master, text=str(outs) + ' ' + outOuts, width=10)
        self.outStaticL.bind('<Button-1>', self.outInput)
        self.outStaticL.place(x=centerx, y=outStaticy, anchor='c')

        self.outIn = Entry(master, width=10)
        self.outIn.bind('<Return>', self.outInSub)
        self.outIn.place_forget()

        # color changing
        self.setHPrimary = Label(master, text="Set Home Primary Color", width=20)
        self.setHPrimary.bind('<Button-1>', self.changeHPrimary)
        self.setHPrimary.place(x=hcolorx, y=priColory, anchor='w')

        self.setAPrimary = Label(master, text="Set Away Primary Color", width=20)
        self.setAPrimary.bind('<Button-1>', self.changeAPrimary)
        self.setAPrimary.place(x=acolorx, y=priColory, anchor='e')

        self.hPriIn = Entry(master, width=18)
        self.hPriIn.bind('<Return>', self.subHP)
        self.hPriIn.place_forget()

        self.aPriIn = Entry(master, width=18)
        self.aPriIn.bind('<Return>', self.subAP)
        self.aPriIn.place_forget()

        self.openConfigLabel = Label(master, text='Open Configuration', width=20)
        self.openConfigLabel.bind('<Button-1>', self.openConfig)
        self.openConfigLabel.place(x=openconfigx, y=configy, anchor='w')

        self.saveConfiglabel = Label(master, text='Save Configuration', width=20)
        self.saveConfiglabel.bind('<Button-1>', self.saveConfig)
        self.saveConfiglabel.place(x=saveconfigx, y=configy, anchor='e')

        Receive(s, self).start()
    def send(self, arg, value=None, value2=None):
        data1 = '~'+ arg + '`'
        if value != None:
            data1 += str(value) + '`'
        if value2 != None:
            for data in value2:
                data1 += str(data) + '`'
        self.s.send(data1.encode())


def start(data, s):
    global homeTeam, awayTeam, homeScore, awayScore, inning, topBottom, outs, outOuts, balls, strikes, firstActive, \
        secondActive, thirdActive, homePrimaryColor, awayPrimaryColor, yellowColor, greyColor

    homeTeam = str(data[1])
    awayTeam = str(data[2])
    homeScore = int(data[3])
    awayScore = int(data[4])
    inning = int(data[5])
    topBottom = str(data[6])
    outs = int(data[7])
    outOuts = str(data[8])
    balls = int(data[9])
    strikes = int(data[10])

    firstActive = str(data[11])
    secondActive = str(data[12])
    thirdActive = str(data[13])
    homePrimaryColor = str(data[14])
    awayPrimaryColor = str(data[15])

    yellowColor = '#dbcf30'
    greyColor = '#737373'

    baseballCtrl = Tk()
    baseballCtrl.configure(bg='#000000')
    baseballCtrl.title("Scorecast Basketball Scoreboard Controller")
    baseballCtrl.geometry(str(windowWidth) + 'x' + str(windowHeight))
    app = CtrlApp(baseballCtrl, s, data).start()

    baseballCtrl.mainloop()
