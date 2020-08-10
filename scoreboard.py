from tkinter import *
from PIL import ImageTk, Image
from lib import basketballStandalone, basketballClient, wrestlingStandalone, wrestlingClient, baseballStandalone, \
    baseballClient
from socket import *
import os

fFont = "Lucida Grande"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def clickBasketball(event):
    root.destroy()
    basketballStandalone.start()


def clickWrestling(event):
    root.destroy()
    wrestlingStandalone.start()


def clickBaseball(event):
    root.destroy()
    baseballStandalone.start()


def connectToHost(event):
    global ip, port
    s=socket()
    ip = str(ipIn.get())
    port = int(portIn.get())
    s.connect((ip, port))
    text = s.recv(256).decode('utf-8')
    dat = text.split('`')
    dat = dat[:-1]

    root.destroy()
    if dat[0] == 'basketball':
        basketballClient.start(ip, port, s, dat)
    elif dat[0] == 'wrestling':
        wrestlingClient.start(dat, s)
    elif dat[0] == 'baseball':
        baseballClient.start(dat, s)



ipy=420
porty=ipy+30
connecty = porty+30

baskety = 200
wrestlingy = baskety + 80
basey = wrestlingy + 80

basketpicy = baskety-40
wrestlingpicy = wrestlingy-40
basepicy=basey-40


def main():
    global root, connectLabel, ipIn, portIn
    root = Tk()
    root.configure(bg='#000000')
    root.title("Scorecast Controller")
    root.geometry('500x500')

    welcomeLabel = Label(root, text='Welcome!\n\n Please Select what scoreboard you would like to use!')
    welcomeLabel.place(x=250, y=50, anchor='c')
    welcomeLabel.config(font=(fFont, 15, 'bold'), fg='#ffffff', bg='#000000')

    connectLabel = Label(root, text='Connect to Host', width=15, height=1)
    connectLabel.place(x=250, y=connecty, anchor='c')
    connectLabel.bind("<Button-1>", connectToHost)
    ipStatic = Label(root, text='IP: ', bg='#000000', fg='#ffffff')
    ipStatic.place(x=210, y=ipy, anchor = 'e')
    ipIn = Entry(root, width=10)
    ipIn.place(x=212, y=ipy, anchor='w')

    portStatic = Label(root, text='Port: ', bg='#000000', fg='#ffffff')
    portStatic.place(x=210, y=porty, anchor = 'e')
    portIn = Entry(root, width=10)
    portIn.place(x=212, y=porty, anchor='w')



    selectBasketball = Label(root, text='BASKETBALL', width=15, height=5, fg='#ffffff', bg='#000000')
    selectBasketball.bind("<Button-1>", clickBasketball)
    selectBasketball.place(x=250, y=baskety, anchor='c')

    selectWrestling = Label(root, text='WRESTLING', width=15, height=5, fg='#ffffff', bg='#000000')
    selectWrestling.bind("<Button-1>", clickWrestling)
    selectWrestling.place(x=250, y=wrestlingy, anchor='c')

    selectBaseball = Label(root, text='BASEBALL', width=15, height=5, fg='#ffffff', bg='#000000')
    selectBaseball.bind("<Button-1>", clickBaseball)
    selectBaseball.place(x=250, y=basey, anchor='c')

    basketballImagePath = resource_path("basketballScoreboardImage.png")
    basketballImg = ImageTk.PhotoImage(Image.open(basketballImagePath).resize((300, 31)))
    basketballPreview = Label(root, image=basketballImg)
    basketballPreview.bind("<Button-1>", clickBasketball)
    basketballPreview.place(x=250, y=basketpicy, anchor='c')

    wrestlingImagePath = resource_path("wrestlingScoreboardImage.png")
    wrestlingImg = ImageTk.PhotoImage(Image.open(wrestlingImagePath).resize((300, 27)))
    wrestlingPreview = Label(root, image=wrestlingImg)
    wrestlingPreview.bind("<Button-1>", clickWrestling)
    wrestlingPreview.place(x=250, y=wrestlingpicy, anchor='c')

    baseballImagePath = resource_path("baseballScoreboardImage.png")
    baseballImg = ImageTk.PhotoImage(Image.open(baseballImagePath).resize((100, 27)))
    baseballPreview = Label(root, image=baseballImg)
    baseballPreview.bind("<Button-1>", clickBaseball)
    baseballPreview.place(x=250, y=basepicy, anchor='c')

    menubar=Menu(root)
    # fileMenu = Menu(menubar, tearoff = 0)
    # fileMenu.add_command(label = 'basketball', command = clickBasketball)
    # menubar.add_cascade(label = 'File', menu=fileMenu)
    root.config(menu=menubar)

    root.mainloop()



main()