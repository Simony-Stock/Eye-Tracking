import csv
import pandas as pd
import numpy as np
import os

inputFileName = "Eye Test 2";
outputFileName = inputFileName +"fix";

#AOI_val = '1'

path_parent = os.path.dirname(os.getcwd()) #gets the path to one directory up
os.chdir(path_parent) #changes working directory to path_parent

#Read CSV file into DataFrame df
df = pd.read_csv(inputFileName+'.csv')
    
leftXThreshold = 0 #threshold value for the x coordinate of left eye
leftXMINThreshold = -0.2 #threshold value for the extreme x coordinate of left eye
leftXMAXThreshold = 0.3

rightXThreshold = 0 #threshold value for the x coordinate of right eye
rightXMINThreshold = -0.2 #threshold value for the extreme minumum x coordinate of right eye
rightXMAXThreshold = 0.3 #threshold value for the extreme maximum x coordinate of right eye

leftYThreshold = 20 #threshold value for theshold height of the eye between upper and lower
leftYMINThreshold = 15 #threshold value for the extreme minimum y height of left eye
leftYMAXThreshold = 27 #threshold value for the extreme maximum y height of left eye

rightYThreshold = 23 #threshold value for theshold height of the eye between upper and lower
rightYMINThreshold = 15 #threshold value for the extreme minimum y height of right eye
rightYMAXThreshold = 27 #threshold value for the extreme maximum y height of right eye

#function that checks if the value in the spcified column of the CSV is greater than the desired threshold value
#this will corespond with looking in the left half of the screen
#2 - LEFT half of the screen, 1- RIGHT half of the screen, 0- NEITHER or UNKNOWN
def findCol(left, right):
    #set variables-----------------------------------------------------------------------------------------
    LisCol0 = df[left] != np.empty 
    #converting the df left column into a series to apply the series.between function to compare < and > simulataneously
    leftcol = df[left].squeeze()
    LisCol1 = leftcol.between(leftXThreshold, leftXMAXThreshold, inclusive="neither")
    LisCol2 = leftcol.between(leftXMINThreshold, leftXThreshold, inclusive="neither") #creates boolean column of T/F based on right X value


    RisCol0 = df[right] != np.empty
    #converting the df right column into a series to apply the series.between function to compare < and > simulataneously
    rightcol = df[right].squeeze() 
    RisCol1 = rightcol.between(rightXThreshold, rightXMAXThreshold, inclusive="neither")
    RisCol2 = rightcol.between(rightXMINThreshold, rightXThreshold, inclusive="neither") #creates boolean column of T/F based on right X value


    #name columns------------------------------------------------------------------------------------------
    df.loc[LisCol0, 'Lcolumn'] = 0 #sets all non empty cels to 0
    df.loc[LisCol1, 'Lcolumn'] = 1 #adds in col=1 - left half screen
    df.loc[LisCol2, 'Lcolumn'] = 2 #adds in col=2 - right half screen

    df.loc[RisCol0, 'Rcolumn'] = 0 #sets all non empty cells to 0
    df.loc[RisCol1, 'Rcolumn'] = 1 #adds in col=1 - left half screen
    df.loc[RisCol2, 'Rcolumn'] = 2 #adds in col=2 - right half screen

#function to identify the row (upper or lower) that the eye is gazing based on the height of the eye itself
#1 - UPPER half of the screen, 2- LOWER half of the screen, 0- NEITHER or UNKNOWN
def findRow(lefth, righth):
    #set variables-----------------------------------------------------------------------------------------
    LisRow0 = df[lefth] != np.empty 
    #converting the df left column into a series to apply the series.between function to compare < and > simulataneously
    leftrow = df[lefth].squeeze()
    LisRow1 = leftrow.between(leftYThreshold, leftYMAXThreshold, inclusive="neither")
    LisRow2 = leftrow.between(leftYMINThreshold, leftYThreshold, inclusive="neither") #creates boolean column of T/F based on left Y value

    RisRow0 = df[righth] != np.empty
    #converting the df right column into a series to apply the series.between function to compare < and > simulataneously
    rightrow = df[righth].squeeze() 
    RisRow1 = rightrow.between(rightYThreshold, rightYMAXThreshold, inclusive="neither")
    RisRow2 = rightrow.between(rightYMINThreshold, rightYThreshold, inclusive="neither") #creates boolean column of T/F based on right Y value


    #name columns------------------------------------------------------------------------------------------
    df.loc[LisRow0, 'Lrow'] = 0 #sets all non empty cells to 0
    df.loc[LisRow1, 'Lrow'] = 1 #adds in col=1 - upper half of screen
    df.loc[LisRow2, 'Lrow'] = 2 #adds in col=2 - lower half of screen


    df.loc[RisRow0, 'Rrow'] = 0 #sets all non empty cells to 0
    df.loc[RisRow1, 'Rrow'] = 1 #adds in col=1 - upper half of screen
    df.loc[RisRow2, 'Rrow'] = 2 #adds in col=2 - lower half of screen


findCol('Left X', 'Right X') #sets the column array
findRow('Left Height','Right Height') #sets the row array

#function to identify the AOI (quadrant) based on the row and column caluclated by the findCol and findRow functions

#change the value of AOI variable based on the value of left x and left y
#df.loc[isLeft('Left X'), 'AOI'] = 12; #AOI set to 122 if X and Y value is positive

# Show the loaded and edited data from the dataframe in the terminal
print(df)

#print the updated Dataframe to the output csv file
df.to_csv(outputFileName+'.csv')
