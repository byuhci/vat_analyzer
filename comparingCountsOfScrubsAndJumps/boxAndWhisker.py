import csv
from collections import namedtuple, defaultdict
import plotly.plotly as py
import plotly.graph_objs as go

recordedTallys= namedtuple('recordedTallys', ['task','user','START','ENDdata','ENDvideo','SELECT','DESELECT','DESELECTdata','CHANGEEVENTTYPE','CANCEL','DELETE','MOVE','MOVEextent','RESIZE','RESIZEextent','JUMPdata','JUMPvideo','SCRUBdata','SCRUBvideo','SCRUBvideoExtent','PLAY','PAUSE','CHANGEPLAYBACKRATE','SKIP','PEEK','STUDY_NAME'])

# task	user	START	END.data	END.video	SELECT	DESELECT	DESELECT.data
# CHANGE-EVENT-TYPE	CANCEL	DELETE	MOVE	MOVE.extent	RESIZE	RESIZE.extent	JUMP.data
# JUMP.video	SCRUB.data	SCRUB.video	SCRUB.video.extent
# PLAY	PAUSE	CHANGE-PLAYBACK-RATE	SKIP	PEEK	STUDY_NAME

def readInCSV():
    # futureGraphs = defaultdict(list)
    with open('jumpsScrubs.csv') as f:
        data = list(csv.reader(f, delimiter=','))
    toBeGraphed = []
    for item in data:
        # print(item)
        if not item[0][:3] == 'pra':
            # print(item[0][:3])
            toBeGraphed.append(recordedTallys(task=item[0], user=item[1],START=item[2],ENDdata=item[3],ENDvideo=item[4],SELECT=item[5],DESELECT=item[6],
                    DESELECTdata=item[7],CHANGEEVENTTYPE=item[8],CANCEL=item[9],DELETE=item[10],MOVE=item[11],MOVEextent=item[12],
                    RESIZE=item[13],RESIZEextent=item[14],JUMPdata=item[15],JUMPvideo=item[16],SCRUBdata=item[17],
                    SCRUBvideo=item[18],SCRUBvideoExtent=item[19],PLAY=item[20],PAUSE=item[21],CHANGEPLAYBACKRATE=item[22],
                    SKIP=item[23],PEEK=item[24],STUDY_NAME=item[25]))

    return toBeGraphed

def mapOfData(dataFromCSV, desiredSubjectOfPlot, secondDesire):
    firstPlot = defaultdict(list)
    secondPlot = defaultdict(list)
    task = 'task'
    for item in dataFromCSV:
        pillsOrRun = getattr(item, task)
        # print(pillsOrRun)
        firstThing = getattr(item, desiredSubjectOfPlot)
        # print(firstThing)
        secondThing = getattr(item, secondDesire)
        # print(secondThing)
        firstPlot[pillsOrRun, desiredSubjectOfPlot].append(float(firstThing))
        # print(firstPlot)
        secondPlot[pillsOrRun, secondDesire].append(float(secondThing))
    # print(firstPlot)
    return firstPlot, secondPlot

def makeTwoBoxAndWhiskers(toBeBoxAndWhiskered):
    graphOne, graphTwo = toBeBoxAndWhiskered


    # data = [
    #     go.Box(
    #         y=[0, 1, 1, 2, 3, 5, 8, 13, 21],
    #         boxpoints='all',
    #         jitter=0.3,
    #         pointpos=-1.8
    #     )
    # ]
    # py.iplot(data)


dataFromCSV = readInCSV()
toBeBoxAndWhiskered = mapOfData(dataFromCSV, 'SCRUBvideo', 'SCRUBdata')
makeTwoBoxAndWhiskers(toBeBoxAndWhiskered)


