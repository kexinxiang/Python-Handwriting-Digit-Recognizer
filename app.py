from tkinter import *
import numpy as np
import PIL
from PIL import ImageTk, Image, ImageDraw
import math
import pickle
import flask
import requests
from flask import request


url = "http://127.0.0.1:5000/recognize"

root = Tk()
root.title("Handwriting digit recognizer")
root.geometry("800x600")

width = 560
height = 560
center = height // 2
white = (255, 255, 255)
    

def show():
    image2 = image1.resize((28,28), resample=PIL.Image.ANTIALIAS)
    filename = "drawn_digit.png"
    image2.save(filename)
    drawn_digit = []
    result = np.array(image2)
    for row in result:
        for col in row:
            drawn_digit.append(255 - col[0])
    serialized_arr = pickle.dumps(drawn_digit)
    trans = requests.post(url, data=serialized_arr, timeout=10)  #transmitting drawn digit array
    number_label.config(text=str(pickle.loads(trans.content)))

def clear():
    c.delete(ALL)
    draw.rectangle([0,0,width,height],fill="white")
    number_label.config(text="...")

def draw_lines(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    c.create_oval(x1, y1, x2, y2, fill="black", width=20)
    draw.ellipse([event.x-20, event.y-20, event.x+20, event.y+20], fill="black")
         
#creating canvas, label, buttons
c = Canvas(root, width=width, height=height,bg="white", cursor="circle")
recog_bt=Button(root, text="recognize", command=show)
clear_bt=Button(root,text="clear", command=clear)
number_label=Label(root, text="...", font=("Helvetica",48))

#positioning
c.grid(row=0, column=0, pady=2, sticky=W)
recog_bt.grid(row=1, column=2, pady=2, padx=2)
clear_bt.grid(row=1, column=0, pady=2)
number_label.grid(row=0, column=1, pady=2, padx=2)

#saving image
image1 = PIL.Image.new("RGB",(width, height), white)
draw = ImageDraw.Draw(image1)

c.bind("<B1-Motion>",draw_lines)


root.mainloop()
