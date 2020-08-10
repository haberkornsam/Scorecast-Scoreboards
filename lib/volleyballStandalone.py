from tkinter import *
import math
import easygui
import xml.etree.ElementTree as ET
from lib import volleyballHost


# control values

ctrlWidth = 600

centerx = ctrlWidth/2
homeTeamLx = 10
awayTeamLx =ctrlWidth-homeTeamLx
homeScoreLx = 10
awayScoreLx = ctrlWidth-homeScoreLx
matchScoreLy = 40
teamEditScorey = 145
hscore1x = 10
hscore2x = 98
ascore1x = ctrlWidth - hscore2x
ascore2x = ctrlWidth - hscore1x
scorey = 165

serveY = 25
hServeX = 187
aServeX = ctrlWidth-hServeX

hTOx = 220
aTOx = ctrlWidth-hTOx
TOy = 205

hTakeTOx = 180
aTakeTOx=ctrlWidth-hTakeTOx
takeTOy = TOy

staticMatchX = 300
foulLaby = 95
hFoulLx = 186
FoulLy = 120
aFoulLx = ctrlWidth - hFoulLx
homeFoulAddX = 245
awayFoulAddX =ctrlWidth-homeFoulAddX
foulAdy = 165
hcolorx = 10
acolorx = ctrlWidth - hcolorx
priColory = 200
secColory = priColory+25
servery = 350


fFont = "Lucida Grande"





def editHomeScore(event):
    homeScoreL.place_forget()
    hEditScore.place(x=homeScoreLx, y=teamEditScorey, anchor='nw')


def editAwayScore(event):
    awayScoreL.place_forget()
    aEditScore.place(x=awayScoreLx, y=teamEditScorey, anchor='ne')


def homeScoreOverride(event):
    global homeScore
    if (int(hEditScore.get())<0):
        return
    homeScore = int(hEditScore.get())
    homeScoreFileUpdate()
    hEditScore.place_forget()
    homeScoreL.place(x=homeScoreLx, y=matchScoreLy, anchor='nw')


def awayScoreOverride(event):
    global awayScore
    if(int(aEditScore.get())<0):
        return
    awayScore = int(aEditScore.get())
    awayScoreFileUpdate()
    aEditScore.place_forget()
    awayScoreL.place(x=awayScoreLx, y=matchScoreLy, anchor='ne')


def homeScoreFileUpdate():
    global homeScore, awayScore
    homeScoreOver.configure(text=homeScore)
    homeScoreOver.update()
    homeScoreL.configure(text=homeScore)


def awayScoreFileUpdate():
    global homeScore, awayScore
    awayScoreOver.configure(text=awayScore)
    awayScoreOver.update()
    awayScoreL.configure(text=awayScore)




def aScore1(event):
    global homeScore, awayScore, serve
    awayScore += 1
    serve = 'Away'
    setServe()
    awayScoreFileUpdate()


def hScore2(event):
    global homeScore, awayScore, serve
    homeScore += 1
    serve = 'Home'
    setServe()
    homeScoreFileUpdate()


def hScore1(event):
    global homeScore, awayScore
    if(homeScore <=0):
        return
    homeScore -= 1
    homeScoreFileUpdate()

def aScore2(event):
    global homeScore, awayScore
    if(awayScore <= 0):
        return
    awayScore -=1
    awayScoreFileUpdate()


def setHomeServe(event):
    global serve
    if(serve == 'Home'):
        serve = 'none'
    else:
        serve = 'Home'
    setServe()

def setAwayServe(event):
    global serve
    if(serve == 'Away'):
        serve = 'none'
    else:
        serve = 'Away'
    setServe()


def setServe():
    global serve
    if(serve=='Home'):
        homeServeCtrl.config(bg='#ffffff', fg='#000000')
        awayServeCtrl.config(bg='#000000', fg='#ffffff')
        awayServeOverlay.place_forget()
        homeServeOverlay.place(x=0, y=0, anchor='nw')
    elif(serve=='Away'):
        awayServeCtrl.config(bg='#ffffff', fg='#000000')
        homeServeCtrl.config(bg='#000000', fg='#ffffff')
        awayServeOverlay.place(x=0, y=0, anchor='nw')
        homeServeOverlay.place_forget()
    else:
        homeServeCtrl.config(bg='#000000', fg='#ffffff')
        awayServeCtrl.config(bg='#000000', fg='#ffffff')
        awayServeOverlay.place_forget()
        homeServeOverlay.place_forget()



def changehTeamScore(event):
    hTeamScoreL.place_forget()
    hTeamScoreIn.place(x=hFoulLx, y=FoulLy, anchor='nw')


