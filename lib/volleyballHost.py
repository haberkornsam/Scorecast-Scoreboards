from tkinter import *
from threading import *
from socket import *
import easygui
import xml.etree.ElementTree as ET


fFont = "Lucida Grande"

scoreboardHeight = 35

serveBarHeight = 3 #the possession bar

scoreFrameWidth = 55
teamFrameWidth = 180
setFrameWidth = 90
matchFrameWidth = 200

bottomy = 60

overlayWidth = 1280
overlayHeight = 120

totalWidth = teamFrameWidth+scoreFrameWidth+teamFrameWidth+scoreFrameWidth+setFrameWidth+matchFrameWidth


sStart = (overlayWidth/2)-(totalWidth/2)

homeScoreX = sStart+teamFrameWidth
awayTeamX = homeScoreX+scoreFrameWidth
awayScoreX = awayTeamX+teamFrameWidth

timeFramex = awayScoreX + scoreFrameWidth

matchFramex = timeFramex + setFrameWidth


class Receive(Thread):
    def __init__(self, server, app):
        Thread.__init__(self)
        self.server = server
        self.app = app



    def run(self):
        while True:
            try:
                text = self.receiveData()
                recvText = text[0]
                if not recvText: break
                if recvText == 'homeTeam':
                    self.app.changeHTeam(text[1])
                elif recvText == 'awayTeam':
                    self.app.changeATeam(text[1])
                elif recvText == 'homeScore':
                    self.app.changeHScore(int(text[1]))
                    self.app.changeServe(str(text[2]))
                elif recvText == 'awayScore':
                    self.app.changeAScore(int(text[1]))
                    self.app.changeServe(str(text[2]))
                elif recvText == 'serve':
                    self.app.changeServe(text[1])
                elif recvText == 'teamScore':
                    self.app.changeTeamScore(int(text[1]), int(text[2]), int(text[3]), text[4])
                elif recvText == 'set':
                    self.app.changeSet(text[1], int(text[2]))
                elif recvText=='homePrimary':
                    self.app.changeHP(text[1])
                elif recvText=='homeSecondary':
                    self.app.changeHS(text[1])
                elif recvText=='awayPrimary':
                    self.app.changeAP(text[1])
                elif recvText=='awaySecondary':
                    self.app.changeAS(text[1])
                elif recvText=='matchScore':
                    self.app.matchUpdate(text[1])
                elif recvText == 'updateTO':
                    self.app.changeHTO(int(text[1]))
                    self.app.changeATO(int(text[2]))
                elif recvText == 'awayTO':
                    self.app.changeATO(int(text[1]))
                elif recvText == 'sync':
                    self.app.changeHTeam(text[1])
                    self.app.changeATeam(text[2])
                    self.app.changeHScore(int(text[3]))
                    self.app.changeAScore(int(text[4]))
                    self.app.changeServe(text[5])
                    self.app.changeTeamScore(int(text[6]), int(text[7]), int(text[8]), text[9])
                    self.app.changeHP(text[10])
                    self.app.changeHS(text[11])
                    self.app.changeAP(text[12])
                    self.app.changeAS(text[13])
                    self.app.changeHTO(int(text[14]))
                    self.app.changeATO(int(text[15]))
                    self.app.matchUpdate(text[16])
            except:
                break



    def receiveData(self):
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
    def changeHTeam(self, newName):
        global homeTeam
        homeTeam = newName
        self.homeTeamOver.config(text=homeTeam)
        self.homeTeamOver.update()

    def changeATeam(self, newName):
        global awayTeam
        awayTeam = newName
        self.awayTeamOver.config(text=awayTeam)
        self.awayTeamOver.update()

    def changeHScore(self, newScore):
        global homeScore
        homeScore = newScore
        self.homeScoreOver.configure(text=homeScore)
        self.homeScoreOver.update()

    def changeAScore(self, newScore):
        global awayScore
        awayScore = newScore
        self.awayScoreOver.configure(text=awayScore)
        self.awayScoreOver.update()

    def changeServe(self, newServe):
        global serve
        serve = newServe
        if(serve=='Home'):
            self.awayServeOverlay.place_forget()
            self.homeServeOverlay.place(x=0,y=0,anchor='nw')
            self.awayServeOverlay.update()
            self.homeServeOverlay.update()
        elif(serve == 'Away'):
            self.awayServeOverlay.place(x=0, y=0, anchor='nw')
            self.homeServeOverlay.place_forget()
            self.awayServeOverlay.update()
            self.homeServeOverlay.update()
        else:
            self.awayServeOverlay.place_forget()
            self.homeServeOverlay.place_forget()
            self.awayServeOverlay.update()
            self.homeServeOverlay.update()

    def changeTeamScore(self, newHomeScore, newAwayScore, newSetNum, newSet):
        global hTeamScore, aTeamScore, matchScore, setNum, set
        hTeamScore=newHomeScore
        aTeamScore=newAwayScore
        set = newSet
        setNum = newSetNum

        if (hTeamScore==aTeamScore):
            matchScore='Match tied '+str(hTeamScore)+'-'+str(aTeamScore)
        elif (hTeamScore>aTeamScore):
            matchScore=homeTeam+' leads '+str(hTeamScore)+'-'+str(aTeamScore)
        elif (aTeamScore>hTeamScore):
            matchScore=awayTeam+' leads '+str(aTeamScore)+'-'+str(hTeamScore)

        self.setNumOver.config(text=set)
        self.matchScoreOver.configure(text=matchScore)

    def changeSet(self, newSet, newSetNum):
        global set, setNum #add set number
        set = newSet
        setNum = newSetNum
        self.setNumOver.configure(text=str(set))

    def changeHP(self, newColor):
        global homePrimaryColor
        homePrimaryColor=newColor
        self.homeTeamFrame.configure(bg=homePrimaryColor)
        self.homeTeamOver.configure(bg=homePrimaryColor)
        self.updateTO()

    def changeHS(self, newColor):
        global homeSecondColor
        homeSecondColor = newColor

        self.homeScoreFrame.config(bg=homeSecondColor)
        self.homeScoreOver.config(bg=homeSecondColor)
        self.updateTO()

    def changeAP(self, newColor):
        global awayPrimaryColor
        awayPrimaryColor = newColor
        self.awayTeamFrame.config(bg=awayPrimaryColor)
        self.awayTeamOver.config(bg=awayPrimaryColor)
        self.updateTO()

    def changeAS(self, newColor):
        global awaySecondColor
        awaySecondColor = newColor
        self.awayScoreFrame.config(bg=awaySecondColor)
        self.awayScoreOver.config(bg=awaySecondColor)
        self.updateTO()

    def matchUpdate(self, newMatchScore):
        global matchScore
        matchScore=newMatchScore
        self.matchScoreOver.config(text=matchScore)
        self.matchScoreOver.update()


    def updateTO(self):
        global homeTO, awayTO, totalTO
        for i in range(totalTO):
            if(i<totalTO-homeTO):
                self.homeTOFrames[i].config(bg='#ffffff')
            else:
                self.homeTOFrames[i]['bg'] = self.homeTOFrames[i].master['bg']
            if(i<totalTO-awayTO):
                self.awayTOFrames[i].config(bg='#ffffff')
            else:
                self.awayTOFrames[i]['bg'] = self.awayTOFrames[i].master['bg']

    def changeHTO(self, newTO):
        global homeTO
        homeTO = newTO
        self.updateTO()

    def changeATO(self, newTO):
        global awayTO
        awayTO = newTO
        self.updateTO()


    def saveConfig(self):
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
        set1 = ET.SubElement(wrestling1, 'Set')
        set1.text = str(set)
        weightClass1=ET.SubElement(wrestling1, 'currentServe')
        weightClass1.text=str(serve)
        weightClass1=ET.SubElement(wrestling1, 'totalTO')
        weightClass1.text=str(totalTO)
        myData=ET.tostring(wrestling1).decode("utf-8")

        configFile=open(str(easygui.filesavebox())+'.xml', 'w')
        configFile.write(myData)

    def openConfig(self):
        global homeScore, awayScore, aTeamScore, hTeamScore, set, \
            homePrimaryColor, homeSecondColor, awayPrimaryColor, awaySecondColor, homeTeam, awayTeam, \
            hTeamScore, aTeamScore, matchScore, homeTO, awayTO, setNum, serve, totalTO
        try:
            tree=ET.parse(easygui.fileopenbox(filetypes=['*.xml'])).getroot()
        except:
            return
        if (tree.tag=='volleyball'):
            self.changeHTeam(str(tree[0][0].text))
            self.changeTeamScore(int(tree[0][1].text),int(tree[1][1].text),int(tree[2].text),str(tree[3].text))
            self.changeHScore(int(tree[0][2].text))
            self.changeHTO(int(tree[0][3].text))
            self.changeHP(str(tree[0][4].text))
            self.changeHS(str(tree[0][5].text))

            self.changeATeam(str(tree[1][0].text))
            self.changeAScore(int(tree[1][2].text))
            self.changeATO(int(tree[1][3].text))
            self.changeAP(str(tree[1][4].text))
            self.changeAS(str(tree[1][5].text))

            self.changeServe(str(tree[4].text))

            totalTO=int(tree[5].text)


    def __init__(self, master, port, data):
        Thread.__init__(self)
        self.master = master


        self.homeTeamFrame=Frame(master)
        self.homeTeamFrame.configure(bg=homePrimaryColor, width=teamFrameWidth, height=scoreboardHeight)
        self.homeTeamFrame.place(x=sStart, y=bottomy, anchor='sw')  # 293.33

        self.homeScoreFrame=Frame(master)
        self.homeScoreFrame.configure(bg=homeSecondColor, width=scoreFrameWidth, height=scoreboardHeight)
        self.homeScoreFrame.place(x=homeScoreX, y=bottomy, anchor='sw')

        self.awayTeamFrame=Frame(master)
        self.awayTeamFrame.configure(bg=awayPrimaryColor, width=teamFrameWidth, height=scoreboardHeight)
        self.awayTeamFrame.place(x=awayTeamX, y=bottomy, anchor='sw')

        self.awayScoreFrame=Frame(master)
        self.awayScoreFrame.configure(bg=awaySecondColor, width=scoreFrameWidth, height=scoreboardHeight)
        self.awayScoreFrame.place(x=awayScoreX, y=bottomy, anchor='sw')

        self.setFrame=Frame(master)
        self.setFrame.configure(bg='#000000', width=setFrameWidth, height=scoreboardHeight)
        self.setFrame.place(x=timeFramex, y=bottomy, anchor='sw')

        self.matchScoreFrame=Frame(master)
        self.matchScoreFrame.config(bg='#000000', width=matchFrameWidth, height=scoreboardHeight)
        self.matchScoreFrame.place(x=matchFramex, y=bottomy, anchor='sw')

        self.homeTeamOver=Label(self.homeTeamFrame, text=homeTeam)
        self.homeTeamOver.place(x=10, y=((scoreboardHeight-serveBarHeight)/2), anchor='w')
        self.homeTeamOver['bg']=self.homeTeamOver.master['bg']
        self.homeTeamOver.config(font=(fFont, 16), fg='#ffffff')

        toBarWidth=(teamFrameWidth/totalTO)-10
        if toBarWidth>35:
            toBarWidth=35

        toBarStart=(teamFrameWidth/2)-((toBarWidth+5)*(totalTO/2))

        self.homeTOFrames=[]

        for i in range(totalTO):
            toBar=Frame(self.homeTeamFrame)
            toBar.config(bg='#ffffff', width=toBarWidth, height=serveBarHeight)
            toBar.place(x=toBarStart+((toBarWidth+5)*i), y=scoreboardHeight, anchor='sw')
            self.homeTOFrames.append(toBar)

        self.homeScoreOver=Label(self.homeScoreFrame, text=homeScore)
        self.homeScoreOver.place(x=(scoreFrameWidth/2), y=((scoreboardHeight+serveBarHeight)/2), anchor='c')
        self.homeScoreOver['bg']=self.homeScoreOver.master['bg']
        self.homeScoreOver.config(font=(fFont, 27), fg='#ffffff')

        self.homeServeOverlay=Frame(self.homeScoreFrame)
        self.homeServeOverlay.config(bg=yellowColor, width=scoreFrameWidth, height=serveBarHeight)
        if (serve=='Home'):
            self.homeServeOverlay.place(x=0, y=0, anchor='nw')

        self.awayTeamOver=Label(self.awayTeamFrame, text=awayTeam)
        self.awayTeamOver.place(x=10, y=((scoreboardHeight-serveBarHeight)/2), anchor='w')
        self.awayTeamOver['bg']=self.awayTeamOver.master['bg']
        self.awayTeamOver.config(font=(fFont, 16), fg='#ffffff')

        self.awayTOFrames=[]

        for i in range(totalTO):
            toBar=Frame(self.awayTeamFrame)
            toBar.config(bg='#ffffff', width=toBarWidth, height=serveBarHeight)
            toBar.place(x=toBarStart+((toBarWidth+5)*i), y=scoreboardHeight, anchor='sw')
            self.awayTOFrames.append(toBar)

        self.awayScoreOver=Label(self.awayScoreFrame, text=awayScore)
        self.awayScoreOver.place(x=(scoreFrameWidth/2), y=((scoreboardHeight+serveBarHeight)/2), anchor='c')
        self.awayScoreOver['bg']=self.awayScoreOver.master['bg']
        self.awayScoreOver.config(font=(fFont, 27), fg='#ffffff')

        self.awayServeOverlay=Frame(self.awayScoreFrame)
        self.awayServeOverlay.config(bg=yellowColor, width=scoreFrameWidth, height=serveBarHeight)
        if (serve=='Home'):
            self.awayServeOverlay.place(x=0, y=0, anchor='nw')

        self.setNumOver=Label(self.setFrame, text=set)
        self.setNumOver.place(x=(setFrameWidth/2), y=(scoreboardHeight/2), anchor='c')
        self.setNumOver['bg']=self.setNumOver.master['bg']
        self.setNumOver.config(font=(fFont, 18), fg='#ffffff')

        self.matchScoreOver=Label(self.matchScoreFrame, text=matchScore)
        self.matchScoreOver.place(x=matchFrameWidth/2, y=(scoreboardHeight/2), anchor='c')
        self.matchScoreOver['bg']=self.setNumOver.master['bg']
        self.matchScoreOver.config(font=(fFont, 16), fg='#ffffff')


        #self.addr='localhost'
        self.addr=''
        self.serverRun = True
        self.port = port
        self.server = socket(AF_INET, SOCK_STREAM)

    def sendConfigData(self, client):
        data = '~volleyball`'
        data += str(homeTeam)+'`'
        data += str(awayTeam)+'`'
        data += str(hTeamScore)+'`'
        data += str(aTeamScore)+'`'
        data += str(homeScore)+'`'
        data += str(awayScore)+'`'
        data += str(homeTO)+'`'
        data += str(awayTO)+'`'
        data += str(homePrimaryColor)+'`'
        data += str(homeSecondColor)+'`'
        data += str(awayPrimaryColor)+'`'
        data += str(awaySecondColor)+'`'
        data += str(serve)+'`'
        data += str(setNum)+'`'
        data += str(set)+'`'
        data += str(totalTO)+'`'
        data += str(matchScore)+'`'
        client.sendall(data.encode())

    def run(self):
        global clients, server
        clients = []
        if self.serverRun == True:
            #if self.addr == 'localHost':
            if self.addr == '':
                self.server.bind((self.addr, self.port))
                self.server.listen(5)
                while(True):
                    self.client, self.addr = self.server.accept()
                    clients.append(self.client)
                    self.sendConfigData(self.client)
                    Receive(self.client, self).start()
        else:
            self.server = socket()
            self.server.bind((self.addr, int(self.port)))

    def stopServe(self):
        global server
        from lib import volleyballStandalone
        data = []
        data.append(homeTeam)
        data.append(awayTeam)
        data.append(serve)
        data.append(hTeamScore)
        data.append(aTeamScore)
        data.append(homeScore)
        data.append(awayScore)
        data.append(setNum)
        data.append(set)
        data.append(totalTO)
        data.append(homeTO)
        data.append(awayTO)
        data.append(homePrimaryColor)
        data.append(homeSecondColor)
        data.append(awayPrimaryColor)
        data.append(awaySecondColor)
        data.append(matchScore)

        self.server.close()
        self.master.destroy()
        volleyballStandalone.start(data=data)


