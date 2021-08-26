import tkinter as tk
from PIL import ImageTk, Image
from functools import partial
import socket, json, threading, logging

root = tk.Tk()
root.attributes("-fullscreen", True)
deck = []
handCardSlots = []
opponentCardSlots = []
userCardSlots = []
handcards = []

#! Networking variables
HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
sendData = None
recvData = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
canStart = False


def clientListener():
    global HOST, PORT, recvData, s, canStart
    s.connect((HOST, PORT))
    print("Connected")
    canStart = True
    while True:
        recvData = s.recv(1024)
        print(recvData)


def clientSender():
    global sendData, s
    while True:
        if sendData is not None:
            s.sendall(sendData)
            sendData = None


def keepUpdated():
    global recvData, opponentCardSlots
    while True:
        if recvData is not None:
            print("Received Data {0}".format(recvData))
            data = json.loads(recvData)
            opponentCardSlots[data["index"]]["jsonindex"] = data["jsonindex"]
            opponentCardSlots[data["index"]]["hasImage"] = True
            try:
                opponentCardSlots[data["index"]]["Button"].config(image=ImageTk.PhotoImage(Image.open(json.load(open("characters.json", "r"))[data["jsonindex"]]["file"]).resize([177, 100])))
                opponentCardSlots[data["index"]]["Button"].pack()
                print("Finished")
            except Exception as e:
                print(e)
            recvData = None


threading.Thread(target=keepUpdated).start()
threading.Thread(target=clientListener).start()
threading.Thread(target=clientSender).start()


imgKlee = Image.open("Images/klee.png")
imgKlee2=imgKlee.resize([177, 100])
imgKlle = ImageTk.PhotoImage(imgKlee2)

imgT = Image.open("Images/Traveler.png")
imgT2 = imgT.resize([110, 110])
imgT3 = ImageTk.PhotoImage(imgT2)

selected = 0

def handButtonClick(n):
    global selected
    for elem in handCardSlots:
        elem["Button"].config(bg="white")
    handCardSlots[n]["Button"].config(bg="green")
    selected = n


def buttonClick(n, ownedByUser):
    global userCardSlots, selected, sendData
    if ownedByUser:
        if not userCardSlots[n]["hasImage"]:
            userCardSlots[n]["Button"].config(image=handCardSlots[selected]["Button"].cget("image"))
            userCardSlots[n]["hasImage"] = True
            toSend = '{"index": ' + str(n) + ', "jsonindex": '+ str(handCardSlots[selected]["jsonindex"]) + '}'
            sendData = bytes(toSend.encode("utf-8"))


def exitWindow():
    toplevel = tk.Toplevel()
    toplevel.title("")
    toplevel.iconbitmap("Images/toplevelIcon.ico")
    toplevel.geometry("160x90")
    tk.Label(toplevel, text="Do you really want to exit?").place(x=10, y=-20, height=90, width=150)
    tk.Button(toplevel, text="Ok", bg="red", command=exit).place(x=10, y=50, height=30, width=60)
    tk.Button(toplevel, text="Cancel", bg="green", command=toplevel.destroy).place(x=90, y=50, height=30, width=60)


tk.Button(text="Exit", bg="red", command=exitWindow).place(x=10, y=10, height=30, width=50)

for i in range(5):
    opponentCardSlots.append({"Button": tk.Button(root, command=partial(buttonClick, i, ownedByUser=False)), "hasImage": False, "effects": []})

for i in range(5):
    userCardSlots.append({"Button": tk.Button(root, command=partial(buttonClick, i, ownedByUser=True)), "hasImage": False, "effects": []})


for i in range(5):
    handCardSlots.append({"Button": tk.Button(root, command=partial(handButtonClick, i)), "hasImage": False})


opponentCardSlots[0]["Button"].place(x=525, y=190, height=170, width=100)
opponentCardSlots[1]["Button"].place(x=675, y=190, height=170, width=100)
opponentCardSlots[2]["Button"].place(x=825, y=190, height=170, width=100)
opponentCardSlots[3]["Button"].place(x=600, y=10, height=170, width=100)
opponentCardSlots[4]["Button"].place(x=750, y=10, height=170, width=100)
userCardSlots[0]["Button"].place(x=600, y=680, height=170, width=100)
userCardSlots[1]["Button"].place(x=750, y=680, height=170, width=100)
userCardSlots[2]["Button"].place(x=825, y=500, height=170, width=100)
userCardSlots[3]["Button"].place(x=675, y=500, height=170, width=100)
userCardSlots[4]["Button"].place(x=525, y=500, height=170, width=100)
handCardSlots[0]["Button"].place(x=1200, y=500, height=170, width=100)
handCardSlots[1]["Button"].place(x=1300, y=500, height=170, width=100)
handCardSlots[0]["Button"].config(image=imgKlle); handCardSlots[0]["jsonindex"] = 0; handCardSlots[0]["hasImage"] = True
handCardSlots[1]["Button"].config(image=imgT3); handCardSlots[1]["jsonindex"] = 1; handCardSlots[1]["hasImage"] = True


while True:
    if canStart:
        root.mainloop()
