from time import strftime
import csv
from collections import defaultdict


def readInData():
    # subjectiveData.csv
    # saw	answer	questionNum	set of questions	QUESTION	task-type
    hasData = defaultdict(set)
    hasVideo = defaultdict(set)
    something = defaultdict(set)
    print(strftime("%Y-%m-%d %H:%M"))
    with open('subjectiveData.csv', 'r') as csvfile:
        allRows = csv.reader(csvfile, delimiter=',')  # , quotechar='|'
        for row in allRows:
            if row[0] == 'data':
                # print(row[1])
                # print(str(row[2:5]))
                hasData[str(row[2:5])].add(row[1])
            elif row[0] == 'video':
                hasVideo[str(row[2:5])].add(row[1])

    return hasData, hasVideo

def printRawData(hasData, hasVideo):
    for key, value in hasVideo.items():
        print(key, value)

hasData, hasVideo = readInData()
printRawData(hasData, hasVideo)