def goMainMenu(event=None):
    overlay.destroy()
    #end processes

def stopServer(ap):
    ap.stopServe()



def start(port, data):
    global homeTeam, awayTeam, serve, hTeamScore, aTeamScore,homeScore, awayScore,setNum, set, totalTO,homeTO, awayTO, \
        homePrimaryColor, awayPrimaryColor, homeSecondColor, awaySecondColor, matchScore, yellowColor, overlay

    homeTeam=data[0]
    awayTeam=data[1]

    serve=data[12]

    hTeamScore=data[2]
    aTeamScore=data[3]

    homeScore=data[4]
    awayScore=data[5]
    setNum=data[13]
    set=data[14]

    totalTO=data[15]

    homeTO=data[6]
    awayTO=data[7]

    homePrimaryColor=data[8]
    homeSecondColor=data[9]
    awayPrimaryColor=data[10]
    awaySecondColor=data[11]
    matchScore=data[16]

    yellowColor='#dbcf30'

    overlay = Tk()
    overlay.configure(bg='#00ff00')
    overlay.geometry('1280x120')
    overlay.title('Scorecast Volleyball Scoreboard')

    overlayApp = App(overlay, port, data)
    overlayApp.start()

    try:
        ip=gethostbyname(getfqdn())
    except:
        ip='Lookup ERROR'


#menubar
    menubar = Menu(overlay)
    fileMenu = Menu(menubar, tearoff=0)
    fileMenu.add_command(label='Save Configuration', command=overlayApp.saveConfig)
    fileMenu.add_command(label='Open Configuration', command=overlayApp.openConfig)
    fileMenu.add_separator()
    fileMenu.add_command(label='Quit', command=goMainMenu)

    serverMenu=Menu(menubar, tearoff=0)
    serverMenu.add_command(label='IP: '+ip, state='disabled')
    serverMenu.add_command(label='Port: '+str(port), state='disabled')
    serverMenu.add_separator()
    serverMenu.add_command(label='Stop Server', command=overlayApp.stopServe)

    menubar.add_cascade(label='File', menu=fileMenu)
    menubar.add_cascade(label='Server', menu=serverMenu)
    overlay.config(menu=menubar)


    overlay.mainloop()