def changeaTeamScore(event):
    aTeamScoreL.place_forget()
    aTeamScoreIn.place(x=aFoulLx, y=FoulLy, anchor='ne')


def submithTeamScore(event):
    global hTeamScore
    if (int(hTeamScoreIn.get())<0):
        return
    hTeamScoreL.place(x=hFoulLx, y=FoulLy, anchor='nw')
    hTeamScoreIn.place_forget()
    hTeamScore = int(hTeamScoreIn.get())
    TeamScoreUpdate()


def submitaTeamScore(event):
    global aTeamScore
    if(int(aTeamScoreIn.get())<0):
        return
    aTeamScore = int(aTeamScoreIn.get())
    aTeamScoreL.place(x=aFoulLx, y=FoulLy, anchor='ne')
    aTeamScoreIn.place_forget()
    TeamScoreUpdate()


def hTeamScoreOne(event):
    global hTeamScore
    hTeamScore += 1
    TeamScoreUpdate()


def aTeamScoreOne(event):
    global aTeamScore
    aTeamScore += 1
    TeamScoreUpdate()



def TeamScoreUpdate():
    global hTeamScore, aTeamScore, matchScore, setNum, set

    if(hTeamScore==aTeamScore):
        matchScore = 'Match tied '+str(hTeamScore)+'-'+str(aTeamScore)
    elif(hTeamScore>aTeamScore):
        matchScore =homeTeam+' leads '+str(hTeamScore)+'-'+str(aTeamScore)
    elif(aTeamScore>hTeamScore):
        matchScore =awayTeam+' leads '+str(aTeamScore)+'-'+str(hTeamScore)


    set =ordinal(setNum)+' Set'
    setNumOver.config(text=set)
    setLabel.config(text=set)

    matchScoreOver.configure(text=matchScore)
    matchScoreOver.update()
    matchScoreCtrl.configure(text=matchScore)
    hTeamScoreL.configure(text=hTeamScore)
    aTeamScoreL.configure(text=aTeamScore)

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

def resetMatchScore(event): #next set btn update to 2nd set etc
    global homeScore, awayScore, hTeamScore, aTeamScore, serve, setNum, set
    if(homeScore>awayScore):
        hTeamScore+=1
    else:
        aTeamScore+=1
    homeScore = 0
    awayScore = 0
    serve = 'none'
    setNum += 1
    set =ordinal(setNum)+" Set"
    setLabel.configure(text=set)
    setNumOver.configure(text=str(set))
    setNumOver.update()
    setServe()
    TeamScoreUpdate()
    homeScoreFileUpdate()
    awayScoreFileUpdate()


def changeSet(event):
    setLabel.place_forget()
    setIn.place(x=centerx, y=10, anchor='n')


def submitHalf(event):
    global set
    setIn.place_forget()
    setLabel.place(x=centerx, y=10, anchor='n')
    set = str(setIn.get())
    setLabel.configure(text=set)
    setNumOver.configure(text=str(set))
    setNumOver.update()


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
    if(homePrimaryColor[0] != '#'):
        homePrimaryColor = '#'+homePrimaryColor
    if(len(homePrimaryColor)!=7):
        return
    try:
        homeTeamFrame.configure(bg=homePrimaryColor)
    except:
        return
    homeTeamOver.configure(bg=homePrimaryColor)
    hPriIn.place_forget()
    setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')
    updateTO()


