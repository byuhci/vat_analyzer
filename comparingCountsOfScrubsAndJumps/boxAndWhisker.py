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
    with open('fromLawrencejumpsScrubs.csv') as f:
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

def mapOfData(dataFromCSV, desiredSubjectOfPlot, secondDesire):
    firstPlot = defaultdict(list)
    secondPlot = defaultdict(list)
    task = 'task'
    for item in dataFromCSV:
        pillsOrRun = getattr(item, task)
        firstThing = getattr(item, desiredSubjectOfPlot)
        secondThing = getattr(item, secondDesire)
        # print(pillsOrRun[:3])
        #  TODO: note that this [:3] puts all 'run-' and all 'pill' into one key
        firstPlot[pillsOrRun[:3], desiredSubjectOfPlot].append(float(firstThing))
        secondPlot[pillsOrRun[:3], secondDesire].append(float(secondThing))
    # print(firstPlot)
    return firstPlot, secondPlot

def makeTwoBoxAndWhiskers(toBeBoxAndWhiskered):
    # graphOne, graphTwo = toBeBoxAndWhiskered
    overallData = {}
    fileName1 = ""
    fileName2 = ""
    for graph in toBeBoxAndWhiskered:
        for key in graph:
            sum = 0
            count = 0
            avg = 0
            # print(key, graph[key])
            for value in graph[key]:
                sum += value
                count += 1
            avg = sum/count
            overallData[key] = (sum, count, avg)
            if fileName1 is "":
                fileName1 = key[1]
            if key[1] is not fileName1:
                fileName2 = key[1]
    print(fileName1 + 'Vs' + fileName2)
    with open(fileName1 + 'V' + fileName2 + '.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        row = []
        for item in overallData:
            print(item, overallData[item])
            row.extend(item)
            row.extend(overallData[item])
            csvwriter.writerow(row)

            # for key, value in averages.items():
            #     # print(key, value)
            #     row = [tempVar]
            #     row.extend(value)
            #     row.extend(key)
            #     # print(row)
            #     csvwriter.writerow(row)






dataFromCSV = readInCSV()
# JUMPdata, 'SCRUBvideo', 'SCRUBdata'
dataThings = ['SCRUBdata', 'JUMPdata']
videoThings = ['SCRUBvideo', 'JUMPvideo']
toBeBoxAndWhiskered = mapOfData(dataFromCSV, 'SCRUBvideo', 'SCRUBdata') # dataThings, videoThings

makeTwoBoxAndWhiskers(toBeBoxAndWhiskered)











# def fakeGraphs(toBeBoxAndWhiskered):
#     graphOne, graphTwo = toBeBoxAndWhiskered
#
#     for videoColor, desiredThing in graphOne, graphTwo:
#         # print(videoColor, desiredThing)
#         dataOneGraph = graphOne[videoColor, desiredThing]
#         # print(graphOne)
#
#         # all_data = [np.random.normal(0, std, 100) for std in range(1, 4)]
#         # print(all_data)
#         fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
#         # rectangular box plot
#         bplot1 = axes[0].boxplot(dataOneGraph,
#                                  vert=True,  # vertical box aligmnent
#                                  patch_artist=True)  # fill with color
#
#         dataTwoGraph = graphTwo[videoColor, desiredThing]
#         bplot2 = axes[1].boxplot(dataTwoGraph,
#                                  vert=True,  # vertical box aligmnent
#                                  patch_artist=True)  # fill with color
#         print(len(dataOneGraph), len(dataTwoGraph))
#
#         # fill with colors
#         colors = ['lightblue', 'lightgreen']
#         for bplot in (bplot1, bplot2):
#             for patch, color in zip(bplot['boxes'], colors):
#                 patch.set_facecolor(color)
#
#         # adding horizontal grid lines
#         for ax in axes:
#             ax.yaxis.grid(True)
#             ax.set_xticks([y + 1 for y in range(len(all_data))], )
#             ax.set_xlabel('xlabel')
#             ax.set_ylabel('ylabel')
#
#         # add x-tick labels
#         plt.setp(axes, xticks=[y + 1 for y in range(len(all_data))],
#                  xticklabels=['x1']) # , 'x2', 'x3', 'x4'
#         plt.title(videoColor) # desiredThing
#         plt.show()

