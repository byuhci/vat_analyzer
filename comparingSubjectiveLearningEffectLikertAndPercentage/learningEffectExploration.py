from collections import defaultdict, namedtuple
import csv
import matplotlib.pyplot as plt
import itertools
import numpy as np

forGraphing = namedtuple('forGraphing', ['pillOrRun', 'hiddenValue', 'quesText'])

def compareLearnedVsUnlearned():
    # futureGraphs = defaultdict(list)
    toBeGraphed = defaultdict(list)
    with open('learnedVunlearnedForSeppi.csv') as f:
        data = list(csv.reader(f, delimiter=','))
        # print(data) # ['C_D', '103', '28', '3.6785714285714284', 'no-video-task', 'When I...']
    for item in data:
        # hiddenValue, quesText = x, y, ymax
        if float(item[3]) < 5:
            maxAnswer = 5
        else:
            maxAnswer = 100
        # print(item)

        toBeGraphed[forGraphing(pillOrRun=item[5], hiddenValue=item[6], quesText=item[7])].append((item[0], item[3], maxAnswer))
        # futureGraphs[item[4], item[5]].append((item[0], item[3], maxAnswer))
    print(toBeGraphed)
    return toBeGraphed

def learnedAndUnlearned(futureGraphs):
    # Sprint(futureGraphs)
    group_num = 0
    for keys in futureGraphs:
        group_num += 1
        # plt.subplot(6, 6, group_num)
        print(keys)
        points = futureGraphs[keys]
        # print(futureGraphs[hiddenValue, quesText], hiddenValue, quesText)
        dataDict = {}
        yMax = 20
        yLabel = 'from 1 to 5'

        fig, ax = plt.subplots(nrows=1, ncols=1)

        title = keys.quesText + '\n' + keys.hiddenValue + '\n' + keys.pillOrRun
        plt.title(title)

        for triplet in points:
            dataDict[triplet[0]] = float(triplet[1]) # (x, y)
            yMax = triplet[2]
        # if yMax == 100:
        #     yLabel = 'Percentage'
        # plt.ylabel(yLabel)
        # plt.xlabel('survey versions')

        plt.bar(range(len(dataDict)), dataDict.values(), align='center')
        plt.xticks(range(len(dataDict)), dataDict.keys())
        # plt.ylabel(yLabel)
        plt.ylim(0, yMax) # 0, yMax
        plt.show()
        plt.tight_layout()
        fig.savefig('graphsComparingLearningEffect/' + title.replace('\n','_') + '.png')
        plt.close(fig)

def boxAndWhiskerIt(toBeAveraged):
    # print(toBeAveraged)
    for graph, points in toBeAveraged.items():
        plt.figure()
        plt.boxplot(points, 0, 'gD')
        plt.title(graph)

        print(graph[0])
        title = graph[0]+'hidden-' +graph[1]

        plt.savefig('boxAndWhiskerComparingVideoToolUsageToData/' + title + '.png')

def describeTheData(toBeAveraged):
    s = pd.Series([1, 2, 3])
    # print(s.describe())
    f = open('boxAndWhiskerComparingVideoToolUsageToData/dataDescribeOutput.txt', 'w')
    for graph, points in toBeAveraged.items():
        s = pd.Series(points)
        f.write(graph[0])
        f.write(graph[1])
        f.write(str(s.describe()))
        #print(s.describe())
        f.write('\n\n')
    f.close()

pleaseGraph = compareLearnedVsUnlearned()
print(pleaseGraph)
# learnedAndUnlearned(pleaseGraph) # this makes graphs
# this makes Box&Whisker plots
# this describes the data

