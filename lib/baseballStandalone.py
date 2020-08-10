from tkinter import *
import easygui
import xml.etree.ElementTree as ET
from lib import baseballHost

windowWidth = 550
windowHeight = 510

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
porty = configy+25

windowHeight = porty + 20

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


fFont = "Lucida Grande"
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
    homeTeambballoverlay.configure(text=homeTeam)
    homeTeambballoverlay.update()
    homeTeambballoverlay.update()


def saveAwayTeam(event):
    global awayTeam
    awayTeam = str(awayInput.get())
    awayInput.place_forget()
    awayLabel.configure(text=awayTeam)
    awayLabel.place(x=awayLabelx, y=teamLabely, anchor='ne')
    awayTeambballoverlay.configure(text=awayTeam)
    awayTeambballoverlay.update()
    awayTeambballoverlay.update()


def editHomeScore(event):
    homeScoreL.place_forget()
    hEditScore.place(x=homeScoreLx, y=teamScoreLy, anchor='w')


def editAwayScore(event):
    awayScoreL.place_forget()
    aEditScore.place(x=awayScoreLx, y=teamScoreLy, anchor='e')


def homeScoreOverride(event):
    global homeScore
    homeScore = int(hEditScore.get())
    homeScoreFileUpdate()
    hEditScore.place_forget()
    homeScoreL.place(x=homeScoreLx, y=teamScoreLy, anchor='w')


def awayScoreOverride(event):
    global awayScore
    awayScore = int(aEditScore.get())
    awayScoreFileUpdate()
    aEditScore.place_forget()
    awayScoreL.place(x=awayScoreLx, y=teamScoreLy, anchor='e')


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


def hScore4(event):
    global homeScore
    homeScore += 4
    homeScoreFileUpdate()


def aScore4(event):
    global awayScore
    awayScore += 4
    awayScoreFileUpdate()


def changeinning(event):
    inningLabel.place_forget()
    inningIn.place(x=centerx, y=teamScoreLy, anchor='n')


def increaseInning(event):
    global inning, topBottom
    inning += 1
    topBottom = 'top'
    updateInning()


def changeTopBottom(event):
    global topBottom, inning
    if topBottom == 'top':
        topBottom = 'bottom'
    elif topBottom == 'bottom':
        inning += 1
        topBottom = 'top'
    updateInning()


def updateInning():
    global inning, topBottom, firstActive, secondActive, thirdActive, outs, outOuts
    inningNumberL.config(text=inning)
    inningNumberL.update()
    inningLabel.config(text=inning)
    if topBottom == 'top':
        topBottomCanvas.coords('Arrow', upArrowPoints)
        topBottomL.coords('ctrlArrow', upCtrlArrow)

    elif topBottom == 'bottom':
        topBottomCanvas.coords('Arrow', downArrowPoints)
        topBottomL.coords('ctrlArrow', downCtrlArrow)

    clearCount()
    outs = 0
    outOuts = 'Out'
    updateOuts()
    firstActive = 'false'
    secondActive = 'false'
    thirdActive = 'false'
    updateBases()


def safeUpdateInning():
    global inning, topBottom, firstActive, secondActive, thirdActive
    inningNumberL.config(text=inning)
    inningNumberL.update()
    inningLabel.config(text=inning)
    if topBottom == 'top':
        topBottomCanvas.coords('Arrow', upArrowPoints)
        topBottomL.coords('ctrlArrow', upCtrlArrow)

    elif topBottom == 'bottom':
        topBottomCanvas.coords('Arrow', downArrowPoints)
        topBottomL.coords('ctrlArrow', downCtrlArrow)


def submitinning(event):
    global inning
    inningIn.place_forget()
    inningLabel.place(x=centerx, y=teamScoreLy, anchor='n')
    inning = int(inningIn.get())
    inningLabel.configure(text=str(inning))
    inningNumberL.configure(text=str(inning))
    inningNumberL.update()


def activateFirst(event):
    global firstActive
    if (firstActive == 'true'):
        baseCtrlCanvas.itemconfig('firstCtrlBase', fill='#000000', outline='#ffffff')
        firstActive = 'false'
    elif (firstActive == 'false'):
        baseCtrlCanvas.itemconfig('firstCtrlBase', fill=yellowColor, outline=yellowColor)
        firstActive = 'true'


