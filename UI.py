from cProfile import label
from tkinter import *
from PIL import ImageTk, Image #must be installed: pip install Pillow
import os

path_parent = os.path.dirname(os.getcwd()) #gets the path to one directory up
os.chdir(path_parent) #changes working directory to path_parent

#creates GUI widget page
wpage = Tk() 
wpage.title("Virtual Low-Cost Eye Tracking Tool for Marketing Research Applications") #title of GUI

#makes page full screen while still having access to page's top toolbar
pagewidth= wpage.winfo_screenwidth()               
pageheight= wpage.winfo_screenheight()               
wpage.geometry("%dx%d" % (pagewidth, pageheight))

#creating images
pic1 = Image.open("ocean1.jpg") #open path to image
pic1 = pic1.resize((768, 432), Image.ANTIALIAS) #(height, width)
pic1Tk = ImageTk.PhotoImage(pic1) #converts image to a tkinter image
L1 = Label(image = pic1Tk) # converts tkinter image to useful label

pic2 = Image.open("ocean2.jpg")
pic2 = pic2.resize((768, 432), Image.ANTIALIAS)
pic2Tk = ImageTk.PhotoImage(pic2)
L2 = Label(image = pic2Tk)

pic3 = Image.open("ocean3.jpg")
pic3 = pic3.resize((768, 432), Image.ANTIALIAS)
pic3Tk = ImageTk.PhotoImage(pic3)
L3 = Label(image = pic3Tk)

pic4 = Image.open("ocean4.jpg")
pic4 = pic4.resize((768, 432), Image.ANTIALIAS)
pic4Tk = ImageTk.PhotoImage(pic4)
L4 = Label(image = pic4Tk)


#creating a start button to open image grid
def startfn():
    L1.grid(column=0, row=1)
    L2.grid(column=0, row=2)
    L3.grid(column=1, row=1)
    L4.grid(column=1, row=2)

#creating start button display
start = Button(wpage, text = "START", command=startfn, bg = "#97FF33", padx = 20, pady = 20)
start.place(x=pagewidth/2, y=0)


wpage.mainloop() #creates continuous loop
