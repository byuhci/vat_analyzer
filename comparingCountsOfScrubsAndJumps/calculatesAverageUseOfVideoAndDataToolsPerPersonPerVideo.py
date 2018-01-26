import csv
from collections import namedtuple, defaultdict
import matplotlib.pyplot as plt
import numpy as np
# from pandas import DataFrame
import pandas as pd
import scipy.stats

recordedTallys= namedtuple('recordedTallys', ['task','user','START','ENDdata','ENDvideo','SELECT','DESELECT','DESELECTdata','CHANGEEVENTTYPE','CANCEL','DELETE','MOVE','MOVEextent','RESIZE','RESIZEextent','JUMPdata','JUMPvideo','SCRUBdata','SCRUBvideo','SCRUBvideoExtent','PLAY','PAUSE','CHANGEPLAYBACKRATE','SKIP','PEEK','STUDY_NAME','HIDDEN'])

# task	user	START	END.data	END.video	SELECT	DESELECT	DESELECT.data
# CHANGE-EVENT-TYPE	CANCEL	DELETE	MOVE	MOVE.extent	RESIZE	RESIZE.extent	JUMP.data
# JUMP.video	SCRUB.data	SCRUB.video	SCRUB.video.extent
# PLAY	PAUSE	CHANGE-PLAYBACK-RATE	SKIP	PEEK	STUDY_NAME

def readInCSV():
    # futureGraphs = defaultdict(list)
    with open('fromLawrenceJumpScrubs_withHiddenValue.csv') as f:
        data = list(csv.reader(f, delimiter=','))
    toBeGraphed = []
    for item in data:
        # print(item)
        if not item[0][:3] == 'pra': # NOTE: this ignores all practice rounds
            # print(item[0][:3])
            toBeGraphed.append(recordedTallys(task=item[0], user=item[1],START=item[2],ENDdata=item[3],ENDvideo=item[4],SELECT=item[5],DESELECT=item[6],
                    DESELECTdata=item[7],CHANGEEVENTTYPE=item[8],CANCEL=item[9],DELETE=item[10],MOVE=item[11],MOVEextent=item[12],
                    RESIZE=item[13],RESIZEextent=item[14],JUMPdata=item[15],JUMPvideo=item[16],SCRUBdata=item[17],
                    SCRUBvideo=item[18],SCRUBvideoExtent=item[19],PLAY=item[20],PAUSE=item[21],CHANGEPLAYBACKRATE=item[22],
                    SKIP=item[23],PEEK=item[24],STUDY_NAME=item[25],HIDDEN=item[26]))

    return toBeGraphed

def mapOfData(dataFromCSV, eventsBeingConsidered):
    dataOfEvents= defaultdict(list)
    for measurableEvent in eventsBeingConsidered:
        for item in dataFromCSV:
            pillsOrRun = getattr(item, 'task')
            firstThing = getattr(item, measurableEvent)
            hiddenValue = getattr(item, 'HIDDEN')
            # print(hiddenValue)
            #  note that this [:3] puts all 'run-' and all 'pill' into one key
            # print(pillsOrRun[:3],measurableEvent)
            if hiddenValue == 'none':
                dataOfEvents[measurableEvent,hiddenValue].append(float(firstThing)) # to separate pills and run, use this: # pillsOrRun[:3],
    # print(dataOfEvents)
    print(len(dataOfEvents))
    return dataOfEvents

def makeCSVwithAveragesDataVsVideo(toBeAveraged, dataOrVideo, nameOfDataOrVideo):
    overallData = {}
    # print(toBeAveraged)
    for key, values in toBeAveraged.items():
        # print(key, values)
        sum = 0
        count = 0
        avg = 0
        for value in values:
             sum += value
             count += 1
        avg = sum/count
        overallData[key] = (sum, count, avg)
    # print(overallData) # shows the averages
    lenDataOrVideo = len(dataOrVideo)
    with open(str(lenDataOrVideo) + nameOfDataOrVideo + '.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        row = [nameOfDataOrVideo + 'THINGS:']
        row.extend(dataOrVideo)
        csvwriter.writerow(row)
        row = []
        for item in overallData:
            # print(item, overallData[item])
            row.extend(item)
            row.extend(overallData[item])
            csvwriter.writerow(row)
            row = []

def boxAndWhiskerIt(toBeAveraged, vidOrDat):
    # print(toBeAveraged)
    for graph, points in toBeAveraged.items():
        plt.figure()
        plt.boxplot(points, 0, 'gD')
        plt.title(graph)

        print(graph[0])
        title = graph[0]+'hidden-' +graph[1]

        plt.savefig('comparingVideoToolUsageToData/' + vidOrDat + title + '.png')

def describeTheData(toBeAveraged, vidOrDat):
    # print(s.describe())
    f = open('comparingVideoToolUsageToData/' + vidOrDat + 'DataDescribeOutput.txt', 'w')
    f.write(vidOrDat)
    for graph, points in toBeAveraged.items():
        s = pd.Series(points)
        f.write(str(graph))
        f.write('\n')
        f.write(str(s.describe()))
        #print(s.describe())
        f.write('\n\n')
    f.close()

def isItNormal(toBeAveraged, vidOrDat):
    # print("hi")
    f = open('comparingVideoToolUsageToData/' + vidOrDat + 'NormalizationVideoToolVsData.txt', 'w')
    f.write(vidOrDat)
    for graph, points in toBeAveraged.items():
        f.write(str(graph))
        if sum(points) == 0:
            f.write("sum of all values is zero")
            f.write('\n')
            continue
        f.write(str(scipy.stats.mstats.normaltest(points)))
        f.write('\n')

dataFromCSV = readInCSV()

dataThings = ['ENDdata','DESELECTdata','MOVE','RESIZE','JUMPdata','SCRUBdata',]
videoThings = ['ENDvideo','JUMPvideo','SCRUBvideo','PLAY','PAUSE','CHANGEPLAYBACKRATE','SKIP']

toBeAveragedData = mapOfData(dataFromCSV, dataThings)
makeCSVwithAveragesDataVsVideo(toBeAveragedData, dataThings, 'data')

toBeAveragedVideo = mapOfData(dataFromCSV, videoThings)
makeCSVwithAveragesDataVsVideo(toBeAveragedVideo, videoThings, 'video')

# boxAndWhiskerIt(toBeAveragedData, 'data') # bo&whisker
# boxAndWhiskerIt(toBeAveragedVideo, 'video') # bo&whisker

# describeTheData(toBeAveragedData, 'data') # count, mean, std, mean, 25, 50, 75, max, dtype
# describeTheData(toBeAveragedVideo, 'video') # count, mean, std, mean, 25, 50, 75, max, dtype

isItNormal(toBeAveragedData, 'data') # normalization spread
isItNormal(toBeAveragedVideo, 'video') # normalization spread