def subHS(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    homeSecondColor = str(hSecIn.get())
    if (homeSecondColor[0]!='#'):
        homeSecondColor='#'+homeSecondColor
    if (len(homeSecondColor)!=7):
        return
    try:
        homeScoreFrame.configure(bg=homeSecondColor)
    except:
        return
    homeScoreOver.configure(bg = homeSecondColor)
    hSecIn.place_forget()
    setHSecond.place(x=hcolorx, y=secColory, anchor='nw')
    updateTO()

def subAP(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    awayPrimaryColor = str(aPriIn.get())
    if (awayPrimaryColor[0]!='#'):
        awayPrimaryColor='#'+awayPrimaryColor
    if (len(awayPrimaryColor)!=7):
        return
    try:
        awayTeamFrame.configure(bg=awayPrimaryColor)
    except:
        return
    awayTeamOver.configure(bg = awayPrimaryColor)
    aPriIn.place_forget()
    setAPrimary.place(x=acolorx, y=priColory, anchor='ne')
    updateTO()


def subAS(event):
    global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

    awaySecondColor = str(aSecIn.get())
    if (awaySecondColor[0]!='#'):
        awaySecondColor='#'+awaySecondColor
    if (len(awaySecondColor)!=7):
        return
    awayScoreFrame.configure(bg=awaySecondColor)
    awayScoreOver.configure(bg=awaySecondColor)
    aSecIn.place_forget()
    setASecond.place(x=acolorx, y=secColory, anchor='ne')
    updateTO()




def updateColors():
    homeTeamFrame.configure(bg=homePrimaryColor)
    homeTeamOver.configure(bg=homePrimaryColor)

    homeScoreFrame.config(bg=homeSecondColor)
    homeScoreOver.config(bg=homeSecondColor)

    awayTeamFrame.configure(bg=awayPrimaryColor)
    awayTeamOver.configure(bg=awayPrimaryColor)

    awayScoreFrame.configure(bg=awaySecondColor)
    awayScoreOver.configure(bg=awaySecondColor)
    updateTO()




def changeHomeAbrev(event):
    homeAbrevL.place_forget()
    homeAbrevIn.place(x=homeTeamLx, y=10, anchor='nw')


def subHomeAbrev(event):
    global homeTeam
    homeTeam = str(homeAbrevIn.get())
    homeAbrevL.config(text=homeTeam)
    homeTeamOver.config(text=homeTeam)
    homeTeamOver.update()
    homeAbrevIn.place_forget()
    homeAbrevL.place(x=homeTeamLx, y=10, anchor='nw')


def changeAwayAbrev(event):
    awayAbrevL.place_forget()
    awayAbrevIn.place(x=awayTeamLx, y=10, anchor='ne')


def subAwayAbrev(event):
    global awayTeam
    awayTeam = str(awayAbrevIn.get())
    awayAbrevL.config(text=awayTeam)
    awayTeamOver.config(text=awayTeam)
    awayTeamOver.update()
    awayAbrevIn.place_forget()
    awayAbrevL.place(x=awayTeamLx, y=10, anchor='ne')


def abrevUpdate():
    homeAbrevL.config(text=homeTeam)
    homeTeamOver.config(text=homeTeam)
    homeTeamOver.update()
    awayAbrevL.config(text=awayTeam)
    awayTeamOver.config(text=awayTeam)
    awayTeamOver.update()


def changeWeightClass(event):
    matchScoreCtrl.place_forget()
    matchScoreIn.place(x=centerx, y=70, anchor='n')


def subWeightClass(event):
    global matchScore
    matchScore = str(matchScoreIn.get())
    weightUpdate()
    matchScoreCtrl.place(x=centerx, y=70, anchor='n')
    matchScoreIn.place_forget()


def weightUpdate():
    matchScoreCtrl.config(text=matchScore)
    matchScoreOver.config(text=matchScore)
    matchScoreOver.update()

def homeResetTO(event):
    global homeTO
    homeTO=0
    updateTO()

def awayResetTO(event):
    global awayTO
    awayTO=0
    updateTO()

def homeTakeTO(event):
    global homeTO
    if(homeTO<totalTO):
        homeTO+=1
        updateTO()

def awayTakeTO(event):
    global awayTO
    if(awayTO<totalTO):
        awayTO+=1
        updateTO()

def updateTO():
    global awayTO, homeTO, homeTOFrames, awayTOFrames, totalTO

    for i in range(totalTO):
        if(i<(totalTO-homeTO)):
            homeTOFrames[i].config(bg='#ffffff')
        else:
            homeTOFrames[i]['bg'] = homeTOFrames[i].master['bg']
        if(i<(totalTO-awayTO)):
            awayTOFrames[i].config(bg='#ffffff')
        else:
            awayTOFrames[i]['bg'] = awayTOFrames[i].master['bg']

    homeTOCtrl.config(text='TO:\n'+str(totalTO-homeTO))
    awayTOCtrl.config(text='TO:\n'+str(totalTO-awayTO))




def updateLabels():
    homeScoreFileUpdate()
    awayScoreFileUpdate()
    TeamScoreUpdate()
    setServe()
    weightUpdate()
    abrevUpdate()
    updateColors()


def openConfig(event=None):
    global homeScore, awayScore, aTeamScore, hTeamScore, set, \
        homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, homeTeam, awayTeam, \
        hTeamScore, aTeamScore, matchScore, homeTO, awayTO, setNum, serve, totalTO
    try:
        tree = ET.parse(easygui.fileopenbox(filetypes=['*.xml'])).getroot()
    except:
        return
    if (tree.tag == 'volleyball'):
        homeTeam = str(tree[0][0].text)
        hTeamScore = int(tree[0][1].text)
        homeScore = int(tree[0][2].text)
        homeTO = int(tree[0][3].text)
        homePrimaryColor = str(tree[0][4].text)
        homeSecondColor = str(tree[0][5].text)

        awayTeam = str(tree[1][0].text)
        aTeamScore = int(tree[1][1].text)
        awayScore = int(tree[1][2].text)
        awayTO = int(tree[1][3].text)
        awayPrimaryColor = str(tree[1][4].text)
        awaySecondColor = str(tree[1][5].text)


        setNum = int(tree[2].text)
        set = str(tree[3].text)
        serve = str(tree[4].text)
        totalTO = int(tree[5].text)
        updateLabels()


def saveConfig(event=None):
    global homeScore, awayScore, aTeamScore, hTeamScore, set, homeTO, awayTO, totalTO, setNum, serve, \
         homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, homeTeam, awayTeam, matchScore
    wrestling1 = ET.Element('volleyball')
    homeTeam1 = ET.SubElement(wrestling1, 'home')
    hAbrev1 = ET.SubElement(homeTeam1, 'name')
    hAbrev1.text = str(homeTeam)
    hTScore1 = ET.SubElement(homeTeam1, 'matchScore')
    hTScore1.text = str(hTeamScore)
    hscore1 = ET.SubElement(homeTeam1, 'setScore')
    hscore1.text = str(homeScore)
    hscore1 = ET.SubElement(homeTeam1, 'timeoutsTaken')
    hscore1.text = str(homeTO)
    hpriColor1 = ET.SubElement(homeTeam1, 'primaryColor')
    hpriColor1.text = str(homePrimaryColor)
    hsecColor1 = ET.SubElement(homeTeam1, 'secondaryColor')
    hsecColor1.text = str(homeSecondColor)
    awayTeam1 = ET.SubElement(wrestling1, 'away')
    aAbrev1 = ET.SubElement(awayTeam1, 'name')
    aAbrev1.text = str(awayTeam)
    aTScore1 = ET.SubElement(awayTeam1, 'matchScore')
    aTScore1.text = str(aTeamScore)
    ascore1 = ET.SubElement(awayTeam1, 'setScore')
    ascore1.text = str(awayScore)
    ascore1 = ET.SubElement(awayTeam1, 'timeoutsTaken')
    ascore1.text = str(awayScore)
    apriColor1 = ET.SubElement(awayTeam1, 'primaryColor')
    apriColor1.text = str(awayPrimaryColor)
    asecColor1 = ET.SubElement(awayTeam1, 'secondaryColor')
    asecColor1.text = str(awaySecondColor)

    half1 = ET.SubElement(wrestling1, 'SetNumber')
    half1.text = str(setNum)
    set1 = ET.SubElement(wrestling1, 'Set')
    set1.text = str(set)
    weightClass1 = ET.SubElement(wrestling1, 'currentServe')
    weightClass1.text = str(serve)
    weightClass1 = ET.SubElement(wrestling1, 'totalTO')
    weightClass1.text = str(totalTO)
    myData = ET.tostring(wrestling1).decode("utf-8")

    configFile = open(str(easygui.filesavebox()) + '.xml', 'w')
    configFile.write(myData)



def submitPort(event):
    global portIn, serverSet
    try:
        port = int(portIn.get())
    except:
        return
    data = []
    data.append(homeTeam)
    data.append(awayTeam)
    data.append(hTeamScore)
    data.append(aTeamScore)
    data.append(homeScore)
    data.append(awayScore)
    data.append(homeTO)
    data.append(awayTO)
    data.append(homePrimaryColor)
    data.append(homeSecondColor)
    data.append(awayPrimaryColor)
    data.append(awaySecondColor)
    data.append(serve)
    data.append(setNum)
    data.append(set)
    data.append(totalTO)
    data.append(matchScore)

    wrestOverlay.destroy()
    volleyballCtrl.destroy()
    serverSet.destroy()
    volleyballHost.start(port, data)

def returnHome(event=None):
    volleyballCtrl.destroy()
    wrestOverlay.destroy()

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


overlayWidth = 1280
overlayHeight = 120


def start(data=None):
    global homeScoreL, awayScoreL, homeScore, awayScore, homeScore1, homeScore2, awayScore1, awayScore2, hEditScore, \
        aEditScore, hTeamScoreL, hTeamScore, aTeamScoreL, aTeamScore, hTeamScoreIn, aTeamScoreIn, set, setLabel, setIn, \
        homeTeamOver, awayTeamOver, homeScoreOver, awayScoreOver, setNumOver, \
        setHPrimary, setHSecond, setAPrimary, setASecond, hSecIn, hPriIn, aSecIn, aPriIn, homePrimaryColor, \
        homeSecondColor, awayPrimaryColor, awaySecondColor, homeTeamFrame, awayTeamFrame, homeScoreFrame, \
        awayScoreFrame, homeAbrevL, homeAbrevIn, awayAbrevIn, awayAbrevL, homeTeam, awayTeam, matchScoreIn, matchScoreCtrl, \
        matchScoreOver, serverLabel, portSubmit, portLabel, portEntry, wrestOverlay, volleyballCtrl, homeServeCtrl, \
        awayServeCtrl, serve, awayServeOverlay, homeServeOverlay, matchScore, setNum, totalTO, homeTO, awayTO, \
        homeTOFrames, awayTOFrames, homeTOCtrl, awayTOCtrl
    volleyballCtrl = Tk()
    volleyballCtrl.configure(bg='#000000')
    volleyballCtrl.title("Scorecast Volleyball Controller")
    volleyballCtrl.geometry('600x260')
    wrestOverlay = Tk()
    wrestOverlay.configure(bg='#00ff00')
    wrestOverlay.geometry('1280x120')
    wrestOverlay.geometry(str(overlayWidth)+'x'+str(overlayHeight))
    wrestOverlay.title('Scorecast Volleyball Scoreboard')

    if data == None:
    # default variables
        homeTeam ='HOME'
        awayTeam ="GUEST"

        serve = 'none'

        hTeamScore = 0
        aTeamScore = 0

        homeScore = 0
        awayScore = 0
        setNum = 1
        set ='1st Set'

        totalTO = 2

        homeTO = 0
        awayTO = 0

        homePrimaryColor = '#c1a551'
        homeSecondColor = '#877338'
        awayPrimaryColor = '#110b5d'
        awaySecondColor = '#0d084a'
        matchScore ='Match Tied 0-0'

    else:
        homeTeam = data[0]
        awayTeam = data[1]
        serve = data[2]
        hTeamScore = data[3]
        aTeamScore = data[4]
        homeScore = data[5]
        awayScore = data[6]
        setNum = data[7]
        set = data[8]
        totalTO = data[9]
        homeTO = data[10]
        awayTO = data[11]
        homePrimaryColor = data[12]
        homeSecondColor = data[13]
        awayPrimaryColor = data[14]
        awaySecondColor = data[15]
        matchScore = data[16]

    yellowColor = '#dbcf30'



    # Team Abrev labels
    homeAbrevL = Label(volleyballCtrl, text=homeTeam, width=20)
    homeAbrevL.bind('<Button-1>', changeHomeAbrev)
    homeAbrevL.place(x=homeTeamLx, y=10, anchor='nw')

    homeAbrevIn = Entry(volleyballCtrl, width=20)
    homeAbrevIn.bind('<Return>', subHomeAbrev)
    homeAbrevIn.place_forget()

    awayAbrevL = Label(volleyballCtrl, text=awayTeam, width=20)
    awayAbrevL.bind('<Button-1>', changeAwayAbrev)
    awayAbrevL.place(x=awayTeamLx, y=10, anchor='ne')

    awayAbrevIn = Entry(volleyballCtrl, width=20)
    awayAbrevIn.bind('<Return>', subAwayAbrev)
    awayAbrevIn.place_forget()

    # Score Elements
    # Score Labels
    homeScoreL = Label(volleyballCtrl, text=homeScore, width=20, height=7)
    homeScoreL.bind("<Button-1>", editHomeScore)
    homeScoreL.place(x=homeScoreLx, y=matchScoreLy, anchor='nw')
    awayScoreL = Label(volleyballCtrl, text=awayScore, width=20, height=7)
    awayScoreL.bind("<Button-1>", editAwayScore)
    awayScoreL.place(x=awayScoreLx, y=matchScoreLy, anchor='ne')

    # Edit Scores
    hEditScore = Entry(volleyballCtrl, width=19)
    hEditScore.bind('<Return>', homeScoreOverride)
    hEditScore.place_forget()
    aEditScore = Entry(volleyballCtrl, width=19)
    aEditScore.bind('<Return>', awayScoreOverride)
    aEditScore.place_forget()

    # Increase Score Buttons
    homeScore1 = Label(volleyballCtrl, text='-1', width=9)
    homeScore1.bind("<Button-1>", hScore1)
    homeScore1.place(x=hscore1x, y=scorey, anchor='nw')

    homeScore2 = Label(volleyballCtrl, text='+1', width=9)
    homeScore2.bind("<Button-1>", hScore2)
    homeScore2.place(x=hscore2x, y=scorey, anchor='nw')

    awayScore1 = Label(volleyballCtrl, text='+1', width=9)
    awayScore1.bind("<Button-1>", aScore1)
    awayScore1.place(x=ascore1x, y=scorey, anchor='ne')
    awayScore2 = Label(volleyballCtrl, text='-1', width=9)
    awayScore2.bind("<Button-1>", aScore2)
    awayScore2.place(x=ascore2x, y=scorey, anchor='ne')

    # Team Scores
    hTeamScoreL = Label(volleyballCtrl, text=hTeamScore, width=12, height=2)
    hTeamScoreL.bind('<Button-1>', changehTeamScore)
    hTeamScoreL.place(x=hFoulLx, y=FoulLy, anchor='nw')

    aTeamScoreL = Label(volleyballCtrl, text=aTeamScore, width=12, height=2)
    aTeamScoreL.bind('<Button-1>', changeaTeamScore)
    aTeamScoreL.place(x=aFoulLx, y=FoulLy, anchor='ne')

    # Team Score Inputs
    hTeamScoreIn = Entry(volleyballCtrl, width=12)
    hTeamScoreIn.bind('<Return>', submithTeamScore)
    hTeamScoreIn.place(x=hFoulLx, y=FoulLy, anchor='nw')
    hTeamScoreIn.place_forget()

    aTeamScoreIn = Entry(volleyballCtrl, width=12)
    aTeamScoreIn.bind('<Return>', submitaTeamScore)
    aTeamScoreIn.place(x=aFoulLx, y=FoulLy, anchor='ne')
    aTeamScoreIn.place_forget()

    # Bonus Labels

    # Add Game Point Buttons
    hGameScoreAd = Label(volleyballCtrl, text="+1", width=6, height=1)
    hGameScoreAd.bind('<Button-1>', hTeamScoreOne)
    hGameScoreAd.place(x=homeFoulAddX, y=foulAdy, anchor='n')

    aGameScoreAd = Label(volleyballCtrl, text="+1", width=6)
    aGameScoreAd.bind('<Button-1>', aTeamScoreOne)
    aGameScoreAd.place(x=awayFoulAddX, y=foulAdy, anchor='n')

    # Clear Team Fouls
    resetMatchLabel = Label(volleyballCtrl, text='Next Set', width=15)
    resetMatchLabel.bind('<Button-1>', resetMatchScore)
    resetMatchLabel.place(x=centerx, y=40, anchor='n')

    # Match Score Static Label
    matchScoreStatic = Label(volleyballCtrl, text='Match Score', fg='#ffffff', bg='#000000')
    matchScoreStatic.place(x=staticMatchX, y=foulLaby, anchor='n')

    # Set Buttons
    setLabel = Label(volleyballCtrl, text=set, width=7)
    setLabel.bind('<Button-1>', changeSet)
    setLabel.place(x=centerx, y=10, anchor='n')

    # Period Input
    setIn = Entry(volleyballCtrl, width=5)
    setIn.bind('<Return>', submitHalf)
    setIn.place_forget()

    # color changing
    setHPrimary = Label(volleyballCtrl, text="Set Home Primary Color", width=20)
    setHPrimary.bind('<Button-1>', changeHPrimary)
    setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')

    setHSecond = Label(volleyballCtrl, text="Set Home Secondary Color", width=20)
    setHSecond.bind('<Button-1>', changeHSecond)
    setHSecond.place(x=hcolorx, y=secColory, anchor='nw')

    setAPrimary = Label(volleyballCtrl, text="Set Away Primary Color", width=20)
    setAPrimary.bind('<Button-1>', changeAPrimary)
    setAPrimary.place(x=acolorx, y=priColory, anchor='ne')

    setASecond = Label(volleyballCtrl, text='Set Away Secondary Color', width=20)
    setASecond.bind('<Button-1>', changeASecond)
    setASecond.place(x=acolorx, y=secColory, anchor='ne')

    hPriIn = Entry(volleyballCtrl, width=18)
    hPriIn.bind('<Return>', subHP)
    hPriIn.place_forget()

    hSecIn = Entry(volleyballCtrl, width=18)
    hSecIn.bind('<Return>', subHS)
    hSecIn.place_forget()

    aPriIn = Entry(volleyballCtrl, width=18)
    aPriIn.bind('<Return>', subAP)
    aPriIn.place_forget()

    aSecIn = Entry(volleyballCtrl, width=18)
    aSecIn.bind('<Return>', subAS)
    aSecIn.place_forget()


    # Match Score String Ctrl

    matchScoreCtrl = Label(volleyballCtrl, text=matchScore, width=20)
    matchScoreCtrl.bind('<Button-1>', changeWeightClass)
    matchScoreCtrl.place(x=centerx, y=70, anchor='n')

    matchScoreIn = Entry(volleyballCtrl, width=15)
    matchScoreIn.bind('<Return>', subWeightClass)
    matchScoreIn.place_forget()

    #serve ctrl

    homeServeFrame = Frame(volleyballCtrl)
    homeServeFrame.config(width = 19, height=90, bg='#ffffff')
    homeServeFrame.bind('<Button-1>', setHomeServe)
    homeServeFrame.place(x=hServeX, y=serveY, anchor = 'nw')

    homeServeCtrl = Label(homeServeFrame, text="S\nE\nR\nV\nE", fg = '#ffffff', bg='#000000')
    homeServeCtrl.bind('<Button-1>', setHomeServe)
    homeServeCtrl.place(x=2,y=2, anchor='nw')


    awayServeFrame = Frame(volleyballCtrl, width = 19, height=90, bg='#ffffff')
    awayServeFrame.bind('<Button-1>', setAwayServe)
    awayServeFrame.place(x=aServeX, y=serveY, anchor = 'ne')

    awayServeCtrl=Label(awayServeFrame, text="S\nE\nR\nV\nE", fg = '#ffffff', bg='#000000')
    awayServeCtrl.bind('<Button-1>', setAwayServe)
    awayServeCtrl.place(x=2, y=2, anchor='nw')

    #Time Outs
    homeTOCtrl = Label(volleyballCtrl, text='TO:\n'+str(totalTO-homeTO))
    homeTOCtrl.bind("<Button-1>", homeResetTO)
    homeTOCtrl.place(x=hTOx, y=TOy, anchor = 'nw')

    homeTakeCtrl = Label(volleyballCtrl, text='Take\nTO')
    homeTakeCtrl.bind('<Button-1>', homeTakeTO)
    homeTakeCtrl.place(x=hTakeTOx, y=takeTOy, anchor='nw')

    awayTOCtrl = Label(volleyballCtrl, text='TO:\n'+str(totalTO-awayTO))
    awayTOCtrl.bind('<Button-1>', awayResetTO)
    awayTOCtrl.place(x=aTOx, y=TOy, anchor='ne')

    awayTakeCtrl = Label(volleyballCtrl, text='Take\nTO')
    awayTakeCtrl.bind('<Button-1>', awayTakeTO)
    awayTakeCtrl.place(x=aTakeTOx, y=takeTOy, anchor='ne')


    # WRESTLINGoverlay



    scoreboardHeight = 35

    serveBarHeight = 3 #the possession bar

    scoreFrameWidth = 55
    teamFrameWidth = 180
    setFrameWidth = 90
    matchFrameWidth = 200

    bottomy = 60


    totalWidth = teamFrameWidth+scoreFrameWidth+teamFrameWidth+scoreFrameWidth+setFrameWidth+matchFrameWidth

    start = (overlayWidth/2)-(totalWidth/2)

    homeScoreX = start+teamFrameWidth
    awayTeamX = homeScoreX+scoreFrameWidth
    awayScoreX = awayTeamX+teamFrameWidth

    timeFramex = awayScoreX + scoreFrameWidth

    matchFramex = timeFramex + setFrameWidth

    homeTeamFrame = Frame(wrestOverlay)
    homeTeamFrame.configure(bg=homePrimaryColor, width=teamFrameWidth, height=scoreboardHeight)
    homeTeamFrame.place(x=start, y=bottomy, anchor='sw')  # 293.33

    homeScoreFrame = Frame(wrestOverlay)
    homeScoreFrame.configure(bg=homeSecondColor, width=scoreFrameWidth, height=scoreboardHeight)
    homeScoreFrame.place(x=homeScoreX, y=bottomy, anchor='sw')

    awayTeamFrame = Frame(wrestOverlay)
    awayTeamFrame.configure(bg=awayPrimaryColor, width=teamFrameWidth, height=scoreboardHeight)
    awayTeamFrame.place(x=awayTeamX, y=bottomy, anchor='sw')

    awayScoreFrame = Frame(wrestOverlay)
    awayScoreFrame.configure(bg=awaySecondColor, width=scoreFrameWidth, height=scoreboardHeight)
    awayScoreFrame.place(x=awayScoreX, y=bottomy, anchor='sw')

    setFrame=Frame(wrestOverlay)
    setFrame.configure(bg='#000000', width=setFrameWidth, height=scoreboardHeight)
    setFrame.place(x=timeFramex, y=bottomy, anchor='sw')


    matchScoreFrame = Frame(wrestOverlay)
    matchScoreFrame.config(bg='#000000', width=matchFrameWidth, height=scoreboardHeight)
    matchScoreFrame.place(x=matchFramex, y=bottomy, anchor='sw')


    homeTeamOver = Label(homeTeamFrame, text=homeTeam)
    homeTeamOver.place(x=10, y=((scoreboardHeight-serveBarHeight)/2), anchor='w')
    homeTeamOver['bg'] = homeTeamOver.master['bg']
    homeTeamOver.config(font=(fFont, 16), fg='#ffffff')

    toBarWidth = (teamFrameWidth/totalTO)-10
    if toBarWidth >35:
        toBarWidth=35

    toBarStart=(teamFrameWidth/2)-((toBarWidth+5)*(totalTO/2))


    homeTOFrames = []

    for i in range(totalTO):
        toBar = Frame(homeTeamFrame)
        toBar.config(bg='#ffffff', width=toBarWidth, height = serveBarHeight)
        toBar.place(x=toBarStart+((toBarWidth+5)*i), y=scoreboardHeight, anchor='sw')
        homeTOFrames.append(toBar)


    homeScoreOver = Label(homeScoreFrame, text=homeScore)
    homeScoreOver.place(x=(scoreFrameWidth/2), y=((scoreboardHeight+serveBarHeight)/2), anchor='c')
    homeScoreOver['bg'] = homeScoreOver.master['bg']
    homeScoreOver.config(font=(fFont, 27), fg='#ffffff')


    homeServeOverlay = Frame(homeScoreFrame)
    homeServeOverlay.config(bg=yellowColor, width=scoreFrameWidth, height = serveBarHeight)
    if(serve=='Home'):
        homeServeOverlay.place(x=0,y=0,anchor='nw')

    awayTeamOver = Label(awayTeamFrame, text=awayTeam)
    awayTeamOver.place(x=10, y=((scoreboardHeight-serveBarHeight)/2), anchor='w')
    awayTeamOver['bg'] = awayTeamOver.master['bg']
    awayTeamOver.config(font=(fFont, 16), fg='#ffffff')

    awayTOFrames=[]

    for i in range(totalTO):
        toBar=Frame(awayTeamFrame)
        toBar.config(bg='#ffffff', width=toBarWidth, height=serveBarHeight)
        toBar.place(x=toBarStart+((toBarWidth+5)*i), y=scoreboardHeight, anchor='sw')
        awayTOFrames.append(toBar)


    awayScoreOver = Label(awayScoreFrame, text=awayScore)
    awayScoreOver.place(x=(scoreFrameWidth/2), y=((scoreboardHeight+serveBarHeight)/2), anchor='c')
    awayScoreOver['bg'] = awayScoreOver.master['bg']
    awayScoreOver.config(font=(fFont, 27), fg='#ffffff')

    awayServeOverlay=Frame(awayScoreFrame)
    awayServeOverlay.config(bg=yellowColor, width=scoreFrameWidth, height=serveBarHeight)
    if (serve=='Home'):
        awayServeOverlay.place(x=0, y=0, anchor='nw')

    setNumOver = Label(setFrame, text=set)
    setNumOver.place(x=(setFrameWidth/2), y=(scoreboardHeight/2), anchor='c')
    setNumOver['bg'] = setNumOver.master['bg']
    setNumOver.config(font=(fFont, 18), fg='#ffffff')


    matchScoreOver = Label(matchScoreFrame, text=matchScore)
    matchScoreOver.place(x=matchFrameWidth/2, y=(scoreboardHeight/2), anchor='c')
    matchScoreOver['bg'] = setNumOver.master['bg']
    matchScoreOver.config(font=(fFont, 16), fg='#ffffff')



    #menubar
    menubar=Menu(volleyballCtrl)
    fileMenu=Menu(menubar, tearoff=0)
    fileMenu.add_command(label='Save Configuration', command=saveConfig)
    fileMenu.add_command(label='Open Configuration', command=openConfig)
    fileMenu.add_separator()
    fileMenu.add_command(label='Quit', command=returnHome)

    serverMenu=Menu(menubar, tearoff=0)
    serverMenu.add_command(label='Start Server', command=openServerSettings)

    menubar.add_cascade(label='File', menu=fileMenu)
    menubar.add_cascade(label='Server', menu=serverMenu)
    volleyballCtrl.config(menu=menubar)

