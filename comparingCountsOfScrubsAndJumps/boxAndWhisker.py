import csv
from collections import namedtuple, defaultdict
import matplotlib.pyplot as plt
import numpy as np

recordedTallys= namedtuple('recordedTallys', ['task','user','START','ENDdata','ENDvideo','SELECT','DESELECT','DESELECTdata','CHANGEEVENTTYPE','CANCEL','DELETE','MOVE','MOVEextent','RESIZE','RESIZEextent','JUMPdata','JUMPvideo','SCRUBdata','SCRUBvideo','SCRUBvideoExtent','PLAY','PAUSE','CHANGEPLAYBACKRATE','SKIP','PEEK','STUDY_NAME'])

# task	user	START	END.data	END.video	SELECT	DESELECT	DESELECT.data
# CHANGE-EVENT-TYPE	CANCEL	DELETE	MOVE	MOVE.extent	RESIZE	RESIZE.extent	JUMP.data
# JUMP.video	SCRUB.data	SCRUB.video	SCRUB.video.extent
# PLAY	PAUSE	CHANGE-PLAYBACK-RATE	SKIP	PEEK	STUDY_NAME

def readInCSV():
    # futureGraphs = defaultdict(list)
    with open('fromLawrencejumpsScrubs_withHiddenValues.csv') as f:
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
                    SKIP=item[23],PEEK=item[24],STUDY_NAME=item[25]))

    return toBeGraphed

def mapOfData(dataFromCSV, eventsBeingConsidered):
    dataOfEvents= defaultdict(list)
    for measurableEvent in eventsBeingConsidered:
        for item in dataFromCSV:
            pillsOrRun = getattr(item, 'task')
            firstThing = getattr(item, measurableEvent)
            # print(firstThing)
            #  note that this [:3] puts all 'run-' and all 'pill' into one key
            # print(pillsOrRun[:3],measurableEvent)
            dataOfEvents[pillsOrRun[:3],measurableEvent].append(float(firstThing))
    # print(dataOfEvents)
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
    print(overallData)
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



dataFromCSV = readInCSV()

dataThings = ['ENDdata','DESELECTdata','MOVE','RESIZE','JUMPdata','SCRUBdata',]
videoThings = ['ENDvideo','JUMPvideo','SCRUBvideo','PLAY','PAUSE','CHANGEPLAYBACKRATE','SKIP']

toBeAveraged = mapOfData(dataFromCSV, dataThings)
makeCSVwithAveragesDataVsVideo(toBeAveraged, dataThings, 'data')

toBeAveraged = mapOfData(dataFromCSV, videoThings)
makeCSVwithAveragesDataVsVideo(toBeAveraged, videoThings, 'video')

