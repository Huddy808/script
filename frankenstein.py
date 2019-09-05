import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import sys
inFile = sys.argv[1]
shell=True
import subprocess
import datetime
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("testSheets-6d40363997eb.json", scope)

client = gspread.authorize(creds)

sheet = client.open("processing_test").sheet1  # Open the spreadhseet

data = sheet.get_all_records() #this will show to us all data
numRows = len(data) +2#that how we gonna find last column
starter = str(sys.argv[1])

if starter.find("originalfields") == -1 and starter.find("__.txt")== -1:
    line = sys.argv[1].rsplit('/') 
    for i in range(len(line)):
        i+1

    sheet.update_cell(numRows,2,line[i])
    
    line2 = line[i].rsplit('_')
    sheet.update_cell(numRows,1,line2[0])
    import subprocess
    out = subprocess.Popen(['wc', '-l',sys.argv[1]], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    stroka = stdout.rsplit(' ')

    sheet.update_cell(numRows,4,stroka[0])
    subprocess.call("split_csv_hash_salt.sh -f" + sys.argv[1], shell=True)

    algo = raw_input("Please enter alghoritm ('n'-Unknown; 's'-Special; 'p' -plaintext)\n")

    if algo == "n":
        sheet.update_cell(numRows,3,"UNKNOWN")
    elif algo == "s":
        sheet.update_cell(numRows,3,"SPECIAL")
    elif algo == "p":
        sheet.update_cell(numRows,3,"PLAINTEXT")
    else:
        sheet.update_cell(numRows,3,algo)



    import subprocess
    new = str(sys.argv[1])
    new = stdout.rsplit('.txt')
    new2 = '_originalfields.txt'
#new3 = new[0] + new2
    out = subprocess.Popen( ['wc', '-l', new[0] + new2, '~/PROCESSED/UNKNOWN/'],
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    stroka = stdout.rsplit(' ')
    stroka2= stroka[1].rsplit('\'') 
    sheet.update_cell(numRows,5,stroka2[1])
    sheet.update_cell(numRows, 6, datetime.datetime.now().strftime('%Y-%m-%d'))
    #sheet.delete_rows(numRows - 1, 7)
    #sheet.delete_rows(numRows - 1, 8)
    #sheet.delete_rows(numRows - 1, 9)
    #sheet.delete_rows(numRows - 1, 10)
    q = int(numRows) -1
    sheet.update_cell(numRows, 7, "TOTAL FILES")
    sheet.update_cell(numRows, 8, numRows - 1)
    sheet.update_cell(numRows, 9, "TOTAL STRINGS")
    sheet.update_cell(numRows, 10, ('=SUM(E2:E%d)' %(numRows))) 
    sheet.update_cell(q, 7, "")
    sheet.update_cell(q, 8, "")
    sheet.update_cell(q, 9, "")
    sheet.update_cell(q, 10, "")


#print(stroka[1])
#print(stdout)
#print (output) 