def activateSecond(event):
    global secondActive
    if (secondActive == 'true'):
        baseCtrlCanvas.itemconfig('secondCtrlBase', fill='#000000', outline='#ffffff')
        secondActive = 'false'
    elif (secondActive == 'false'):
        baseCtrlCanvas.itemconfig('secondCtrlBase', fill=yellowColor, outline=yellowColor)
        secondActive = 'true'


def activateThird(event):
    global thirdActive
    if (thirdActive == 'true'):
        baseCtrlCanvas.itemconfig('thirdCtrlBase', fill='#000000', outline='#ffffff')
        thirdActive = 'false'
    elif (thirdActive == 'false'):
        baseCtrlCanvas.itemconfig('thirdCtrlBase', fill=yellowColor, outline=yellowColor)
        thirdActive = 'true'


def submitBases(event):
    updateBases()


def updateBases():
    if (firstActive == 'true'):
        baseCtrlCanvas.itemconfig('firstCtrlBase', fill=yellowColor, outline=yellowColor)
        baseGraphicCanvas.itemconfig('firstBase', fill=yellowColor, outline=yellowColor)
    elif (firstActive == 'false'):
        baseCtrlCanvas.itemconfig('firstCtrlBase', fill='#000000', outline='#ffffff')
        baseGraphicCanvas.itemconfig('firstBase', fill='#000000', outline=greyColor)
    if (secondActive == 'true'):
        baseCtrlCanvas.itemconfig('secondCtrlBase', fill=yellowColor, outline=yellowColor)
        baseGraphicCanvas.itemconfig('secondBase', fill=yellowColor, outline=yellowColor)
    elif (secondActive == 'false'):
        baseCtrlCanvas.itemconfig('secondCtrlBase', fill='#000000', outline='#ffffff')
        baseGraphicCanvas.itemconfig('secondBase', fill='#000000', outline=greyColor)
    if (thirdActive == 'true'):
        baseCtrlCanvas.itemconfig('thirdCtrlBase', fill=yellowColor, outline=yellowColor)
        baseGraphicCanvas.itemconfig('thirdBase', fill=yellowColor, outline=yellowColor)
    elif (thirdActive == 'false'):
        baseCtrlCanvas.itemconfig('thirdCtrlBase', fill='#000000', outline='#ffffff')
        baseGraphicCanvas.itemconfig('thirdBase', fill='#000000', outline=greyColor)


def changeCount(event):
    global ballIn, strikeIn, countL
    countL.place_forget()
    ballIn.place(x=centerx - 6, y=countLy, anchor='e')
    strikeIn.place(x=centerx - 3, y=countLy, anchor='w')


def submitCount(event):
    global ballIn, strikeIn, countL, strikes, balls
    if (ballIn.get() != ''):
        balls = int(ballIn.get())
    if (strikeIn.get() != ''):
        strikes = int(strikeIn.get())
    ballIn.place_forget()
    strikeIn.place_forget()
    updateCount()
    countL.place(x=centerx, y=countLy, anchor='c')


def addBall(event):
    global balls, firstActive, secondActive, thirdActive, homeScore, awayScore
    if (balls == 3):
        clearCount()
        if (firstActive == 'false'):
            firstActive = 'true'
        elif (secondActive == 'false'):
            secondActive = 'true'
        elif (thirdActive == 'false'):
            thirdActive = 'true'
        else:
            if (topBottom == 'top'):
                homeScore += 1
            elif (topBottom == 'bottom'):
                awayScore += 1
            homeScoreFileUpdate()
        updateBases()
    else:
        balls += 1
    updateCount()


def addStrike(event):
    global strikes, balls, outs
    if (strikes == 2):
        clearCount()
        outs += 1
        updateOuts()
    else:
        strikes += 1
    updateCount()


def clearCount():
    global balls, strikes
    balls = 0
    strikes = 0
    updateCount()

def resetCount(event):
    clearCount()

def addOut(event):
    global outs

    outs += 1
    clearCount()
    updateOuts()


def outInput(event):
    global outStaticL, outIn
    outStaticL.place_forget()
    outIn.place(x=centerx, y=outStaticy, anchor='c')


def outInSub(event):
    global outs, outStaticL, outIn
    outs = int(outIn.get())
    outIn.place_forget()
    outStaticL.place(x=centerx, y=outStaticy, anchor='c')
    updateOuts()


