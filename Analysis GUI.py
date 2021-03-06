from multiprocessing.connection import wait
import os
from time import *
from tkinter import *  
from tkinter.filedialog import askopenfilename
import string
import Eye_Gaze
import Eye_Fixation
import Data_Analysis

#combine all processes into one. say "Processing..." and the "Complete"

filename = string

path_parent = os.path.dirname(os.getcwd()) #gets the path to one directory up
os.chdir(path_parent) #changes working directory to path_parent

def MyButtonClicked():
  global filename
  global status1
  global status2
  global status3

  filepath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
  filename = filepath.split("/")[-1]

  lbl1=Label(p4, text='Step 1 - Raw Data Capture: ', fg='black', font=("Helvetica", 9))
  lbl1.pack(side = LEFT)
  status1 = Label(p4, text='Waiting', fg='red', font=("Helvetica", 9))
  status1.pack(side = LEFT)

  lbl2=Label(p5, text='Step 2 - Data Processing: ', fg='black', font=("Helvetica", 9))
  lbl2.pack(side = LEFT)
  status2 = Label(p5, text='Waiting', fg='red', font=("Helvetica", 9))
  status2.pack(side = LEFT)

  lbl3=Label(p6, text='Step 3 - Data Visualization: ', fg='black', font=("Helvetica", 9))
  lbl3.pack(side = LEFT)
  status3 = Label(p6, text='Waiting', fg='red', font=("Helvetica", 9))
  status3.pack(side = LEFT)

  #text- filename.ext
  lbl=Label(p2, text=str(filename), fg='black', font=("Helvetica", 9))
  lbl.pack(side = LEFT)

  #submit button
  btn=Button(p3, text="Submit", fg='red', command = lambda: StartAnalysis()) #lambda means only run function after button is pressed and lets you pass in arguments
  btn.pack(side = LEFT)
  
def StartAnalysis():
  global filename
  global status1
  global status2
  global status3

  #Step 1 ------------------------------------------------------------------------------------
  status1 = Processing(p4,status1)
  gazeFile = Eye_Gaze.getGaze(filename.split(".")[0], filename.split(".")[1]) #passes in the video file and returns the gaze csv file name
  Complete(p4,status1)

  #Step 2 ------------------------------------------------------------------------------------
  status2 = Processing(p5,status2)
  fixFile = Eye_Fixation.getFix(gazeFile.split(".")[0], gazeFile.split(".")[1]) #passes in the video file and returns the gaze csv file name
  Complete(p5,status2)

  #Step 3 ------------------------------------------------------------------------------------
  status3 = Processing(p6,status3)
  analysisFile = Data_Analysis.getAnalysis(fixFile.split(".")[0], fixFile.split(".")[1]) #passes in the video file and returns the gaze csv file name
  Complete(p6,status3)

  lbl=Label(p7, text='Results stored in ' + str(fixFile), fg='black', font=("Helvetica", 9))
  lbl.pack(side = BOTTOM)

def Processing(panel, label):
  label.destroy()
  label=Label(panel, text='Processing...', fg='orange', font=("Helvetica", 9))
  label.pack(side=LEFT)
  Tk. update_idletasks(window)
  return label

def Complete(panel, label):
  label.destroy()
  label=Label(panel, text='Complete', fg='green', font=("Helvetica", 9))
  label.pack(side = LEFT)
  Tk. update_idletasks(window)

window = Tk() #open window
p1 = PanedWindow()
p1.pack(side = TOP)

p2 = PanedWindow()
p2.pack(side = TOP)

p3 = PanedWindow()
p3.pack(side = TOP)

p4 = PanedWindow()
p4.pack(side = TOP)

p5 = PanedWindow()
p5.pack(side = TOP)

p6 = PanedWindow()
p6.pack(side = TOP)

p7 = PanedWindow()
p7.pack(side = TOP)

#text- Please select video file
lbl=Label(p1, text="Please select video file: ", fg='black', font=("Helvetica", 14))
lbl.pack(side = LEFT)

#File search button
btn=Button(p2, text="Choose file", fg='black', command=MyButtonClicked)
btn.pack(side=LEFT)

window.title('Analysis GUI')
window.geometry("800x200+10+20")
window.mainloop()