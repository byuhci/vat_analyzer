import csv
from collections import namedtuple, defaultdict
import matplotlib.pyplot as plt
import numpy as np
# from pandas import DataFrame
import pandas as pd
import scipy.stats
from scipy.stats import mannwhitneyu


recordedTallys= namedtuple('recordedTallys', ['task','user','START','ENDdata','ENDvideo','SELECT','DESELECT','DESELECTdata','CHANGEEVENTTYPE','CANCEL','DELETE','MOVE','MOVEextent','RESIZE','RESIZEextent','JUMPdata','JUMPvideo','SCRUBdata','SCRUBvideo','SCRUBvideoExtent','PLAY','PAUSE','CHANGEPLAYBACKRATE','SKIP','PEEK','STUDY_NAME','HIDDEN'])

# task	user	START	END.data	END.video	SELECT	DESELECT	DESELECT.data
# CHANGE-EVENT-TYPE	CANCEL	DELETE	MOVE	MOVE.extent	RESIZE	RESIZE.extent	JUMP.data
# JUMP.video	SCRUB.data	SCRUB.video	SCRUB.video.extent
# PLAY	PAUSE	CHANGE-PLAYBACK-RATE	SKIP	PEEK	STUDY_NAME

def readInCSV():
    # futureGraphs = defaultdict(list)
    with open('fromLawrenceJumpScrubs_withHiddenValue_withFeb.csv') as f:
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
    # print(len(dataOfEvents))
    return dataOfEvents



def makeCSVwithAveragesDataVsVideo(toBeAveraged, dataOrVideo, nameOfDataOrVideo):
    overallData = {}
    # print(toBeAveraged)
    # print(str(dataOrVideo))
    for key, values in toBeAveraged.items():
        # print(key, values)
        sum = 0
        count = 0
        avg = 0
        for value in values:
             sum += value
             count += 1
        avg = sum/count
        # print(type(overallData))
        overallData[key[0], nameOfDataOrVideo] = (sum, count, avg)
    # print(overallData) # shows the averages
    lenDataOrVideo = len(dataOrVideo)
    with open('comparingVideoToolUsageToDataWithFeb/' + str(lenDataOrVideo) + nameOfDataOrVideo + 'WithFeb.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # row = [nameOfDataOrVideo + 'THINGS:']
        # row.extend(dataOrVideo)
        row = ['vidOrDataOrNeutral', 'eventType', 'hiddenValue', 'numTimesOccured', 'numOfVideos','avgNumTimesPerVideo']
        csvwriter.writerow(row)
        for item in overallData:
            # print(overallData[item][0])
            if overallData[item][1] == 0:
                continue
            row = [nameOfDataOrVideo]
            row.extend(item)
            row.extend(overallData[item])
            csvwriter.writerow(row)
    # print(overallData)
    return overallData

def boxAndWhiskerIt(toBeAveraged, vidOrDat):
    # print(toBeAveraged)
    for graph, points in toBeAveraged.items():
        plt.figure()
        plt.boxplot(points, 0, 'gD')
        plt.title(graph)

        # print(graph[0])
        title = graph[0]+'hidden-' +graph[1]

        plt.savefig('comparingVideoToolUsageToDataWithFeb/' + vidOrDat + title + '.pdf')

def describeTheData(toBeAveraged, vidOrDat):
    # print(s.describe())
    f = open('comparingVideoToolUsageToDataWithFeb/' + vidOrDat + 'DataDescribeOutputWithFeb.txt', 'w')
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
    f = open('comparingVideoToolUsageToDataWithFeb/' + vidOrDat + 'NormalizationVideoToolVsDataWithFeb.txt', 'w')
    f.write(vidOrDat)
    for graph, points in toBeAveraged.items():
        f.write(str(graph))
        if sum(points) == 0:
            f.write("sum of all values is zero")
            f.write('\n')
            continue
        f.write(str(scipy.stats.mstats.normaltest(points)))
        f.write('\n')

def wilcoxonTest(analyzableData, vidOrDat): #non parametric test
    f = open('comparingVideoToolUsageToDataWithFeb/wilcoxon/' + vidOrDat + 'WilcoxonWithFeb.txt', 'w')
    f.write('(this error kept printing to the console) UserWarning: Warning: sample size too small for normal approximation. ')
    f.write('\n')
    for graph, points in analyzableData.items():
        f.write(str(graph))
        f.write('\n')
        f.write('datapoints: ')
        f.write(str(len(points)))
        f.write('\n')
        f.write(str(scipy.stats.wilcoxon(points)))
        f.write('\n')
        f.write('\n')
    f.close()

def oneSampleTTest(analyzableData,vidOrDat):
    f = open('comparingVideoToolUsageToDataWithFeb/oneSampleTTest/' + vidOrDat + 'OneSampleTTestWithFeb.txt', 'w')
    for graph, points in analyzableData.items():
        f.write(str(graph))
        f.write('\n')
        f.write(str(scipy.stats.ttest_1samp(points, 0)))
        f.write('\n')
        f.write('\n')
    f.close()

def makeDatVidNeutComparison(toBePlotted):
    print("hi")
    print(toBePlotted)
    dataResults = {}
    videoResults  = {}
    neutralResults = {}
    for toolAndType, usage in toBePlotted.items():
        if toolAndType[1] == 'data':
            dataResults[toolAndType[0]] = usage[2]
        elif toolAndType[1] == 'video':
            videoResults[toolAndType[0]] = usage[2]
        elif toolAndType[1] == 'neutral':
            neutralResults[toolAndType[0]] = usage[2]
    print(dataResults)

    print(dataResults.values())

    N = 5
    menMeans = dataResults.values() # (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd = (2, 3, 4, 1, 2)
    womenStd = (3, 5, 2, 3, 3)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, menMeans, width, yerr=menStd)
    p2 = plt.bar(ind, womenMeans, width,
                 bottom=menMeans, yerr=womenStd)

    plt.ylabel('number times used per video per user')
    plt.xlabel('different interfaces')
    plt.title('Uses of tool per user per video')

    plt.savefig('comparingVideoToolUsageToDataWithFeb/forPaper.pdf')

    # ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    # ts = ts.cumsum()
    # ts.plot()

    # N = 5
    # menMeans = (20, 35, 30, 35, 27)
    # womenMeans = (25, 32, 34, 20, 25)
    # menStd = (2, 3, 4, 1, 2)
    # womenStd = (3, 5, 2, 3, 3)
    #
    # ind = np.arange(N)  # the x locations for the groups
    # width = 0.35  # the width of the bars: can also be len(x) sequence
    #
    # p1 = plt.bar(ind, menMeans, width, yerr=menStd)
    # p2 = plt.bar(ind, womenMeans, width,
    #              bottom=menMeans, yerr=womenStd)
    #
    # plt.ylabel('number times used per video per user')
    # plt.title('Uses of tool per user per video')
    # plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    # plt.yticks(np.arange(0, 81, 10))
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))
    # plt.interactive(False)