def updateOuts():
    global topBottom, outs, inning, outStaticL, outOuts
    if (outs >= 3):
        if (topBottom == 'top'):
            topBottom = 'bottom'
        elif (topBottom == 'bottom'):
            topBottom = 'top'
            inning += 1
        updateInning()
        outs = 0
    if (outs == 2):
        outOuts = 'Outs'
    else:
        outOuts = 'Out'
    outOverlay.config(text=str(outs))
    outOverlay.update()
    outStaticOverlay.config(text=outOuts)
    outStaticOverlay.update()
    outStaticL.config(text=str(outs) + ' ' + outOuts)


def updateCount():
    global countL, balls, strikes
    countL.config(text=str(balls) + '-' + str(strikes))
    countOverlay.config(text=str(balls) + '-' + str(strikes))
    countOverlay.update()


def changeHPrimary(event):
    setHPrimary.place_forget()
    hPriIn.place(x=hcolorx, y=priColory, anchor='w')


def changeAPrimary(event):
    setAPrimary.place_forget()
    aPriIn.place(x=acolorx, y=priColory, anchor='e')


def subHP(event):
    global homePrimaryColor

    homePrimaryColor = str(hPriIn.get())
    homeFrame.configure(bg=homePrimaryColor)
    homeTeambballoverlay.configure(bg=homePrimaryColor)
    homeScoreFrame.configure(bg=homePrimaryColor)
    homeScorebballoverlay.configure(bg=homePrimaryColor)
    hPriIn.place_forget()
    setHPrimary.place(x=hcolorx, y=priColory, anchor='w')


def subAP(event):
    global awayPrimaryColor

    awayPrimaryColor = str(aPriIn.get())
    awayFrame.configure(bg=awayPrimaryColor)
    awayScoreFrame.configure(bg=awayPrimaryColor)
    awayTeambballoverlay.configure(bg=awayPrimaryColor)
    awayScorebballoverlay.configure(bg=awayPrimaryColor)
    aPriIn.place_forget()
    setAPrimary.place(x=acolorx, y=priColory, anchor='e')


def updateTeamNames():
    homeLabel.configure(text=homeTeam)
    homeTeambballoverlay.configure(text=homeTeam)
    homeTeambballoverlay.update()
    awayLabel.configure(text=awayTeam)
    awayTeambballoverlay.configure(text=awayTeam)
    awayTeambballoverlay.update()


def updateColors():
    homeFrame.configure(bg=homePrimaryColor)
    homeTeambballoverlay.configure(bg=homePrimaryColor)
    homeScoreFrame.configure(bg=homePrimaryColor)
    homeScorebballoverlay.configure(bg=homePrimaryColor)
    awayFrame.configure(bg=awayPrimaryColor)
    awayTeambballoverlay.configure(bg=awayPrimaryColor)
    awayScoreFrame.configure(bg=awayPrimaryColor)
    awayScorebballoverlay.configure(bg=awayPrimaryColor)


def updateLabels():
    updateTeamNames()
    homeScoreFileUpdate()
    awayScoreFileUpdate()
    updateCount()
    safeUpdateInning()
    updateOuts()
    updateColors()
    updateBases()


def openConfig(event):
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

        updateLabels()


def saveConfig(event):
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


def enterPort(event):
    serverLabel.place_forget()
    portSubmit.place(x=centerx+30, y=porty, anchor='w')
    portLabel.place(x=centerx-30, y=porty, anchor='e')
    portEntry.place(x=centerx-30, y=porty, anchor='w')

def submitPort(event):
    port = int(portEntry.get())
    data = []
    data.append(homeTeam)
    data.append(awayTeam)
    data.append(homeScore)
    data.append(awayScore)
    data.append(inning)
    data.append(topBottom)
    data.append(outs)
    data.append(outOuts)
    data.append(balls)
    data.append(strikes)
    data.append(firstActive)
    data.append(secondActive)
    data.append(thirdActive)
    data.append(homePrimaryColor)
    data.append(awayPrimaryColor)

    bballoverlay.destroy()
    basketballCtrl.destroy()
    baseballHost.start(port, data)


