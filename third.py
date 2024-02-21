global res

from PIL import Image
from moviepy.editor import *
import time
import os
import framing
import threading

# file = open("fps.txt")
# fp = 1 / int(file.read)
# file.close()
# print(fp)
import pyglet


def code(d, z):
    global res, rsize
    rimg = Image.open(r"frames\frame{0}.jpg".format(z))
    img = rimg.resize(rsize)
    size = img.size
    res = ""
    for i in range(size[1]):
        for a in range(size[0]):
            temp = img.getpixel((a, i))
            if temp == 0:
                res += " "
                continue
            R = temp[0]
            G = temp[1]
            B = temp[2]
            Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
            y = Y // 21.25 + 1
            res += d[y]
        res += "\n"


def play(zmax, test=0):
    global timer
    z = 0
    if test == 0:
        while z < int(zmax):
            thread = threading.Thread(target=code, args=(d, z))
            thread.run()
            time.sleep(fp - timer)  # 0.023
            print(res)
            z += 1
            if z % 150 == 0:
                os.system("cls")
    else:
        start = time.time()
        while z < int(zmax):
            thread = threading.Thread(target=code, args=(d, z))
            thread.run()
            print(res)
            z += 1
        stop = time.time()
        timer = (stop - start) / zmax


while 1:
    ppp = int(input("1. Framing\n2. Playing\n"))
    if ppp == 1:
        name = input("Filename: ")
        framing.FrameCapture(name)
        video = VideoFileClip(name)
        audio = video.audio
        audio.write_audiofile("audio.mp3")
    elif ppp == 3:
        name = input("Filename: ")
        video = VideoFileClip(name)
        audio = video.audio
        audio.write_audiofile("audio.mp3")
    else:
        if int(input("Original speed(w sound): ")) == 1:
            file = open("fps.txt")
            fp = round(1 / int(file.readlines()[0]), 2)
            file.close()
            flag = 1
        else:
            fp = float(input("Delay: "))
            flag = 0
        name = r"frames\frame0.jpg"
        img = Image.open(name)
        size = img.size
        # ratio = size[0]/size[1]
        # wsize1 = int(input("x"))
        # rsize = (wsize1, round(wsize1*ratio))
        rsize = (size[0] // 10, size[1] // 10)
        invert_color = int(input("Invert color(0 1): "))
        # os.system("mode con cols=100 lines=100")
        os.system("mode con cols={0} lines={1}".format(str(rsize[0]), str(rsize[1])))

        if invert_color == 0:
            d = {1: ".", 2: ",", 3: "-", 4: "~", 5: ":", 6: ";", 7: "=", 8: "!", 9: "*", 10: "#", 11: "$", 12: "@"}
        else:
            d = {1: "@", 2: "$", 3: "#", 4: "*", 5: "!", 6: "=", 7: ";", 8: ":", 9: "~", 10: "-", 11: ",", 12: "."}
        z = 0
        file = open("fps.txt")
        zmax = file.readlines()[1]
        file.close()
        play(610, 1)
        input(timer)
        if flag == 1:
            song = pyglet.media.load('audio.mp3')
            song.play()
        play(zmax)



