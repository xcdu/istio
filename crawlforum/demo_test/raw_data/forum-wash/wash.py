import csv
#import pandas as pd
#df = pd.read_csv('template.csv', error_bad_lines=False)
#print(df)
# If you know the name of the column skip this
'''
first_column = df.columns[0]
# Delete first
df = df.drop([first_column], axis=1)
df.to_csv('template-wash1.csv', index=False)
'''
with open('template-wash1.csv', 'r') as csvfile, open('temp-wash2.csv', 'w') as output:
    writer = csv.writer(output)
    csvreader = csv.reader(csvfile)
    list=[]
    for index, value in enumerate(csvreader):
        if any(field.strip() for field in value):
            list.append(index)
    print(list)
            #writer.writerow(value)
'''

with open("template.csv","r") as source:
    rdr= csv.reader( source )
    with open("template-wash1.csv","w") as result:
        wtr= csv.writer( result )
        for r in rdr:
            del r[0]
            wtr.writerow( r )
'''