# # import numpy as np
# import matplotlib.pyplot as plt
# import csv
# import itertools
#
#
# round one with Alyssa
# x = []
# y = []
#
# title = [] # String of question
# point = [] # data point
# line = [] # vid/dat hidden
# allGraphs = {}
# listOfTuples = []
# translation = {}
#
# with open('surveyResults.csv', 'r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         translation = {'not applicable': 0, 'no-data-task':1, 'no-video-task':2,'has-both-task':3 }
#
#         if row[5] not in allGraphs:
#             allGraphs[row[5]] = [int(row[2]), yvalue]
#         else:
#             allGraphs[row[5]].append(int(row[2]))
#             allGraphs[row[5]].append(yvalue)
#
#
# for item in allGraphs:
#     manyPairs = allGraphs[item]
#     for dataPoint in manyPairs:
#         print("hi")
#         # how can I access dataPoint and dataPoint+1??
#         # plt.plot(pair[1], pair[0], label=item)
#         # plt.xlabel('what was visible')
#         # plt.ylabel('satisfaction/success')
#         # plt.title(item)
#         # plt.legend()
#         # plt.show()
#
#


# # round two, with Jeff
# import csv
# import itertools
# import matplotlib.pyplot as plt
#
#
# with open('surveyResults.csv') as f:
#     data = list(csv.reader(f, delimiter=','))
#     data.sort(key=lambda row: row[4])
#
# for group_num, (group_name, rows) in enumerate(itertools.groupby(data, key=lambda row: row[4])):
#     plt.subplot(5, 5, group_num+1)
#     # print(rows[4])
#     plt.title(group_name)
#     rows = sorted(list(rows), key=lambda row: row[3]) # sort by hidden video type
#     # print(rows.type())
#     print('\n'.join([str(row) for row in rows]))
#     xs, heights, names = zip(*((n, float(row[2]), row[3]) for n, row in enumerate(rows)))
#     print(group_name, xs, names, heights)
#     print(type(xs), type(names))
#     plt.xticks(xs, names)
#     plt.bar(xs, heights)
#     plt.ylim(0, 5 if heights[0] < 5 else 100)
#
# plt.show()

# round three, with Kristian
# import csv
#
# with open('surveyResults.csv') as f:
#     data = list(csv.reader(f, delimiter=','))
#     # data.sort(key=lambda row: row[4])

# round four
import collections
import csv
import matplotlib.pyplot as plt
import itertools
import numpy as np

def compareLearnedVsUnlearned():
    futureGraphs = collections.defaultdict(list)
    with open('runFirstThenPills_allABCD.csv') as f:
        data = list(csv.reader(f, delimiter=','))
        # print(data) # ['C_D', '103', '28', '3.6785714285714284', 'no-video-task', 'When I...']
    for item in data:
        # hiddenValue, quesText = x, y, ymax
        if float(item[3]) < 5:
            maxAnswer = 5
        else:
            maxAnswer = 100
        futureGraphs[item[4], item[5]].append((item[0], item[3], maxAnswer))
    return futureGraphs

def learnedAndUnlearned(futureGraphs):
    group_num = 0
    for hiddenValue, quesText in futureGraphs:
        points = futureGraphs[hiddenValue, quesText]
        xobjects = []
        yvalues = []
        yMax = 0
        yLabel = 'from 1 to 5'
        if yMax == 100:
            'Percentage'
        for triplet in points:
            yvalues.append(triplet[1])
            xobjects.append(triplet[0])

            yMax = triplet[2]
        yPos = np.arrange(len(xobjects))
        plt.bar(yPos, yvalues, align='center', alpha=.5)  # what is alpha?
        plt.xticks(yPos, xobjects)
        plt.ylabel(yLabel)
        plt.title(quesText)
        plt.show()

# objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
# y_pos = np.arange(len(objects))
# performance = [10, 8, 6, 4, 2, 1]
#
# plt.bar(y_pos, performance, align='center', alpha=0.5)
# plt.xticks(y_pos, objects)
# plt.ylabel('Usage')
# plt.title('Programming language usage')
#
# plt.show()


pleaseGraph = compareLearnedVsUnlearned()
learnedAndUnlearned(pleaseGraph)