def start():
    global homeLabel, homeTeam, awayLabel, awayTeam, homeSave, awaySave, homeInput, awayInput, homeScoreL, awayScoreL, \
        homeScore, awayScore, homeScore1, homeScore2, homeScore3, awayScore1, awayScore2, awayScore3, hEditScore, \
        aEditScore, awayEditScoreSave, homeEditScoreSave, inning, inningLabel, inningIn, homePoss, awayPoss, \
        homeTeambballoverlay, awayTeambballoverlay, homeScorebballoverlay, awayScorebballoverlay, inningbballoverlay, \
        setHPrimary, setAPrimary, hPriIn, aPriIn, homePrimaryColor, awayPrimaryColor, homeFrame, awayFrame, \
        homeScoreFrame, awayScoreFrame, topBottom, outs, balls, strikes, firstBasePoints, secondBasePoints, \
        thirdBasePoints, downArrowPoints, upArrowPoints, infoFrame, topBottomCanvas, inningNumberL, outStaticOverlay, \
        coundOverlay, baseGraphicCanvas, topBottomArrow, firstBasePoly, secondBasePoly, thirdBasePoly, yellowColor, \
        upCtrlArrow, downCtrlArrow, topBottomL, baseCtrlCanvas, firstActive, secondActive, thirdActive, outOverlay, \
        countL, countOverlay, outStaticL, outOuts, outIn, ballIn, strikeIn, serverLabel, portSubmit, portLabel, \
        portEntry, basketballCtrl, bballoverlay, greyColor

    basketballCtrl = Tk()
    basketballCtrl.configure(bg='#000000')
    basketballCtrl.title("Scorecast Baseball Scoreboard Controller")
    basketballCtrl.geometry(str(windowWidth) + 'x' + str(windowHeight))
    bballoverlay = Tk()
    bballoverlay.configure(bg='#00ff00')
    bballoverlay.geometry('290x110')
    bballoverlay.title('Scorecast Baseball Scoreboard')

    # default variables
    homeTeam = 'HOME'
    awayTeam = 'VISITOR'
    homeScore = 0
    awayScore = 0
    inning = 1
    topBottom = 'top'
    outs = 0
    outOuts = 'Out'
    balls = 0
    strikes = 0

    firstActive = 'false'
    secondActive = 'false'
    thirdActive = 'false'
    awayPrimaryColor = '#110b5d'
    homePrimaryColor = '#c1a551'

    yellowColor = '#dbcf30'
    greyColor = '#737373'

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
    homeScoreL.place(x=homeScoreLx, y=teamScoreLy, anchor='w')
    awayScoreL = Label(basketballCtrl, text=00, width=20, height=7)
    awayScoreL.bind("<Button-1>", editAwayScore)
    awayScoreL.place(x=awayScoreLx, y=teamScoreLy, anchor='e')

    # Edit Scores
    hEditScore = Entry(basketballCtrl, width=19)
    hEditScore.bind('<Return>', homeScoreOverride)
    hEditScore.place_forget()
    aEditScore = Entry(basketballCtrl, width=19)
    aEditScore.bind('<Return>', awayScoreOverride)
    aEditScore.place_forget()

    # Increase Score Buttons
    homeScore1 = Label(basketballCtrl, text='+1', width=addScoreWidth)
    homeScore1.bind("<Button-1>", hScore1)
    homeScore1.place(x=hscore1x, y=scorey, anchor='nw')
    homeScore2 = Label(basketballCtrl, text='+2', width=addScoreWidth)
    homeScore2.bind("<Button-1>", hScore2)
    homeScore2.place(x=hscore2x, y=scorey, anchor='nw')
    homeScore3 = Label(basketballCtrl, text='+3', width=addScoreWidth)
    homeScore3.bind("<Button-1>", hScore3)
    homeScore3.place(x=hscore3x, y=scorey, anchor='nw')
    homeScore4 = Label(basketballCtrl, text='+4', width=addScoreWidth)
    homeScore4.bind('<Button-1>', hScore4)
    homeScore4.place(x=hscore4x, y=scorey, anchor='nw')

    awayScore1 = Label(basketballCtrl, text='+1', width=addScoreWidth)
    awayScore1.bind("<Button-1>", aScore1)
    awayScore1.place(x=ascore1x, y=scorey, anchor='ne')
    awayScore2 = Label(basketballCtrl, text='+2', width=addScoreWidth)
    awayScore2.bind("<Button-1>", aScore2)
    awayScore2.place(x=ascore2x, y=scorey, anchor='ne')
    awayScore3 = Label(basketballCtrl, text='+3', width=addScoreWidth)
    awayScore3.bind("<Button-1>", aScore3)
    awayScore3.place(x=ascore3x, y=scorey, anchor='ne')
    awayScore4 = Label(basketballCtrl, text='+4', width=addScoreWidth)
    awayScore4.bind('<Button-1>', aScore4)
    awayScore4.place(x=ascore4x, y=scorey, anchor='ne')

    # Inning Buttons

    inningStatic = Label(basketballCtrl, text='Inning', width=5, bg='#000000', fg='#ffffff')
    inningStatic.place(x=centerx, y=inningLabely - 5, anchor='s')

    inningLabel = Label(basketballCtrl, text=inning, width=5)
    inningLabel.bind('<Button-1>', changeinning)
    inningLabel.place(x=centerx, y=inningLabely, anchor='n')

    # Inning Input
    inningIn = Entry(basketballCtrl, width=5)
    inningIn.bind('<Return>', submitinning)
    inningIn.place_forget()

    inInning = Label(basketballCtrl, text='+', width=2)
    inInning.bind('<Button-1>', increaseInning)
    inInning.place(x=centerx + 1, y=inInningy, anchor='ne')

    bottomLCanW = 16
    bottomLCanH = 16

    upCtrlArrow = [bottomLCanW / 2, 3, bottomLCanW - 3, bottomLCanH - 3, 0 + 3, bottomLCanH - 3]
    downCtrlArrow = [3, 3, bottomLCanW - 3, 3, bottomLCanW / 2, bottomLCanH - 3]

    topBottomL = Canvas(basketballCtrl, width=bottomLCanW, height=bottomLCanH, highlightthickness=0, bg="#000000")
    topBottomL.bind('<Button-1>', changeTopBottom)
    topBottomL.place(x=centerx + 7, y=inInningy + 5, anchor='nw')

    topBottomL.create_polygon(upCtrlArrow, outline="#ffffff", width=3, tags='ctrlArrow', fill='#ffffff')

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
                     secondCtrly - ctrlBaseSize, secondCtrlx, secondCtrly, secondCtrlx - ctrlBaseSize,
                     secondCtrly - ctrlBaseSize]
    thirdCtrlPts = [thirdCtrlx - ctrlBaseSize, thirdCtrly - ctrlBaseSize, thirdCtrlx, thirdCtrly,
                    thirdCtrlx - ctrlBaseSize,
                    thirdCtrly + ctrlBaseSize, thirdCtrlx - ctrlBaseSize - ctrlBaseSize, thirdCtrly]

    baseCtrlCanvas = Canvas(basketballCtrl)
    baseCtrlCanvas.config(width=baseCtrlWidth, height=baseCtrlHeight, highlightthickness=0, bg='#000000')

    baseCtrlCanvas.place(x=centerx, y=baseCtrlCanvy, anchor='c')
    baseCtrlCanvas.create_polygon(firstCtrlPts, outline='#ffffff', width=1, tags=('firstCtrlBase'))
    baseCtrlCanvas.create_polygon(secondCtrlPts, outline='#ffffff', width=1, tags=('secondCtrlBase'))
    baseCtrlCanvas.create_polygon(thirdCtrlPts, outline='#ffffff', width=1, tags=('thirdCtrlBase'))
    baseCtrlCanvas.tag_bind('firstCtrlBase', '<Button-1>', activateFirst)
    baseCtrlCanvas.tag_bind('secondCtrlBase', '<Button-1>', activateSecond)
    baseCtrlCanvas.tag_bind('thirdCtrlBase', '<Button-1>', activateThird)

    submitBaseL = Label(basketballCtrl, text='SAVE', width=10)
    submitBaseL.bind('<Button-1>', submitBases)
    submitBaseL.place(x=centerx, y=subBasey, anchor='n')

    clearL = Label(basketballCtrl, text='Reset Count', width=10)
    clearL.bind('<Button-1>', resetCount)
    clearL.place(x=centerx, y=clearCounty, anchor='c')

    countL = Label(basketballCtrl, text=str(balls) + '-' + str(strikes), width=10)
    countL.bind('<Button-1>', changeCount)
    countL.place(x=centerx, y=countLy, anchor='c')

    ballIn = Entry(basketballCtrl, width=4)
    ballIn.bind('<Return>', submitCount)
    ballIn.place(x=centerx - 6, y=countLy, anchor='e')
    ballIn.place_forget()

    strikeIn = Entry(basketballCtrl, width=5)
    strikeIn.bind('<Return>', submitCount)
    strikeIn.place(x=centerx - 3, y=countLy, anchor='w')
    strikeIn.place_forget()

    ballL = Label(basketballCtrl, text='BALL', width=4)
    ballL.bind('<Button-1>', addBall)
    ballL.place(x=centerx - 6, y=ballStrikey, anchor='e')

    strikeL = Label(basketballCtrl, text='STRIKE', width=5)
    strikeL.bind('<Button-1>', addStrike)
    strikeL.place(x=centerx - 3, y=ballStrikey, anchor='w')

    outL = Label(basketballCtrl, text='OUT', width=10)
    outL.bind('<Button-1>', addOut)
    outL.place(x=centerx, y=outy, anchor='c')

    outStaticL = Label(basketballCtrl, text=str(outs) + ' ' + outOuts, width=10)
    outStaticL.bind('<Button-1>', outInput)
    outStaticL.place(x=centerx, y=outStaticy, anchor='c')

    outIn = Entry(basketballCtrl, width=10)
    outIn.bind('<Return>', outInSub)
    outIn.place_forget()

    # color changing
    setHPrimary = Label(basketballCtrl, text="Set Home Primary Color", width=20)
    setHPrimary.bind('<Button-1>', changeHPrimary)
    setHPrimary.place(x=hcolorx, y=priColory, anchor='w')

    setAPrimary = Label(basketballCtrl, text="Set Away Primary Color", width=20)
    setAPrimary.bind('<Button-1>', changeAPrimary)
    setAPrimary.place(x=acolorx, y=priColory, anchor='e')

    hPriIn = Entry(basketballCtrl, width=18)
    hPriIn.bind('<Return>', subHP)
    hPriIn.place_forget()

    aPriIn = Entry(basketballCtrl, width=18)
    aPriIn.bind('<Return>', subAP)
    aPriIn.place_forget()

    openConfigLabel = Label(basketballCtrl, text='Open Configuration', width=20)
    openConfigLabel.bind('<Button-1>', openConfig)
    openConfigLabel.place(x=openconfigx, y=configy, anchor='w')

    saveConfiglabel = Label(basketballCtrl, text='Save Configuration', width=20)
    saveConfiglabel.bind('<Button-1>', saveConfig)
    saveConfiglabel.place(x=saveconfigx, y=configy, anchor='e')

    # server
    serverLabel = Label(basketballCtrl, text='Server Config', width=10)
    serverLabel.bind("<Button-1>", enterPort)
    serverLabel.place(x=centerx, y=porty, anchor='c')

    portSubmit = Label(basketballCtrl, text='Submit')
    portSubmit.bind("<Button-1>", submitPort)
    portSubmit.place_forget()

    portEntry = Entry(basketballCtrl, width=4)
    portEntry.bind("<Return>", submitPort)
    portEntry.place_forget()

    portLabel = Label(basketballCtrl, bg='#000000', text='Port: ', fg='#ffffff')
    portLabel.place_forget()

    # baseball overlay

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
    secondBasePoints = [secondx, secondy - baseSize - baseSize, secondx + baseSize, secondy - baseSize, secondx,
                        secondy, secondx - baseSize, secondy - baseSize]
    thirdBasePoints = [thirdx - baseSize, thirdy - baseSize, thirdx, thirdy, thirdx - baseSize, thirdy + baseSize,
                       thirdx - baseSize - baseSize, thirdy]

    downArrowPoints = [0, 0, topBottomCanvasWidth, 0, topBottomCanvasWidth / 2, topBottomCanvasHeight]
    upArrowPoints = [topBottomCanvasWidth / 2, 0, topBottomCanvasWidth, topBottomCanvasHeight, 0, topBottomCanvasHeight]

    homeFrame = Frame(bballoverlay)
    homeFrame.configure(bg=homePrimaryColor, width=teamNameWidth, height=teamHeight)
    homeFrame.place(x=teamx, y=homey, anchor='nw')  # 293.33

    homeTeambballoverlay = Label(homeFrame, text=homeTeam)
    homeTeambballoverlay.place(x=5, y=teamHeight / 2, anchor='w')
    homeTeambballoverlay['bg'] = homeTeambballoverlay.master['bg']
    homeTeambballoverlay.config(font=(fFont, 18), fg='#ffffff')

    homeScoreFrame = Frame(bballoverlay)
    homeScoreFrame.configure(bg=homePrimaryColor, width=scoreFrameWidth, height=teamHeight)
    homeScoreFrame.place(x=scorex, y=homey, anchor='nw')

    homeScorebballoverlay = Label(homeScoreFrame, text=homeScore)
    homeScorebballoverlay.place(x=scoreFrameWidth / 2, y=teamHeight / 2, anchor='c')
    homeScorebballoverlay['bg'] = homeScorebballoverlay.master['bg']
    homeScorebballoverlay.config(font=(fFont, 23), fg='#ffffff')

    awayFrame = Frame(bballoverlay)
    awayFrame.configure(bg=awayPrimaryColor, width=teamNameWidth, height=teamHeight)
    awayFrame.place(x=teamx, y=awayy, anchor='nw')

    awayTeambballoverlay = Label(awayFrame, text=awayTeam)
    awayTeambballoverlay.place(x=5, y=teamHeight / 2, anchor='w')
    awayTeambballoverlay['bg'] = awayTeambballoverlay.master['bg']
    awayTeambballoverlay.config(font=(fFont, 18), fg='#ffffff')

    awayScoreFrame = Frame(bballoverlay)
    awayScoreFrame.configure(bg=awayPrimaryColor, width=scoreFrameWidth, height=teamHeight)
    awayScoreFrame.place(x=scorex, y=awayy, anchor='nw')

    awayScorebballoverlay = Label(awayScoreFrame, text=awayScore)
    awayScorebballoverlay.place(x=scoreFrameWidth / 2, y=teamHeight / 2, anchor='c')
    awayScorebballoverlay['bg'] = awayScorebballoverlay.master['bg']
    awayScorebballoverlay.config(font=(fFont, 23), fg='#ffffff')

    infoFrame = Frame(bballoverlay)
    infoFrame.configure(bg='#000000', width=infoFrameWidth, height=infoFrameHeight)
    infoFrame.place(x=teamx, y=infoFramey, anchor='nw')

    topBottomCanvas = Canvas(infoFrame)
    topBottomCanvas.config(bg="#000000", width=topBottomCanvasWidth, height=topBottomCanvasHeight, bd=0,
                           highlightthickness=0)
    topBottomCanvas.place(x=topBottomx, y=infoFrameHeight / 2, anchor='c')

    topBottomArrow = topBottomCanvas.create_polygon(upArrowPoints, fill=greyColor, tags='Arrow')

    inningNumberL = Label(infoFrame, text=str(inning))
    inningNumberL.place(x=inningx, y=infoFrameHeight / 2, anchor='w')
    inningNumberL['bg'] = inningNumberL.master['bg']
    inningNumberL.config(font=(fFont, 15), fg='#ffffff')

    outOverlay = Label(infoFrame, text=outs, width=outWidth)
    outOverlay.place(x=outx, y=(infoFrameHeight / 2), anchor='c')
    outOverlay['bg'] = outOverlay.master['bg']
    outOverlay.config(font=(fFont, 15), fg='#ffffff')

    outStaticOverlay = Label(infoFrame, text=outOuts)
    outStaticOverlay.place(x=outSx, y=infoFrameHeight / 2, anchor='w')
    outStaticOverlay['bg'] = outStaticOverlay.master['bg']
    outStaticOverlay.config(font=(fFont, 14), fg=greyColor)

    countOverlay = Label(infoFrame, text=str(balls) + '-' + str(strikes))
    countOverlay.place(x=countx, y=infoFrameHeight / 2, anchor='c')
    countOverlay['bg'] = countOverlay.master['bg']
    countOverlay.config(font=(fFont, 16), fg='#ffffff')

    baseGraphicCanvas = Canvas(bballoverlay)
    baseGraphicCanvas.config(bg="#000000", width=baseGraphicWidth, height=baseGraphicHeight,
                             borderwidth=0, highlightthickness=0)
    baseGraphicCanvas.place(x=baseGraphicFramex, y=homey, anchor='nw')

    firstBasePoly = baseGraphicCanvas.create_polygon(firstBasePoints, outline=greyColor, width=1, tags='firstBase')
    secondBasePoly = baseGraphicCanvas.create_polygon(secondBasePoints, outline=greyColor, width=1, tags='secondBase')
    thirdBasePoly = baseGraphicCanvas.create_polygon(thirdBasePoints, outline=greyColor, width=1, tags='thirdBase')
