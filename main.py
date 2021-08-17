from classes import Card
import tkinter as tk


deck = list[Card]


root = tk.Tk()
root.attributes("-fullscreen", True)


def exitWindow():
    toplevel = tk.Toplevel()
    toplevel.title("")
    toplevel.iconbitmap("Images/toplevelIcon.ico")
    toplevel.geometry("160x90")
    tk.Label(toplevel, text="Do you really want to exit?").place(x=10, y=10)
    tk.Button(toplevel, text="Ok", bg="red", command=root.destroy).place(x=10, y=50)
    tk.Button(toplevel, text="Cancel", bg="green", command=toplevel.destroy).place(x=50, y=50)


tk.Button(text="Exit", bg="red", command=exitWindow).place(x=10, y=10, height=30, width=50)


root.mainloop()
