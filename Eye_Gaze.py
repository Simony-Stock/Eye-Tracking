from tkinter import *     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import math
import string
import cv2 as cv
import numpy as np
import dlib 
import os
import csv

def getGaze(videoname, ext):

  file_name = "shape_predictor_68_face_landmarks.dat" #file with landmark data
  VideoName = videoname #name of the video to be analyzed
  header = ['Left X', 'Left Height', 'Right X', 'Right Height', 'Timestamp'] #header of the csv file table

  #path_parent = os.path.dirname(os.getcwd()) #gets the path to one directory up
  #os.chdir(path_parent) #changes working directory to path_parent
  cap = cv.VideoCapture(str(VideoName) + "." +str(ext)) #camera 0->rear, 1->front, str(VideoName) + ".mp4"
  detector = dlib.get_frontal_face_detector() #build in detector to detect the 4 corner points of the face
  predictor = dlib.shape_predictor(file_name) #predicts the facial landmark points 0 to 67
  rawDataName = VideoName + ".csv" #csv raw data file name

  with open(rawDataName, 'w', encoding='UTF8', newline='') as dataFile:
    writer = csv.writer(dataFile) #open the csv file
    writer.writerow(header) #write in the header row
    while True:
      exists, frame = cap.read() #reads in video frame by frame

      #break if file cannot be found
      if not exists:
        break

      gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #grayscale of frame video
      faces = detector(gray) #array of the faces detected

      for face in faces:

        #find eye landparks
        landmarks = predictor(gray, face)

        #Isolating The Eyes --------------------------------------------------------------------------------
        #array of the eye markers
        Leye = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                        (landmarks.part(37).x, landmarks.part(37).y),
                        (landmarks.part(38).x, landmarks.part(38).y),
                        (landmarks.part(39).x, landmarks.part(39).y),
                        (landmarks.part(40).x, landmarks.part(40).y),
                        (landmarks.part(41).x, landmarks.part(41).y)], np.int32)

        Reye = np.array([(landmarks.part(42).x, landmarks.part(42).y),
                        (landmarks.part(43).x, landmarks.part(43).y),
                        (landmarks.part(44).x, landmarks.part(44).y),
                        (landmarks.part(45).x, landmarks.part(45).y),
                        (landmarks.part(46).x, landmarks.part(46).y),
                        (landmarks.part(47).x, landmarks.part(47).y)], np.int32)

        #4 points of bounding rectangle 
        Lxmax=max(Leye[0][0], Leye[1][0], Leye[2][0], Leye[3][0], Leye[4][0], Leye[5][0])
        Lxmin=min(Leye[0][0], Leye[1][0], Leye[2][0], Leye[3][0], Leye[4][0], Leye[5][0])
        Lymax=max(Leye[0][1], Leye[1][1], Leye[2][1], Leye[3][1], Leye[4][1], Leye[5][1])
        Lymin=min(Leye[0][1], Leye[1][1], Leye[2][1], Leye[3][1], Leye[4][1], Leye[5][1])

        Rxmax=max(Reye[0][0], Reye[1][0], Reye[2][0], Reye[3][0], Reye[4][0], Reye[5][0])
        Rxmin=min(Reye[0][0], Reye[1][0], Reye[2][0], Reye[3][0], Reye[4][0], Reye[5][0])
        Rymax=max(Reye[0][1], Reye[1][1], Reye[2][1], Reye[3][1], Reye[4][1], Reye[5][1])
        Rymin=min(Reye[0][1], Reye[1][1], Reye[2][1], Reye[3][1], Reye[4][1], Reye[5][1])
        
        #add a slight blur to eliminate noise
        #leftEye = cv.GaussianBlur(leftEye, (3,3), 0) 
        #rightEye = cv.GaussianBlur(rightEye, (3,3), 0)

        #outline the eye polygon in white to separate the iris/pupil from any outside noise picked up durring thresholding
        cv.polylines(gray, [Leye], True, (255,255,255), 2) 
        cv.polylines(gray, [Reye], True, (255,255,255), 2) 

        #creates a frame containing only the left eye
        leftEye = gray [Lymin:Lymax,Lxmin:Lxmax] 
        rightEye= gray [Rymin:Rymax,Rxmin:Rxmax]

        #Thresholding -----------------------------------------------------------------------------------------
        #inverse binary thresholf with a threshold vlue of 80
        Lret, Lthresh= cv.threshold(leftEye, 80, 255, cv.THRESH_BINARY_INV) 
        Rret, Rthresh= cv.threshold(rightEye, 80, 255, cv.THRESH_BINARY_INV)

        #outlines the contours created by thresholding
        Lcontours, Lhierarchy = cv.findContours(Lthresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 
        Rcontours, Rhierarchy = cv.findContours(Rthresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        #orders the contours by area this ensures the iris & pupil are in the first contour
        Lcontours = sorted(Lcontours, key=lambda x: cv.contourArea(x), reverse=True) 
        Rcontours = sorted(Rcontours, key=lambda x: cv.contourArea(x), reverse=True)

        #Drawing Guide Lines on the Original Frame ------------------------------------------------------------
        #creating axes
        (Lx,Ly,Lw,Lh) = cv.boundingRect(leftEye)
        Lx=Lx+Lxmin
        Ly=Ly+Lymin
        #***************************verify*************************
        Lmid_left = (Lx , Ly + int(Lh/2))
        Lmid_bottom = (Lx + int(Lw/2), Ly + int(Lh))
        Lmid_right = (Lx + int(Lw), Ly + int(Lh/2))
        Lmid_top = (Lx + int(Lw/2), Ly )
        Lorigin = (int((Lmid_left[0]+Lmid_right[0])/2), int((Lmid_top[1]+Lmid_bottom[1])/2))

        (Rx,Ry,Rw,Rh) = cv.boundingRect(rightEye)
        Rx=Rx+Rxmin
        Ry=Ry+Rymin
        Rmid_left = (Rx , Ry + int(Rh/2))
        Rmid_bottom = (Rx + int(Rw/2), Ry + int(Rh))
        Rmid_right = (Rx + int(Rw), Ry + int(Rh/2))
        Rmid_top = (Rx + int(Rw/2), Ry )
        Rorigin = (int((Rmid_left[0]+Rmid_right[0])/2), int((Rmid_top[1]+Rmid_bottom[1])/2))

        #creats black outline box
        cv.rectangle(frame, (Lx, Ly), (Lx + Lw, Ly + Lh), (0, 0, 0), 1)
        cv.rectangle(frame, (Rx, Ry), (Rx + Rw, Ry + Rh), (0, 0, 0), 1)

        #creats white cross hairs
        cv.line(frame, Lmid_top, Lmid_bottom, (255, 255, 255), 1)
        cv.line(frame, Lmid_right, Lmid_left, (255, 255, 255), 1)
        LWidth = Lmid_right[0] - Lmid_left[0]
        LHeight = Lmid_bottom[1] - Lmid_top[1]
        LHeightNorm = LHeight/LWidth
        #cv.circle(frame, Lmid_bottom, 5, (255,0,0), 2)

        cv.line(frame, Rmid_top, Rmid_bottom, (255, 255, 255), 1)
        cv.line(frame, Rmid_right, Rmid_left, (255, 255, 255), 1)
        RWidth = Rmid_right[0] - Rmid_left[0]
        RHeight = Rmid_bottom[1] - Rmid_top[1]
        RHeightNorm = RHeight/RWidth
        #cv.circle(frame, Rmid_bottom, 5, (255,0,0), 2)

        #Find Pupil Points ------------------------------------------------------------------------------------
        LPupilPoint = (0,0)
        for cnt in Lcontours:
          #lines locating pupils
          (x,y,w,h) = cv.boundingRect(cnt)
          x=x+Lxmin
          y=y+Lymin
          LPupilPoint_abs = (x + int(w/2), y + int(h/2))
          LPupilPoint = ((LPupilPoint_abs[0]-Lorigin[0])/(Lmid_right[0]-Lorigin[0]), (LPupilPoint_abs[1]-Lorigin[1])/(Lmid_top[1]-Lorigin[1]))

          #creats blue outline box
          cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
          
          #creates yellow pupil point
          cv.circle(frame, LPupilPoint_abs, 0, (0, 255, 255), 2)
          break #to ensure you only do the first one (greatest surface area)
        
        RPupilPoint = (0,0)
        for cnt in Rcontours:
          #lines locating pupils
          (x,y,w,h) = cv.boundingRect(cnt)
          x=x+Rxmin
          y=y+Rymin
          RPupilPoint_abs = (x + int(w/2), y + int(h/2))
          RPupilPoint = ((RPupilPoint_abs[0]-Rorigin[0])/(Rmid_right[0]-Rorigin[0]), (RPupilPoint_abs[1]-Rorigin[1])/(Rmid_top[1]-Rorigin[1]))

          #creates blue outline box
          cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

          #creates yellow pupil point
          cv.circle(frame, RPupilPoint_abs, 0, (0, 255, 255), 2)
          break #to ensure you only do the first one (greatest surface area)

        #Recording output values -------------------------------------------------------------------------------      
        output = [str(LPupilPoint[0]), str(LHeightNorm), str(RPupilPoint[0]), str(RHeightNorm),str(math.ceil(cap.get(cv.CAP_PROP_POS_MSEC)))] #str((cap.get(cv.CAP_PROP_POS_FRAMES)))
        writer.writerow(output)

        #Displaying Frames ------------------------------------------------------------------------------------
        #h, w = Lthresh.shape
        #h1, w1 = Rthresh.shape
        #cv.polylines(frame, [Leye], True, (0,0,255), 1) 
        #cv.polylines(frame, [Reye], True, (0,0,255), 1)
        #cv.imshow("Left Threshold", cv.resize(Lthresh, (2*w, 2*h)))
        #cv.imshow("Right Threshold", cv.resize(Rthresh, (2*w1, 2*h1)))
          
      #a half sized frame is better when we read from an mp4 file but the original size is better when reading from the camera
      height, width,_ = frame.shape  
      #***************************cv.imshow("Frame", cv.resize(frame, (math.floor(width/2), math.floor(height/2)))) 
      #cv.imshow("Frame", frame)

      key = cv.waitKey(1)
      if key == 32: #space bar to exit
        break 

  cap.release()
  cv.destroyAllWindows()

  #returning the csv file name
  result = str(VideoName + ".csv")
  return result