globalDataScrubbingVars = []
globalVideoScrubbingVars = []

def calculateMean(toBeAveragedDict, variables, interface, biggerDict):
    print("variables: ")
    print(variables)
    print("interface: ")
    print(interface)
    print("toBeAveragedDict: " + str(toBeAveragedDict.__sizeof__()))
    print(toBeAveragedDict)
    allNumbersForTypeOfTool = []
    for key, many_values in toBeAveragedDict.items():
        allNumbersForTypeOfTool.append(many_values)
        # to calculate for the individual kinds of annotation tool usage
        # print(key)
        # print(np.mean(many_values))
        # if key == ('SCRUBvideo', 'none'): # ('SCRUBvideo', 'none')
        #     print("OOOOOOOOOOOOOOOOONNNNNNNNNNNNNNNNNNNNNNNNNNEEEEEEEEEEEEEEEEEEEEE")
        #     globalVideoScrubbingVars = many_values
        #     print(globalVideoScrubbingVars)
        #
        # if key == ('SCRUBdata', 'none'): #  ('SCRUBdata', 'none')
        #     print("OOOOOOOOOOOOOOOOONNNNNNNNNNNNNNNNNNNNNNNNNNEEEEEEEEEEEEEEEEEEEEE")
        #     globalDataScrubbingVars = many_values
        #     print(globalDataScrubbingVars)
    print(np.mean(allNumbersForTypeOfTool))
    print('\n')
    #
    print(str(interface))
    biggerDict[str(interface)] = allNumbersForTypeOfTool

