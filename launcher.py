import os, requests


response = requests.request("GET", "https://raw.githubusercontent.com/LikeableJuniper/CardGame/main/classes.py")
open("classes.py", "w").close()
open("classes.py", "w").write(response.text.replace("\n", ""))

response = requests.request("GET", "https://raw.githubusercontent.com/LikeableJuniper/CardGame/main/main.py")
open("main.py", "w").close()
open("main.py", "w").write(response.text.replace("\n", ""))


os.system("py main.py")
