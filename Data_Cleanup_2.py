#!/usr/bin/env python
#Code by David Weinberger david_m_weinberger@whirlpool.com
#Last modified: 8/10/16

#Todo: add to specific folder (might be hard)
#Todo: Why are blank files getting passed - do an array element 1 check see if its blank?

import csv, glob, os.path, time
fileCount = 0
headers = ["a","b","c","d","e","f","g","h","i","j","k"] #column labels, Todo: give proper column names

def fileConvert(convFile, CSV_f):
    global fileCount
    raw_data = open(convFile,'r', newline='')
    reader = csv.reader(raw_data, delimiter='|', quoting=csv.QUOTE_NONE)

    for check in reader: #checks that data in file is good to write by seeing if it is building proper arrays for writing to CSV, if not exit subroutine 
        if (len(check) < 8) or (len(check) > 10): #9 is usual length, but last element may be 8 due to blank element at end of most lines
            print ("*Malformed data in {0}, cannot convert".format(convFile))
            return

    #if I do not close and open the file again it writes blank data, I do not know why it does this; problem only exists with the check in reader if statement    
    raw_data.close()
    raw_data = open(convFile,'r', newline='')
    reader = csv.reader(raw_data, delimiter='|', quoting=csv.QUOTE_NONE)

    CSV_data = open(CSV_f,'w', newline='')
    writer = csv.writer(CSV_data)
    
    writer.writerow(headers) #writes headers

    for row in reader: #itterates through each row, splits up date/time as unique CSV columns, splits up bracket element into separate elements (IDK what this columns name is)
        row[5:6] = row[5].split(" ")
        row[7:8] = row[7].split(" ")
        row[9:10] = row[9][1:-1].split(":") #removes the brackets and splits elements
        writer.writerow(row)

    raw_data.close()
    CSV_data.close()
    fileCount += 1
    print("{0} converted to CSV, see {1}".format(convFile, CSV_f))

for file in glob.glob("*.txt"):
    root_file = file[0:-4] #get root name of file without extension
    CSV_file = root_file + "CSV.csv"

    #fileConvert(file,CSV_file) #testing purposes
    if os.path.isfile(CSV_file) == False:
        fileConvert(file,CSV_file)
    elif os.path.getmtime(file) > os.path.getmtime(CSV_file): #due to odities in time system, it's backwards from what you would expect
        fileConvert(file,CSV_file)
    else:
        print("*" + file + " has already been converted, skipping")

input("\n {0} file(s) converted, press enter to close ".format(fileCount))