def runCode(dictInfo):
    # print(dictInfo)
    toBePlotted = {}
    biggerDict = defaultdict(list) # []
    for interface, variables in dictInfo.items():
        toBeAveraged = mapOfData(dataFromCSV, variables)
        toBePlotted.update(makeCSVwithAveragesDataVsVideo(toBeAveraged, dataThings, interface))



        calculateMean(toBeAveraged, variables, interface, biggerDict)
    print("hi")
    print(biggerDict)
    for oneInterfaceName, values in biggerDict.items():
        for otherName, moreValues in biggerDict.items():
            print("comparing: " + oneInterfaceName + " to " + otherName)
            print(mannwhitneyu(values, moreValues))

    # print(globalVideoScrubbingVars)
    # print(mannwhitneyu([2.0, 0.0, 0.0, 0.0, 0.0, 43.0, 0.0, 0.0, 11.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 11.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 8.0, 0.0, 0.0, 2.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 2.0, 0.0, 4.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [2.0, 101.0, 37.0, 27.0, 52.0, 61.0, 53.0, 36.0, 2.0, 25.0, 34.0, 44.0, 47.0, 91.0, 37.0, 42.0, 63.0, 82.0, 64.0, 43.0, 45.0, 36.0, 65.0, 33.0, 38.0, 15.0, 25.0, 35.0, 57.0, 14.0, 30.0, 7.0, 37.0, 23.0, 14.0, 9.0, 51.0, 21.0, 60.0, 24.0, 53.0, 31.0, 29.0, 46.0, 47.0, 31.0, 30.0, 17.0, 69.0, 34.0, 37.0, 74.0, 51.0, 23.0, 41.0, 48.0, 73.0, 39.0, 17.0, 50.0, 60.0, 38.0, 59.0, 35.0, 85.0, 35.0, 23.0, 39.0, 33.0, 88.0, 46.0, 24.0, 103.0, 40.0, 30.0, 48.0, 41.0, 38.0, 27.0, 0.0, 31.0, 17.0, 44.0, 30.0, 16.0, 0.0, 37.0, 39.0, 34.0, 17.0, 46.0, 44.0, 53.0, 45.0, 41.0, 48.0, 31.0, 34.0, 38.0, 28.0, 43.0, 44.0, 27.0, 0.0, 54.0, 63.0, 38.0, 24.0, 44.0]))

    #     boxAndWhiskerIt(toBeAveraged, interface)  # bo&whisker
    #     describeTheData(toBeAveraged, interface)  # count, mean, std, mean, 25, 50, 75, max, dtype
    #     oneSampleTTest(toBeAveraged, interface)  # normalization spread
    # # print(len(toBePlotted))
    # makeDatVidNeutComparison(toBePlotted)

dataFromCSV = readInCSV()

# dataThings = ['ENDdata','DESELECTdata','MOVE','RESIZE','JUMPdata','SCRUBdata',]
# videoThings = ['ENDvideo','JUMPvideo','SCRUBvideo','PLAY','PAUSE','CHANGEPLAYBACKRATE','SKIP']

dataThings = ['ENDdata','DESELECTdata','MOVE','RESIZE','JUMPdata','SCRUBdata',]
videoThings = ['ENDvideo','JUMPvideo','SCRUBvideo','CHANGEPLAYBACKRATE','SKIP']
neutralThings = ['PLAY','PAUSE','START','CHANGEEVENTTYPE','CANCEL','DELETE','PEEK'] # not included?? 'DESELECTneutral'

dictInfo = {}
dictInfo['data'] = dataThings
dictInfo['video'] = videoThings
dictInfo['neutral'] = neutralThings

runCode(dictInfo)
#
# toBeAveragedVideo = mapOfData(dataFromCSV, videoThings)
# toBePlotted = makeCSVwithAveragesDataVsVideo(toBeAveragedVideo, videoThings, 'video')
# makeDatVidNeutComparison(toBePlotted)
#
# toBeAveragedVideo = mapOfData(dataFromCSV, videoThings)
# toBePlotted = makeCSVwithAveragesDataVsVideo(toBeAveragedVideo, neutralThings, 'neutral')
# makeDatVidNeutComparison(toBePlotted)
#
#
# boxAndWhiskerIt(toBeAveragedData, 'data') # bo&whisker
# boxAndWhiskerIt(toBeAveragedVideo, 'video') # bo&whisker
#
# describeTheData(toBeAveragedData, 'data') # count, mean, std, mean, 25, 50, 75, max, dtype
# describeTheData(toBeAveragedVideo, 'video') # count, mean, std, mean, 25, 50, 75, max, dtype
#
# oneSampleTTest(toBeAveragedData, 'data') # normalization spread
# oneSampleTTest(toBeAveragedVideo, 'video') # normalization spread
#
#
