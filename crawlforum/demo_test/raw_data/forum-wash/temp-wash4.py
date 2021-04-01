
import re
import csv
#wash out non-standard templates
list=[]
counter=1
with open('temp-wash3.csv', 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        for field in row:
            if ('apiVersion:' in field) or ('kind:' in field):
                list.append(counter)
        counter=counter+1
res = [] 
for i in list: 
    if i not in res: 
        res.append(i) 
print(res)
        
with open('temp-wash3.csv', 'r') as csvfile, open('temp-wash4.csv', 'w') as output:
    writer = csv.writer(output)
    csvreader = csv.reader(csvfile)
    #row count starts 1 because i used 1 to form the list above
    row_count = 1
    
    for row in csvreader:
        if row_count in res:
            print(row_count)
            writer.writerow(row)
        row_count=row_count+1

with open('text-wash5.csv', 'r') as csvfile, open('text-wash6.csv', 'w') as output:
    writer = csv.writer(output)
    csvreader = csv.reader(csvfile)
    #row count starts 1 because i used 1 to form the list above
    row_count = 1
    
    for row in csvreader:
        if row_count in res:
            print(row_count)
            writer.writerow(row)
        row_count=row_count+1