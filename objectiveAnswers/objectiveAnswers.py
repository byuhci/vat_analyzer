import csv
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats
import csv
from collections import defaultdict, namedtuple

# 'task', 'user', 'precision', 'recall', 'F1', 'study', 'hidden'
objectivePoint = namedtuple('objectivePoint', 'task, user, precision, recall, F1, study, hidden')

def readInput():
    # format: task	user	precision	recall	F1	study	hidden
    allObjectiveData = []
    # tuesdayUserStudy_c_d.csv # objective_2018_01_25_studyABCD.csv
    with open('objective_2018_01_25_studyABCD.csv') as csvfile:
        data = list(csv.reader(csvfile, delimiter=','))
        for row in data:
            # print(row)
            # run-blue	16	0.7998874313	0.7209302326	0.75745646		studyB	none
            allObjectiveData.append(objectivePoint(task=row[0], user=row[1], precision=row[2], recall=row[3], F1=row[4], study=row[5], hidden=row[6]))
    # print(allObjectiveData)
    return allObjectiveData

def eachUsersAverages(allObjectiveData):
    perUserRecallScores = defaultdict(list)
    for point in allObjectiveData:
        # task = getattr(point, 'task')
        user = getattr(point, 'user')
        # precision = getattr(point, 'precision')
        recall = getattr(point, 'recall')
        # F1 = getattr(point, 'F1')
        # study = getattr(point, 'study')
        # hidden = getattr(point, 'hidden')
        perUserRecallScores[user].append(float(recall))
    userNameToAverageRecall = {}
    for userName, allRecallScores in perUserRecallScores.items():
        # print(userName, allRecallScores)
        # for item in allRecallScores:
        average = sum(allRecallScores)/len(allRecallScores)
        userNameToAverageRecall[userName] = average
        print(userName, average)
    f = open('objectiveData/averageRecallScorePerUser.txt', 'w')
    for user, score in userNameToAverageRecall.items():
        f.write(user)
        f.write(',')
        f.write(str(score))
        f.write('\n')
    f.close()

    # print(userNameToAverageRecall)


def lookForMissing(allObjectiveData):
    perStudyAndVideoEqualsUser = defaultdict(list)
    for point in allObjectiveData:
        task = getattr(point, 'task')
        user = getattr(point, 'user')
        precision = getattr(point, 'precision')
        recall = getattr(point, 'recall')
        F1 = getattr(point, 'F1')
        study = getattr(point, 'study')
        hidden = getattr(point, 'hidden')
        perStudyAndVideoEqualsUser[study, task].append(user)
    for studysTask, value in perStudyAndVideoEqualsUser.items():
        # print(studysTask)
        perStudyAndVideoEqualsUser[studysTask] = sorted(value)


    print(perStudyAndVideoEqualsUser)

def selectAspectsOfData(allObjectiveData):
    perTaskAndHiddenEqualsPrecision = defaultdict(list)
    perTaskAndHiddenEqualsRecall = defaultdict(list)
    perTaskAndHiddenEqualsF1 = defaultdict(list)
    perUserPrecision = defaultdict(list)
    perStudyAndTaskEqualsPrecision = defaultdict(list)
    perHiddenEqualF1 = defaultdict(list)
    for point in allObjectiveData:
        task = getattr(point, 'task')
        user = getattr(point, 'user')
        precision = getattr(point, 'precision')
        recall = getattr(point, 'recall')
        F1 = getattr(point, 'F1')
        study = getattr(point, 'study')
        hidden = getattr(point, 'hidden')

        perTaskAndHiddenEqualsPrecision[task, hidden].append(float(precision))
        perTaskAndHiddenEqualsRecall[task, hidden].append(float(recall))
        perTaskAndHiddenEqualsF1[task, hidden].append(float(F1))
        perUserPrecision[user].append(float(precision))
        perStudyAndTaskEqualsPrecision[study, task].append(float(precision))
        perHiddenEqualF1[hidden].append(float(precision))

    return perTaskAndHiddenEqualsPrecision
strSelectAspectsOfData= 'perTaskAndHiddenEqualsPrecision'



def describeTheData(inputData):
    # print(s.describe())
    f = open('objectiveData/dataDescribeOutput/' + strSelectAspectsOfData + 'DataDescribeOutput.txt', 'w')
    for graph, points in inputData.items():
        s = pd.Series(points)
        f.write(str(graph))
        f.write('\n')
        f.write(str(s.describe()))
        #print(s.describe())
        f.write('\n\n')
    f.close()

def isItNormal(inputData):
    # print("hi")
    f = open('objectiveData/normalization/' + strSelectAspectsOfData + 'Normalization.txt', 'w')
    for graph, points in inputData.items():
        f.write(str(graph))
        f.write('\n')
        if sum(points) == 0:
            f.write("sum of all values is zero")
            f.write('\n')
            continue
        if len(points) <= 20:
            f.write("Twenty or less points were given, (")
            f.write(str(len(points)))
            f.write(") this might not be accurate: \n")
        if len(points) < 8:
            f.write("less than eight points were given, this cannot be run")
            continue
        f.write(str(scipy.stats.mstats.normaltest(points)))
        f.write('\n\n')



def boxAndWhiskerIt(inputData):
    for graph, points in inputData.items():
        yMin = 0
        yMax = 1
        plt.ylim(yMin,yMax)
        print(graph, points)
        plt.figure()
        plt.boxplot(points, 0, 'gD')
        plt.title(graph) # what was hidden, run- or pill, actual question
        plt.savefig('objectiveData/boxAndWhisker/' + strSelectAspectsOfData + '/' + strSelectAspectsOfData + str(graph) + '.png')

def wilcoxonTest(analyzableData): #non parametric test
    f = open('objectiveData/wilcoxon/' + strSelectAspectsOfData + 'Wilcoxon.txt', 'w')
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

def oneSampleTTest(analyzableData):
    f = open('objectiveData/oneSampleTTest/' + strSelectAspectsOfData + 'OneSampleTTest.txt', 'w')
    for graph, points in analyzableData.items():
        f.write(str(graph))
        f.write('\n')
        f.write(str(scipy.stats.ttest_1samp(points, 0)))
        f.write('\n')
        f.write('\n')
    f.close()





def mannWhiteneyTest(analyzableData):
    print("do more stuff")

input = readInput()
# selectedResults = selectAspectsOfData(input)
# lookForMissing(input)
# # boxAndWhiskerIt(selectedResults)

averagedInfo = eachUsersAverages(input)