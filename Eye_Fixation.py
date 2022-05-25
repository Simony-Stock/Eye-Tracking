import csv
import pandas as pd
import numpy as np
import os

inputFileName = "Test1";
outputFileName = inputFileName +"fix";
column = 0
row = 0

#AOI_val = '1'

path_parent = os.path.dirname(os.getcwd()) #gets the path to one directory up
os.chdir(path_parent) #changes working directory to path_parent

#Read CSV file into DataFrame df
df = pd.read_csv(inputFileName+'.csv')
    
leftXThreshold = 0; #threshold value for the x coordinate of left eye

#function that checks if the value in the spcified column of the CSV is greater than the desired threshold value
#this will corespond with looking in the left half of the screen
def isLeft(text):
    a = df[text] < leftXThreshold
    #change value of column to left (1) if value is less than threshold
    df.loc[a, 'column'] = 1; #edits the value in the new column to 1 based on the above condition
    #change value of column to right (2) if value is greater than threshold
    a = df[text] > leftXThreshold
    df.loc[a, 'column'] = 2; #edits the value in the new column to 2 based on the above condition



print(isLeft('Left X')) # output of condition is a series of boolean (T/F) statements with a length equal to the number of rows 

#change the value of AOI variable based on the value of left x and left y
#df.loc[isLeft('Left X'), 'AOI'] = 12; #AOI set to 122 if X and Y value is positive

# Show the loaded and edited data from the dataframe in the terminal
print(df)

#print the updated Dataframe to the output csv file
df.to_csv(outputFileName+'.csv')




#edit a value in the csv file 
    #df.loc[row_label, column name] = new_value
    
#changes the value in the second row of data (0, 1) and the 4th column (header, 0, 1, 2, 3, 4)
#df.iloc[1, 4] = 12 

#using pandas

#pd.read_csv('Sample CSV File - Sheet1.csv', delimiter = ',')


#with open ('Sample CSV File - Sheet1.csv', 'a') as f: #csv file openned in append mode to make changes
#    df.to_csv(f, mode='a', header=False)

#    input_data = pd.read_csv(file) #import the csv file for reading
#df.tp_csv(f, header = False)
#for row in input_data:
#input_data= input_data[['Left X','Left Y','Right X','Right Y','Time','AOI']]
#input_data["AOI"] = AOI_val #change the value in the AOI column of every row in the csv file
#input_data.to_cvs('Sample CSV File - Sheet1.csv') #writing to the csv file