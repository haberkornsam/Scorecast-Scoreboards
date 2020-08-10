from tkinter import *
from threading import *
from socket import *
from time import *
import easygui
import xml.etree.ElementTree as ET
import math

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

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])



class Receive(Thread):
    def __init__(self, s, app):
        Thread.__init__(self)
        self.s = s
        self.app = app

    def run(self):
        while 1:
            pass

    def recieveData(self):
        while True:
            datum = self.s.recv(256).decode('utf-8')
            if datum[0]=='~':
                datum = datum[1:]
                data = datum.split('`')
                return data[:-1]
            else:
                break


class CtrlApp(Thread):
    def changeHomeAbrev(self, event):
        self.homeAbrevL.place_forget()
        self.homeAbrevIn.place(x=homeTeamLx, y=10, anchor='nw')

    def subHomeAbrev(self, event):
        global homeTeam
        homeTeam=str(self.homeAbrevIn.get())
        self.homeAbrevL.config(text=homeTeam)
        self.homeAbrevIn.place_forget()
        self.homeAbrevL.place(x=homeTeamLx, y=10, anchor='nw')
        self.send('homeTeam', homeTeam)

    def changeAwayAbrev(self, event):
        self.awayAbrevL.place_forget()
        self.awayAbrevIn.place(x=awayTeamLx, y=10, anchor='ne')

    def subAwayAbrev(self, event):
        global awayTeam
        awayTeam=str(self.awayAbrevIn.get())
        self.awayAbrevL.config(text=awayTeam)
        self.awayAbrevIn.place_forget()
        self.awayAbrevL.place(x=awayTeamLx, y=10, anchor='ne')
        self.send('awayTeam', homeTeam)

    def abrevUpdate(self):
        self.homeAbrevL.config(text=homeTeam)
        self.awayAbrevL.config(text=awayTeam)

    def editHomeScore(self, event):
        self.homeScoreL.place_forget()
        self.hEditScore.place(x=homeScoreLx, y=teamEditScorey, anchor='nw')


    def editAwayScore(self, event):
        self.awayScoreL.place_forget()
        self.aEditScore.place(x=awayScoreLx, y=teamEditScorey, anchor='ne')

    def homeScoreOverride(self, event):
        global homeScore
        if(int(self.hEditScore.get())<0):
            return
        homeScore = int(self.hEditScore.get())
        self.homeScoreFileUpdate()
        self.hEditScore.place_forget()
        self.homeScoreL.place(x=homeScoreLx, y=matchScoreLy, anchor='nw')


    def awayScoreOverride(self, event):
        global awayScore
        if(int(self.aEditScore.get())<0):
            return
        awayScore = int(self.aEditScore.get())
        self.awayScoreFileUpdate()
        self.aEditScore.place_forget()
        self.awayScoreL.place(x=awayScoreLx, y=matchScoreLy, anchor='ne')

    def homeScoreFileUpdate(self):
        global homeScore
        self.homeScoreL.configure(text=homeScore)
        self.send('homeScore', homeScore, serve)

    def awayScoreFileUpdate(self):
        global awayScore
        self.awayScoreL.configure(text=awayScore)
        self.send('awayScore', awayScore, serve)

    def hScore1(self, event):
        global homeScore
        if(homeScore<=0):
            return
        homeScore -= 1
        self.homeScoreFileUpdate()

    def hScore2(self, event):
        global homeScore, serve
        homeScore += 1
        serve = 'Home'
        self.setServe()
        self.homeScoreFileUpdate()

    def aScore1(self, event):
        global awayScore, serve
        awayScore+=1
        serve='Away'
        self.setServe()
        self.awayScoreFileUpdate()

    def aScore2(self, event):
        global awayScore
        if(awayScore<=0):
            return
        awayScore -=1
        self.awayScoreFileUpdate()

    def setServe(self):
        global serve
        if(serve=='Home'):
            self.homeServeCtrl.configure(bg='#ffffff', fg='#000000')
            self.awayServeCtrl.configure(bg='#000000', fg='#ffffff')
        elif(serve=='Away'):
            self.awayServeCtrl.configure(bg='#ffffff', fg='#000000')
            self.homeServeCtrl.configure(bg='#000000', fg='#ffffff')
        else:
            self.homeServeCtrl.configure(bg='#000000', fg='#ffffff')
            self.awayServeCtrl.configure(bg='#000000', fg='#ffffff')


    def changehTeamScore(self, event):
        self.hTeamScoreL.place_forget()
        self.hTeamScoreIn.place(x=hFoulLx, y=FoulLy, anchor='nw')

    def changeaTeamScore(self, event):
        self.aTeamScoreL.place_forget()
        self.aTeamScoreIn.place(x=aFoulLx, y=FoulLy, anchor='ne')

    def submithTeamScore(self, event):
        global hTeamScore
        if(int(self.hTeamScoreIn.get())<0):
            return
        self.hTeamScoreL.place(x=hFoulLx, y=FoulLy, anchor='nw')
        self.hTeamScoreIn.place_forget()
        hTeamScore = int(self.hTeamScoreIn.get())
        self.teamScoreUpdate()

    def submitaTeamScore(self, event):
        global aTeamScore
        if (int(self.aTeamScoreIn.get())<0):
            return
        aTeamScore=int(self.aTeamScoreIn.get())
        self.aTeamScoreL.place(x=aFoulLx, y=FoulLy, anchor='ne')
        self.aTeamScoreIn.place_forget()
        self.TeamScoreUpdate()

    def hTeamScoreOne(self, event):
        global hTeamScore
        hTeamScore += 1
        self.TeamScoreUpdate()

    def aTeamScoreOne(self, event):
        global aTeamScore
        aTeamScore+=1
        self.TeamScoreUpdate()

    def TeamScoreUpdate(self):
        global hTeamScore, aTeamScore, matchScore, setNum, set

        if (hTeamScore==aTeamScore):
            matchScore='Match tied '+str(hTeamScore)+'-'+str(aTeamScore)
        elif (hTeamScore>aTeamScore):
            matchScore=homeTeam+' leads '+str(hTeamScore)+'-'+str(aTeamScore)
        elif (aTeamScore>hTeamScore):
            matchScore=awayTeam+' leads '+str(aTeamScore)+'-'+str(hTeamScore)

        set = ordinal(setNum)+' Set'
        self.setLabel.configure(text=set)
        self.matchScoreCtrl.configure(text=matchScore)
        self.hTeamScoreL.config(text=hTeamScore)
        self.aTeamScoreL.configure(text=aTeamScore)

        self.send('teamScore', hTeamScore, str(aTeamScore)+'`'+str(setNum)+'`'+str(set))

    def resetMatchScore(self, event):
        global homeScore, awayScore, hTeamScore, aTeamScore, serve, setNum, set
        if (homeScore>awayScore):
            hTeamScore+=1
        else:
            aTeamScore+=1
        homeScore=0
        awayScore=0
        serve='none'
        setNum+=1
        set=ordinal(setNum)+" Set"
        self.setLabel.configure(text=set)
        self.setServe()
        self.TeamScoreUpdate()
        self.homeScoreFileUpdate()
        self.awayScoreFileUpdate()

    def changeSet(self, event):
        self.setLabel.place_forget()
        self.setIn.place(x=centerx, y=10, anchor='n')

    def submitHalf(self, event):
        global set, setNum
        self.setIn.place_forget()
        self.setLabel.place(x=centerx, y=10, anchor='n')
        set=str(self.setIn.get())
        self.setLabel.configure(text=set)
        self.send('set', set, setNum)

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

        homePrimaryColor=str(self.hPriIn.get())
        if (homePrimaryColor[0]!='#'):
            homePrimaryColor='#'+homePrimaryColor
        if (len(homePrimaryColor)!=7):
            return
        self.hPriIn.place_forget()
        self.setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')
        self.send('homePrimary', homePrimaryColor)

    def subHS(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        homeSecondColor=str(self.hSecIn.get())
        if (homeSecondColor[0]!='#'):
            homeSecondColor='#'+homeSecondColor
        if (len(homeSecondColor)!=7):
            return
        self.hSecIn.place_forget()
        self.setHSecond.place(x=hcolorx, y=secColory, anchor='nw')
        self.send('homeSecondary', homeSecondColor)

    def subAP(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        awayPrimaryColor=str(self.aPriIn.get())
        if (awayPrimaryColor[0]!='#'):
            awayPrimaryColor='#'+awayPrimaryColor
        if (len(awayPrimaryColor)!=7):
            return
        self.aPriIn.place_forget()
        self.setAPrimary.place(x=acolorx, y=priColory, anchor='ne')
        self.send('awayPrimary', awayPrimaryColor)

    def subAS(self, event):
        global homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor

        awaySecondColor=str(self.aSecIn.get())
        if (awaySecondColor[0]!='#'):
            awaySecondColor='#'+awaySecondColor
        if (len(awaySecondColor)!=7):
            return
        self.aSecIn.place_forget()
        self.setASecond.place(x=acolorx, y=secColory, anchor='ne')
        self.send('awaySecondary', awaySecondColor)

    def changeWeightClass(self, event):
        self.matchScoreCtrl.place_forget()
        self.matchScoreIn.place(x=centerx, y=70, anchor='n')

    def subWeightClass(self, event):
        global matchScore
        matchScore=str(self.matchScoreIn.get())
        self.weightUpdate()
        self.matchScoreCtrl.place(x=centerx, y=70, anchor='n')
        self.matchScoreIn.place_forget()

    def weightUpdate(self):
        self.matchScoreCtrl.config(text=matchScore)
        self.send('matchScore', matchScore)

    def setHomeServe(self, event):
        global serve
        if(serve == 'Home'):
            serve = 'none'
        else:
            serve = 'Home'
        self.setServe()
        self.send('serve', serve)

    def setAwayServe(self, event):
        global serve
        if(serve=='Away'):
            serve = 'none'
        else:
            serve = 'Away'
        self.setServe()
        self.send('serve', serve)
    def homeResetTO(self, event):
        global homeTO
        homeTO=0
        self.updateTO()
    def homeTakeTO(self, event):
        global homeTO
        if (homeTO<totalTO):
            homeTO+=1
            self.updateTO()
    def awayTakeTO(self, event):
        global awayTO
        if (awayTO<totalTO):
            awayTO+=1
            self.updateTO()
    def awayResetTO(self, event):
        global awayTO
        awayTO=0
        self.updateTO()

    def updateTO(self):
        global awayTO, homeTO, totalTO

        self.homeTOCtrl.config(text='TO:\n'+str(totalTO-homeTO))
        self.awayTOCtrl.config(text='TO:\n'+str(totalTO-awayTO))
        self.send('updateTO', homeTO, awayTO)

    def sync(self):
        data = '~sync`'
        data += str(homeTeam)+'`'
        data += str(awayTeam)+'`'
        data += str(homeScore)+'`'
        data += str(awayScore)+'`'
        data += str(serve)+'`'
        data += str(hTeamScore)+'`'
        data += str(aTeamScore)+'`'
        data += str(setNum)+'`'
        data += str(set)+'`'
        data += str(homePrimaryColor)+'`'
        data += str(homeSecondColor)+'`'
        data += str(awayPrimaryColor)+'`'
        data += str(awaySecondColor)+'`'
        data += str(homeTO)+'`'
        data += str(awayTO)+'`'
        data += str(matchScore)+'`'

        self.s.send(data.encode())

    def updateLabels(self):
        self.sync()
        self.homeScoreFileUpdate()
        self.awayScoreFileUpdate()
        self.TeamScoreUpdate()
        self.setServe()
        self.weightUpdate()
        self.abrevUpdate()



    def openConfig(self, event=None):
        global homeScore, awayScore, aTeamScore, hTeamScore, set, \
            homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, homeTeam, awayTeam, \
            hTeamScore, aTeamScore, matchScore, homeTO, awayTO, setNum, serve, totalTO
        try:
            tree=ET.parse(easygui.fileopenbox(filetypes=['*.xml'])).getroot()
        except:
            return
        if (tree.tag=='volleyball'):
            homeTeam=str(tree[0][0].text)
            hTeamScore=int(tree[0][1].text)
            homeScore=int(tree[0][2].text)
            homeTO=int(tree[0][3].text)
            homePrimaryColor=str(tree[0][4].text)
            homeSecondColor=str(tree[0][5].text)

            awayTeam=str(tree[1][0].text)
            aTeamScore=int(tree[1][1].text)
            awayScore=int(tree[1][2].text)
            awayTO=int(tree[1][3].text)
            awayPrimaryColor=str(tree[1][4].text)
            awaySecondColor=str(tree[1][5].text)

            setNum=int(tree[2].text)
            set=str(tree[3].text)
            serve=str(tree[4].text)
            totalTO=int(tree[5].text)
            self.updateLabels()

    def saveConfig(self, event=None):
        global homeScore, awayScore, aTeamScore, hTeamScore, set, homeTO, awayTO, totalTO, setNum, serve, \
            homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, homeTeam, awayTeam, matchScore
        wrestling1=ET.Element('volleyball')
        homeTeam1=ET.SubElement(wrestling1, 'home')
        hAbrev1=ET.SubElement(homeTeam1, 'name')
        hAbrev1.text=str(homeTeam)
        hTScore1=ET.SubElement(homeTeam1, 'matchScore')
        hTScore1.text=str(hTeamScore)
        hscore1=ET.SubElement(homeTeam1, 'setScore')
        hscore1.text=str(homeScore)
        hscore1=ET.SubElement(homeTeam1, 'timeoutsTaken')
        hscore1.text=str(homeTO)
        hpriColor1=ET.SubElement(homeTeam1, 'primaryColor')
        hpriColor1.text=str(homePrimaryColor)
        hsecColor1=ET.SubElement(homeTeam1, 'secondaryColor')
        hsecColor1.text=str(homeSecondColor)
        awayTeam1=ET.SubElement(wrestling1, 'away')
        aAbrev1=ET.SubElement(awayTeam1, 'name')
        aAbrev1.text=str(awayTeam)
        aTScore1=ET.SubElement(awayTeam1, 'matchScore')
        aTScore1.text=str(aTeamScore)
        ascore1=ET.SubElement(awayTeam1, 'setScore')
        ascore1.text=str(awayScore)
        ascore1=ET.SubElement(awayTeam1, 'timeoutsTaken')
        ascore1.text=str(awayScore)
        apriColor1=ET.SubElement(awayTeam1, 'primaryColor')
        apriColor1.text=str(awayPrimaryColor)
        asecColor1=ET.SubElement(awayTeam1, 'secondaryColor')
        asecColor1.text=str(awaySecondColor)

        half1=ET.SubElement(wrestling1, 'SetNumber')
        half1.text=str(setNum)
        set1=ET.SubElement(wrestling1, 'Set')
        set1.text=str(set)
        weightClass1=ET.SubElement(wrestling1, 'currentServe')
        weightClass1.text=str(serve)
        weightClass1=ET.SubElement(wrestling1, 'totalTO')
        weightClass1.text=str(totalTO)
        myData=ET.tostring(wrestling1).decode("utf-8")

        configFile=open(str(easygui.filesavebox())+'.xml', 'w')
        configFile.write(myData)

    def returnHome(self, event=None):
        self.master.destroy()



    def __init__(self, master, s, data):
        self.s = s
        self.master = master
        Thread.__init__(self)

        self.homeAbrevL=Label(master, text=homeTeam, width=20)
        self.homeAbrevL.bind('<Button-1>', self.changeHomeAbrev)
        self.homeAbrevL.place(x=homeTeamLx, y=10, anchor='nw')

        self.homeAbrevIn=Entry(master, width=20)
        self.homeAbrevIn.bind('<Return>', self.subHomeAbrev)
        self.homeAbrevIn.place_forget()

        self.awayAbrevL=Label(master, text=awayTeam, width=20)
        self.awayAbrevL.bind('<Button-1>', self.changeAwayAbrev)
        self.awayAbrevL.place(x=awayTeamLx, y=10, anchor='ne')

        self.awayAbrevIn=Entry(master, width=20)
        self.awayAbrevIn.bind('<Return>', self.subAwayAbrev)
        self.awayAbrevIn.place_forget()

        # Score Elements
        # Score Labels
        self.homeScoreL=Label(master, text=homeScore, width=20, height=7)
        self.homeScoreL.bind("<Button-1>", self.editHomeScore)
        self.homeScoreL.place(x=homeScoreLx, y=matchScoreLy, anchor='nw')
        self.awayScoreL=Label(master, text=awayScore, width=20, height=7)
        self.awayScoreL.bind("<Button-1>", self.editAwayScore)
        self.awayScoreL.place(x=awayScoreLx, y=matchScoreLy, anchor='ne')

        # Edit Scores
        self.hEditScore=Entry(master, width=19)
        self.hEditScore.bind('<Return>', self.homeScoreOverride)
        self.hEditScore.place_forget()
        self.aEditScore=Entry(master, width=19)
        self.aEditScore.bind('<Return>', self.awayScoreOverride)
        self.aEditScore.place_forget()

        # Increase Score Buttons
        self.homeScore1=Label(master, text='-1', width=9)
        self.homeScore1.bind("<Button-1>", self.hScore1)
        self.homeScore1.place(x=hscore1x, y=scorey, anchor='nw')

        self.homeScore2=Label(master, text='+1', width=9)
        self.homeScore2.bind("<Button-1>", self.hScore2)
        self.homeScore2.place(x=hscore2x, y=scorey, anchor='nw')

        self.awayScore1=Label(master, text='+1', width=9)
        self.awayScore1.bind("<Button-1>", self.aScore1)
        self.awayScore1.place(x=ascore1x, y=scorey, anchor='ne')
        self.awayScore2=Label(master, text='-1', width=9)
        self.awayScore2.bind("<Button-1>", self.aScore2)
        self.awayScore2.place(x=ascore2x, y=scorey, anchor='ne')

        # Team Scores
        self.hTeamScoreL=Label(master, text=hTeamScore, width=12, height=2)
        self.hTeamScoreL.bind('<Button-1>', self.changehTeamScore)
        self.hTeamScoreL.place(x=hFoulLx, y=FoulLy, anchor='nw')

        self.aTeamScoreL=Label(master, text=aTeamScore, width=12, height=2)
        self.aTeamScoreL.bind('<Button-1>', self.changeaTeamScore)
        self.aTeamScoreL.place(x=aFoulLx, y=FoulLy, anchor='ne')

        # Team Score Inputs
        self.hTeamScoreIn=Entry(master, width=12)
        self.hTeamScoreIn.bind('<Return>', self.submithTeamScore)
        self.hTeamScoreIn.place(x=hFoulLx, y=FoulLy, anchor='nw')
        self.hTeamScoreIn.place_forget()

        self.aTeamScoreIn=Entry(master, width=12)
        self.aTeamScoreIn.bind('<Return>', self.submitaTeamScore)
        self.aTeamScoreIn.place(x=aFoulLx, y=FoulLy, anchor='ne')
        self.aTeamScoreIn.place_forget()

        # Bonus Labels

        # Add Game Point Buttons
        self.hGameScoreAd=Label(master, text="+1", width=6, height=1)
        self.hGameScoreAd.bind('<Button-1>', self.hTeamScoreOne)
        self.hGameScoreAd.place(x=homeFoulAddX, y=foulAdy, anchor='n')

        self.aGameScoreAd=Label(master, text="+1", width=6)
        self.aGameScoreAd.bind('<Button-1>', self.aTeamScoreOne)
        self.aGameScoreAd.place(x=awayFoulAddX, y=foulAdy, anchor='n')

        # Clear Team Fouls
        self.resetMatchLabel=Label(master, text='Next Set', width=15)
        self.resetMatchLabel.bind('<Button-1>', self.resetMatchScore)
        self.resetMatchLabel.place(x=centerx, y=40, anchor='n')

        # Match Score Static Label
        self.matchScoreStatic=Label(master, text='Match Score', fg='#ffffff', bg='#000000')
        self.matchScoreStatic.place(x=staticMatchX, y=foulLaby, anchor='n')

        # Set Buttons
        self.setLabel=Label(master, text=set, width=7)
        self.setLabel.bind('<Button-1>', self.changeSet)
        self.setLabel.place(x=centerx, y=10, anchor='n')

        # Period Input
        self.setIn=Entry(master, width=5)
        self.setIn.bind('<Return>', self.submitHalf)
        self.setIn.place_forget()

        # color changing
        self.setHPrimary=Label(master, text="Set Home Primary Color", width=20)
        self.setHPrimary.bind('<Button-1>', self.changeHPrimary)
        self.setHPrimary.place(x=hcolorx, y=priColory, anchor='nw')

        self.setHSecond=Label(master, text="Set Home Secondary Color", width=20)
        self.setHSecond.bind('<Button-1>', self.changeHSecond)
        self.setHSecond.place(x=hcolorx, y=secColory, anchor='nw')

        self.setAPrimary=Label(master, text="Set Away Primary Color", width=20)
        self.setAPrimary.bind('<Button-1>', self.changeAPrimary)
        self.setAPrimary.place(x=acolorx, y=priColory, anchor='ne')

        self.setASecond=Label(master, text='Set Away Secondary Color', width=20)
        self.setASecond.bind('<Button-1>', self.changeASecond)
        self.setASecond.place(x=acolorx, y=secColory, anchor='ne')

        self.hPriIn=Entry(master, width=18)
        self.hPriIn.bind('<Return>', self.subHP)
        self.hPriIn.place_forget()

        self.hSecIn=Entry(master, width=18)
        self.hSecIn.bind('<Return>', self.subHS)
        self.hSecIn.place_forget()

        self.aPriIn=Entry(master, width=18)
        self.aPriIn.bind('<Return>', self.subAP)
        self.aPriIn.place_forget()

        self.aSecIn=Entry(master, width=18)
        self.aSecIn.bind('<Return>', self.subAS)
        self.aSecIn.place_forget()

        # Match Score String Ctrl

        self.matchScoreCtrl=Label(master, text=matchScore, width=20)
        self.matchScoreCtrl.bind('<Button-1>', self.changeWeightClass)
        self.matchScoreCtrl.place(x=centerx, y=70, anchor='n')

        self.matchScoreIn=Entry(master, width=15)
        self.matchScoreIn.bind('<Return>', self.subWeightClass)
        self.matchScoreIn.place_forget()

        # serve ctrl

        self.homeServeFrame=Frame(master)
        self.homeServeFrame.config(width=19, height=90, bg='#ffffff')
        self.homeServeFrame.bind('<Button-1>', self.setHomeServe)
        self.homeServeFrame.place(x=hServeX, y=serveY, anchor='nw')

        self.homeServeCtrl=Label(self.homeServeFrame, text="S\nE\nR\nV\nE", fg='#ffffff', bg='#000000')
        self.homeServeCtrl.bind('<Button-1>', self.setHomeServe)
        self.homeServeCtrl.place(x=2, y=2, anchor='nw')

        self.awayServeFrame=Frame(master, width=19, height=90, bg='#ffffff')
        self.awayServeFrame.bind('<Button-1>', self.setAwayServe)
        self.awayServeFrame.place(x=aServeX, y=serveY, anchor='ne')

        self.awayServeCtrl=Label(self.awayServeFrame, text="S\nE\nR\nV\nE", fg='#ffffff', bg='#000000')
        self.awayServeCtrl.bind('<Button-1>', self.setAwayServe)
        self.awayServeCtrl.place(x=2, y=2, anchor='nw')

        # Time Outs
        self.homeTOCtrl=Label(master, text='TO:\n'+str(totalTO-homeTO))
        self.homeTOCtrl.bind("<Button-1>", self.homeResetTO)
        self.homeTOCtrl.place(x=hTOx, y=TOy, anchor='nw')

        self.homeTakeCtrl=Label(master, text='Take\nTO')
        self.homeTakeCtrl.bind('<Button-1>', self.homeTakeTO)
        self.homeTakeCtrl.place(x=hTakeTOx, y=takeTOy, anchor='nw')

        self.awayTOCtrl=Label(master, text='TO:\n'+str(totalTO-awayTO))
        self.awayTOCtrl.bind('<Button-1>', self.awayResetTO)
        self.awayTOCtrl.place(x=aTOx, y=TOy, anchor='ne')

        self.awayTakeCtrl=Label(master, text='Take\nTO')
        self.awayTakeCtrl.bind('<Button-1>', self.awayTakeTO)
        self.awayTakeCtrl.place(x=aTakeTOx, y=takeTOy, anchor='ne')

        # menubar
        self.menubar=Menu(master)
        fileMenu=Menu(self.menubar, tearoff=0)
        fileMenu.add_command(label='Save Configuration', command=self.saveConfig)
        fileMenu.add_command(label='Open Configuration', command=self.openConfig)
        fileMenu.add_separator()
        fileMenu.add_command(label='Quit', command=self.returnHome)

        #serverMenu=Menu(menubar, tearoff=0)
        #serverMenu.add_command(label='Start Server', command=openServerSettings)

        self.menubar.add_cascade(label='File', menu=fileMenu)
        #menubar.add_cascade(label='Server', menu=serverMenu)
        master.config(menu=self.menubar)


        Receive(s, self).start()

    def send(self, arg, value=None, value2=None):
        data1 = '~'+arg+'`'
        if(value != None):
            data1 += str(value)+'`'
        if value2 != None:
            data1 += str(value2)+'`'
        self.s.send(data1.encode())




def start(data, s):
    global homeTeam, awayTeam, serve, hTeamScore, aTeamScore, homeScore, awayScore, setNum, set, totalTO, homeTO, \
        awayTO, homePrimaryColor, awayPrimaryColor, homeSecondColor, awaySecondColor, matchScore, yellowColor

    homeTeam=str(data[1])
    awayTeam=str(data[2])

    serve=str(data[13])

    hTeamScore=int(data[3])
    aTeamScore=int(data[4])

    homeScore=int(data[5])
    awayScore=int(data[6])
    setNum=int(data[14])
    set=str(data[15])

    totalTO=int(data[16])

    homeTO=int(data[7])
    awayTO=int(data[8])

    homePrimaryColor=str(data[9])
    homeSecondColor=str(data[10])
    awayPrimaryColor=str(data[11])
    awaySecondColor=str(data[12])
    matchScore=str(data[17])

    yellowColor='#dbcf30'

    volleyballCtrl = Tk()
    volleyballCtrl.configure(bg='#000000')
    volleyballCtrl.title("Scorecast Volleyball Controller")
    volleyballCtrl.geometry('600x260')

    app = CtrlApp(volleyballCtrl, s, data).start()

    volleyballCtrl.mainloop()