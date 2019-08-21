import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import sys
inFile = sys.argv[1]
shell=True
import subprocess

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("testSheets-6d40363997eb.json", scope)

client = gspread.authorize(creds)

sheet = client.open("testus").sheet1  # Open the spreadhseet

data = sheet.get_all_records() #this will show to us all data
numRows = len(data) +2#that how we gonna find last column
#numRows = sheet.row_count #this is len of all columns
stroka = sys.argv[1].rsplit('/')

for i in range(len(stroka)):
   i+1
sheet.update_cell(numRows,1,stroka[i])
import subprocess
out = subprocess.Popen(['wc', '-l',sys.argv[1]], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
stdout,stderr = out.communicate()
stroka = stdout.rsplit(' ')
sheet.update_cell(numRows,3,stroka[0])
subprocess.call("/home/hudson/workspace/JULIAN/split_csv_hash_salt.sh -f" + sys.argv[1], shell=True)

algo = raw_input("Please enter alghoritm\n")

if algo == "n":
    sheet.update_cell(numRows,2,"UNKNOWN")
elif algo == "s":
    sheet.update_cell(numRows,2,"SPECIAL")
else:
    sheet.update_cell(numRows,2,algo)



import subprocess
new = sys.argv[1]
new = stdout.rsplit('.txt')
new2 = '_originalfields.txt'
new3 = new[0] + new2
out = subprocess.Popen(['wc', '-l', new3], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
stdout,stderr = out.communicate()
stroka = stdout.rsplit(' ')
sheet.update_cell(numRows,4,stroka[1])
print(stroka[1])
#print(stdout)
#print (output) 