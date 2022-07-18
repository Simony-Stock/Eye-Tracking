import cv2 as cv
import numpy as np
import dlib 
import os

path_parent = os.path.dirname(os.getcwd()) #gets the path to one directory up
os.chdir(path_parent) #changes working directory to path_parent

cap = cv.VideoCapture("Eye Movement.mp4") #camera 0->rear, 1->front
detector = dlib.get_frontal_face_detector() #build in detector to detect the 4 corner points of the face

file_name = "shape_predictor_68_face_landmarks.dat" #file with landmark data
 
predictor = dlib.shape_predictor(file_name) #predicts the facial landmark points 0 to 67

while True:
  _,frame = cap.read() #front facing video
  gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #grayscale of frame video

  faces = detector(gray) #array of the 4 corner points on the face
  for face in faces:

    #display eye landparks
    landmarks = predictor(gray, face)

    #Left Eye
    Leye = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                            (landmarks.part(37).x, landmarks.part(37).y),
                            (landmarks.part(38).x, landmarks.part(38).y),
                            (landmarks.part(39).x, landmarks.part(39).y),
                            (landmarks.part(40).x, landmarks.part(40).y),
                            (landmarks.part(41).x, landmarks.part(41).y)], np.int32)

    xmax=max(Leye[0][0], Leye[1][0], Leye[2][0], Leye[3][0], Leye[4][0], Leye[5][0])
    xmin=min(Leye[0][0], Leye[1][0], Leye[2][0], Leye[3][0], Leye[4][0], Leye[5][0])
    ymax=max(Leye[0][1], Leye[1][1], Leye[2][1], Leye[3][1], Leye[4][1], Leye[5][1])
    ymin=min(Leye[0][1], Leye[1][1], Leye[2][1], Leye[3][1], Leye[4][1], Leye[5][1])
    

    leftEye= frame [ymin:ymax,xmin:xmax]
    leftEye = cv.cvtColor(leftEye, cv.COLOR_BGR2GRAY)
    leftEye = cv.GaussianBlur(leftEye, (5,5), 0)

    Lret, Lthresh= cv.threshold(leftEye, 90, 255, cv.THRESH_BINARY_INV)  
    Lcontours, Lhierarchy = cv.findContours(Lthresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    Lcontours = sorted(Lcontours, key=lambda x: cv.contourArea(x), reverse=True)

    #lines locating pupils
    for cnt in Lcontours:
      (x,y,w,h) = cv.boundingRect(cnt)
      x=x+xmin
      y=y+ymin

      cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
      cv.line(frame, (x + int(w/2), y + int(h/2) + 50), (x + int(w/2), y + int(h/2) - 50), (0, 255, 0), 1)
      cv.line(frame, (x + int(w/2) + 50, y + int(h/2)), (x + int(w/2) - 50, y + int(h/2)), (0, 255, 0), 1)
      break

    #Right Eye
    Reye = np.array([(landmarks.part(42).x, landmarks.part(42).y),
                            (landmarks.part(43).x, landmarks.part(43).y),
                            (landmarks.part(44).x, landmarks.part(44).y),
                            (landmarks.part(45).x, landmarks.part(45).y),
                            (landmarks.part(46).x, landmarks.part(46).y),
                            (landmarks.part(47).x, landmarks.part(47).y)], np.int32)

    xmax=max(Reye[0][0], Reye[1][0], Reye[2][0], Reye[3][0], Reye[4][0], Reye[5][0])
    xmin=min(Reye[0][0], Reye[1][0], Reye[2][0], Reye[3][0], Reye[4][0], Reye[5][0])
    ymax=max(Reye[0][1], Reye[1][1], Reye[2][1], Reye[3][1], Reye[4][1], Reye[5][1])
    ymin=min(Reye[0][1], Reye[1][1], Reye[2][1], Reye[3][1], Reye[4][1], Reye[5][1])
    

    rightEye= frame [ymin:ymax,xmin:xmax]
    rightEye = cv.cvtColor(rightEye, cv.COLOR_BGR2GRAY)
    rightEye = cv.GaussianBlur(rightEye, (5,5), 0)

    Rret, Rthresh= cv.threshold(rightEye, 90, 255, cv.THRESH_BINARY_INV)  
    Rcontours, Rhierarchy = cv.findContours(Rthresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    Rcontours = sorted(Rcontours, key=lambda x: cv.contourArea(x), reverse=True)

    #lines locating pupils
    for cnt in Rcontours:
      (x,y,w,h) = cv.boundingRect(cnt)
      x=x+xmin
      y=y+ymin
      rows, cols, _= frame.shape

      cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
      cv.line(frame, (x + int(w/2), y + int(h/2) + 50), (x + int(w/2), y + int(h/2) - 50), (0, 255, 0), 1)
      cv.line(frame, (x + int(w/2) + 50, y + int(h/2)), (x + int(w/2) - 50, y + int(h/2)), (0, 255, 0), 1)
      break
    
    h, w = Lthresh.shape
    h1, w1 = Rthresh.shape
    cv.polylines(frame, [Leye], True, (0,0,255), 1) 
    cv.polylines(frame, [Reye], True, (0,0,255), 1)
    cv.imshow("Left Threshold", cv.resize(Lthresh, (2*w, 2*h)))
    cv.imshow("Right Threshold", cv.resize(Rthresh, (2*w1, 2*h1)))
   
  cv.imshow("Frame",  frame)

  key = cv.waitKey(1)
  if key == 32: #space bar to exit
    break 

cap.release()
cv.destroyAllWindows()