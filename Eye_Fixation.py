import pandas as pd
import numpy as np
import os
from scipy.stats import mode

inputFileName = "test";
outputFileName = inputFileName +"fix";


path_parent = os.path.dirname(os.getcwd()) #gets the path to one directory up
os.chdir(path_parent) #changes working directory to path_parent

#Read CSV file into DataFrame df
df = pd.read_csv(inputFileName+'.csv')
    
leftXThreshold = 0 #threshold value for the x coordinate of left eye #changed this 
leftXMINThreshold = -0.4 #threshold value for the extreme x coordinate of left eye
leftXMAXThreshold = 0.3 #threshold value for the extreme maximum x coordinate of left eye

rightXThreshold = 0 #threshold value for the x coordinate of right eye
rightXMINThreshold = -0.4 #threshold value for the extreme minumum x coordinate of right eye
rightXMAXThreshold = 0.3 #threshold value for the extreme maximum x coordinate of right eye

leftYThreshold = 0.297 #threshold value for theshold height of the eye between upper and lower
leftYMINThreshold = 0.2 #threshold value for the extreme minimum y height of left eye
leftYMAXThreshold = 0.35 #threshold value for the extreme maximum y height of left eye

rightYThreshold = 0.297 #threshold value for theshold height of the eye between upper and lower
rightYMINThreshold = 0.2 #threshold value for the extreme minimum y height of right eye
rightYMAXThreshold = 0.35 #threshold value for the extreme maximum y height of right eye

#function that checks if the value in the spcified column of the CSV is greater than the desired threshold value
#this will corespond with looking in the left half of the screen
#2 - LEFT half of the screen, 1- RIGHT half of the screen, 0- NEITHER or UNKNOWN
def findCol(left, right):
    #set variables-----------------------------------------------------------------------------------------
    LisCol0 = df[left] != np.empty
    #converting the df left column into a series to apply the series.between function to compare < and > simulataneously
    leftcol = df[left].squeeze()
    LisCol1 = leftcol.between(leftXThreshold, leftXMAXThreshold, inclusive="neither") #creates boolean column based on right X value (left)
    LisCol2 = leftcol.between(leftXMINThreshold, leftXThreshold, inclusive="neither") #creates boolean column based on right X value (right)

    RisCol0 = df[right] != np.empty
    #converting the df right column into a series to apply the series.between function to compare < and > simulataneously
    rightcol = df[right].squeeze() 
    RisCol1 = rightcol.between(rightXThreshold, rightXMAXThreshold, inclusive="neither") #creates boolean column based on left X value (left)
    RisCol2 = rightcol.between(rightXMINThreshold, rightXThreshold, inclusive="neither") #creates boolean column based on right X value (right)


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
    LisRow1 = leftrow.between(leftYThreshold, leftYMAXThreshold, inclusive="neither")  #creates boolean column based on left Y value (upper)
    LisRow2 = leftrow.between(leftYMINThreshold, leftYThreshold, inclusive="neither") #creates boolean column based on left Y value (lower)

    RisRow0 = df[righth] != np.empty
    #converting the df right column into a series to apply the series.between function to compare < and > simulataneously
    rightrow = df[righth].squeeze() 
    RisRow1 = rightrow.between(rightYThreshold, rightYMAXThreshold, inclusive="neither") #creates boolean column of based on right Y value (upper)
    RisRow2 = rightrow.between(rightYMINThreshold, rightYThreshold, inclusive="neither") #creates boolean column of based on right Y value (lower)


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
#Any row with the column and row within the left and right eye that are not equal will be removed and AOI set to 0
def AOIid(LeftCol, RightCol, LeftRow, RightRow, Time):
    #condition setup-----------------------------------------------------------------------------------------------
    timeEqualZero = (df[Time] == 0) #AOI will be 0 if timestamp is equal to zero to remove error points
    timeLessThan5 = (df[Time] < 5000 ) #remove points before 5 seconds
    timeMoreThan5 = (df[Time].index > (len(df.index)-131)) #remove points 5 second from the end of the video using a negative indexed numpy array    
    colunEqual = (df[LeftCol] != df[RightCol]) #left and right column unequal
    rowunEqual = (df[LeftRow] != df[RightRow]) #left and right row unequal

    condition1 = ((df[LeftCol] == 1) & (df[LeftRow] == 1)) #quadrant 1, upper left conditon
    condition2 = ((df[LeftCol] == 2) & (df[LeftRow] == 1)) #quadrant 2, upper right conditon
    condition3 = ((df[LeftCol] == 1) & (df[LeftRow] == 2)) #quadrant 3, lower left conditon
    condition4 = ((df[LeftCol] == 2) & (df[LeftRow] == 2)) #quadrant 4, lower right conditon

    #conditional statement for AOI column
    df['AOI'] = np.select([timeMoreThan5, timeLessThan5, timeEqualZero, colunEqual, rowunEqual, condition1, condition2, condition3, condition4], [0,0,0,0,0,1, 2, 3, 4], default=0)

AOIid('Lcolumn', 'Rcolumn', 'Lrow', 'Rrow', 'Timestamp') #change the value of AOI column based on the value of row and column

df.to_csv(outputFileName+'.csv') #print the updated Dataframe to the output csv file


#function to identify areas of fixation by averaging the identified AOIs while removing any 0 terms
def eyeFixation (LeftCol, RightCol, LeftRow, RightRow, Time, AOI):
    df.drop(df[df[AOI] == 0].index, inplace=True) #remove rows with 0 AOI to calculate the fixation averages
    
    #determine the mode of evergy 3 rows of df  
    fixation =df.groupby(np.arange(len(df)) // 3)[Time, AOI].apply(lambda x: x.mode()) #groups
    fixation.to_csv(outputFileName+'It1.csv') #print the updated Dataframe to the output csv file
    
    #second iteration taking the mode of every 3 again to determine fixation points and relative time
    df1 = pd.read_csv(outputFileName+'It1.csv') #create a fixation dataframe for using the mode of the first

    df1= df1.dropna() #remove rows with NAN AOI to calculate the 1/3 the data set, leaving the fixation averages

    fixation1 = df1.groupby(np.arange(len(df1)) // 3)[Time, AOI].apply(lambda x: x.mode()) #groups the data into sets of 3 and calculates the mode of the AOI 
    fixation1= fixation1.dropna() #remove rows with NAN AOI to calculate the 1/3 the data set, leaving the fixation averages
    fixation1.to_csv(outputFileName+'It2.csv') #print the updated Dataframe to the output csv file to display areas of fixation

    print(fixation1) #print identified areas of eye fixation and timing

eyeFixation('Lcolumn', 'Rcolumn', 'Lrow', 'Rrow', 'Timestamp', 'AOI')