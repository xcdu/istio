import csv
'''
cover = []
with open('test.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        cover.append(row[0])
print(cover)
'''

import os.path
from os import path
if path.exists("post2.csv"):
    with open("post.csv", "r") as lastFile:
        postID = list(csv.reader(lastFile))[-1][0]
        print("not empty")
else:
    postID = 0
    print("empty")