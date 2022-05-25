import csv
import pandas as pd
import numpy as np

inputFileName = "Test1";
outputFileName = inputFileName +"fix";
column = 0
row = 0

#AOI_val = '1'

#Read CSV file into DataFrame df
df = pd.read_csv(inputFileName+'.csv')
    
leftXThreshold = 0; #threshold value for the x coordinate of left eye

#function that checks if the value in the spcified column of the CSV is greater than the desired threshold value
def isLeft(text):
    return df[text] > leftXThreshold

print(isLeft('Left X')) # output of condition is a series of boolean (T/F) statements with a length equal to the number of rows 



#change the value of AOI variable based on the value of left x and left y
df.loc[isLeft('Left X'), 'AOI'] = 12; #AOI set to 122 if X and Y value is positive

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