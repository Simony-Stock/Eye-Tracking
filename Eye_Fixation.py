import csv
from csv import writer
from csv import reader
import pandas as pd
#with open('Sample CSV File - Sheet1.csv') as inputData:
#    reader = csv.reader(inputData) #to read csv file
#
#    writer =  csv.writer(inputData) #to write to a set csv file
#    for row in reader:
#        print(row)

#function for adding entry at end of CSV designated the identified AOI being looked at
def add_col_in_CSV(input_csv, output_csv):
    with open(input_csv, 'r') as input_val,\
            open(output_csv, 'w', newline='') as output_val:
        # CSV reader object - where data will be read
        csv_reader = reader(input_val)
        # CSV writer object for output - where data will be written
        csv_writer = writer(output_val)
        # For a loop reading the entries of the input csv
        
        for row in csv_reader:
            # add a column to each row of the csv
            if column[1] >0.5:
                row.append(12) 
            #transform_row(row, csv_reader.line_num)
            # the updated row is written to output csv
            csv_writer.writerow(row)


#with open('Sample CSV File - Sheet1.csv', 'r') as input_val:
#    csv_reader = reader(input_val)
#    for row in csv_reader: 
#        if (row in csv.reader < 0.3):
#            AOI_val = '2';
AOI_val = '2'



#add_col_in_CSV('Sample CSV File - Sheet1.csv', 'Output0.csv')