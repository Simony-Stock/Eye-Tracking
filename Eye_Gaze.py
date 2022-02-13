import cv2 as cv
import numpy as np
import dlib 
import os

cap = cv.VideoCapture(1) #camera 0->rear, 1->front
detector = dlib.get_frontal_face_detector() #build in detector to detect the 4 corner points of the face

file_name = "shape_predictor_68_face_landmarks.dat" #file with landmark data
path_parent = os.path.dirname(os.getcwd()) #gets the path to one directory up
os.chdir(path_parent) #changes working directory to path_parent this has to be done so that the next line can locate the landmark data file
predictor = dlib.shape_predictor(file_name) #predicts the facial landmark points 0 to 67



#midpoint calculation function
def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

while True:
  _, frame = cap.read() #front facing video
  gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #grayscale of frame video

  faces = detector(gray) #array of the 4 corner points on the face

  for face in faces:
    x, y = face.left(), face.top()
    x1, y1 = face.right(), face.bottom()
    cv.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

    #display all facial landparks
    landmarks = predictor(gray, face)
    for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv.circle(frame, (x, y), 1, (255, 0, 0), -1)
        
  cv.imshow("Frame", frame)

  key = cv.waitKey(1)
  if key == 32: #space bar to exit
    break 

cap.release()
cv.destroyAllWindows()