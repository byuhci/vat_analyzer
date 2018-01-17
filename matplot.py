# # import numpy as np
# import matplotlib.pyplot as plt
# import csv
# import itertools
#
#
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
import csv
import itertools
import matplotlib.pyplot as plt


with open('surveyResults.csv') as f:
    data = list(csv.reader(f, delimiter=','))
    data.sort(key=lambda row: row[5])

for group_name, rows in itertools.groupby(data, lambda row: row[5]):
    # print(rows[5])
    plt.title(group_name)
    rows = sorted(list(rows), key=lambda row: row[5]) # was four before
    # print(rows.type())
    print(rows), '/n'
    xs, heights, names = zip(*((n, int(row[2]), row[4]) for n, row in enumerate(rows)))
    print(group_name, xs, names, heights)
    plt.xticks(xs, names)
    plt.bar(xs, heights)
    plt.show()