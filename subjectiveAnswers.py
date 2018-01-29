from __future__ import division
import glob
import json
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats
import collections
from collections import defaultdict, namedtuple
import numpy as np
from textwrap import wrap


SURVEY_PATH = '/users/home/naomi/Documents/AML/vat_analyzer/surveyInstructionsAndResults'
resultOutput = '/users/home/naomi/Documents/AML/vat_analyzer/'

Point = namedtuple('Point', 'userName, studyName, videoName, hiddenValue, '
                            'quesText, quesAnswer, quesNum, responseType, surveyFamily, answerMax')


def runVariousSurveys(possibleSurveys):
    points = []
    for study in possibleSurveys:  # ['studyA', 'studyB', 'studyC', 'studyD'] or just two of those
        points += runOneVariationOfSurveys(study)
    return points


def rawDataCSV(points):
    os.chdir(SURVEY_PATH )
    with open('allRawResults.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for tup in sorted(points):
            csvwriter.writerow(tup)
            # or csvfile.write(*tup, sep=', ')


def calculateTotalAnswersPerQuestion(points):
    # sum, count, average, maxAverage
    averages = defaultdict(lambda: [0, 0, 0, 0])
    for point in points:
        # (point)
        # Increment sum by answer, then increment count by 1
        averages[point[2:5]][0] += int(point.quesAnswer)
        averages[point[2:5]][1] += 1
        # print(point[2:5])
    # print(averages)
    return averages


    # # sum, count, average, maxAverage
    # averages = defaultdict(lambda: [0, 0, 0, 0])
    # for key, value in somePoints.items():
    #     print(key, value)
    #     averages[key] =
    #
    #     # Increment sum by answer, then increment count by 1
    #     averages[point[2:5]][0] += int(point.quesAnswer)
    #     averages[point[2:5]][1] += 1
    #     # print(point[2:5])


def calculateAverageAnswer(averages):
    # sum, count, average
    for value in averages.values():
        value[2] = value[0] / value[1]
    return averages

def makeAveragedCSV(averages):
    # print(averages)
    with open('subjectiveAnswersHiddenValRunOrPillActualQuestion/barGraphs/' + tempVar + '.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for key, value in averages.items():
            # print(key, value)
            row = [tempVar]
            row.extend(value)
            row.extend(key)
            # print(key, value)
            csvwriter.writerow(row)


def runOneVariationOfSurveys(studyType):
    answerMax = 100
    # print(os.getcwd())
    os.chdir(SURVEY_PATH)
    # print(os.getcwd())
    with open(studyType + '.tasks.json', 'r') as file:
        guidelines = json.load(file)
    studyInfo = {}
    quesInfo = {}
    # loop through each survey style ('has-both', 'no-vid', etc.)
    for key, value in guidelines['surveys'].items():
        # loop through each question in the survey:
        if key not in ['userinfo', 'practice-task', 'empty-task']:
            # key values: 'has-both', 'no-vid', etc.
            for question in value:
                # likert, likertPercentage, likertTime, etc.
                responseType = question['type']
                # question1, question2, etc.
                quesNum = question['name'].lower().replace(' ', '')
                quesText = question['text']
                quesInfo[(key, quesNum)] = (responseType, quesText)

    for task in guidelines['tasks']:
        videoNames = task['name']
        # Ignore data points that are from surveys
        if task['type'] != 'survey':
            survey = task['survey']
            data = task['data']
            if 'hide' in data:
                hidden = 'no-' + data['hide'] + '-task'
            else:
                hidden = 'has-both-task'  # Neither is hidden
            studyInfo[videoNames] = (hidden, survey)
        else:
            survey = task['survey']
            hidden = 'not applicable'
            studyInfo[videoNames] = (hidden, survey)

    # go to the folder with all users' data/results
    os.chdir(os.path.join(SURVEY_PATH, studyType))

    # only allow users 001-045
    validFiles = list(filter(lambda x: x.split('.')[0] <= '045.info.json',
                             glob.glob('*.info.json')))

    points = []
    for fileName in validFiles:
        with open(fileName, 'r') as file:
            information = json.load(file)
        userName = fileName.split('.')[0]
        allSurveys = information['surveys']

        for key, value in allSurveys.items():
            if key not in ['user-info', 'practice-first',
                           'practice-second', 'practice-third',
                           'practice-survey']:
                # 'has-both' or 'no-video' or 'post-section'
                hiddenThing, surveyFamily = studyInfo[key]
                questions = ['question' + str(i)
                             for i in range(1, len(value) + 1)]
                answers = [value[q] for q in questions]

                for quesNum, quesAnswer in zip(questions, answers):
                    quesType, quesText = quesInfo[(surveyFamily, quesNum)]
                    # Adjust (-2 to +2) to (1 to 5)
                    if (quesType == 'likert' or quesType == 'likertTime'):
                        quesAnswer = int(quesAnswer) + 3
                    if quesAnswer < 5:
                        answerMax = 5
                    points.append(Point(userName, studyType, key,
                                        hiddenThing, quesText, quesAnswer,
                                        quesNum, quesType, surveyFamily, answerMax))

                if key in ['run-survey', 'pills-survey']:
                    1 + 2

            elif key in ['user-info', 'practice-first',
                         'practice-second', 'practice-third',
                         'practice-survey']:
                1 + 1
            else:
                print("key: ", key, '\n', 'this was a BUG')
    # print(points) # total of 1200 are made here
    return points


def compareLearedVsUnlearned(points):
    with open('learnedVsUnlearned.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # points.type() # list
        newMap = {}
        # print(points)
        for key, value in averages.items():
            row = []
        csvwriter.writerow(row)
        # print(newMap)

    return newMap


def combineTwoRows(values):
    sum, count = 0, 0
    # print(values)
    for sum2, count2, currentAvg, maxAnswer in values:
        sum += sum2
        count += count2
    average = sum / count
    return sum, count, average


def correctForLearningEffect(averages):
    aggregate = collections.defaultdict(list)
    for (color, visible, question), value in averages.items():
        aggregate[visible, question].append(value)
    aggregate = {k: combineTwoRows(v) for k, v in aggregate.items()}  #

    return aggregate


def calculatePillsAndRunSeparate(averages):
    aggregate = collections.defaultdict(list)
    for (color, visible, question), value in averages.items():
        if color == 'pill-red' or color == 'pill-orange':
            color = 'pill-comb-red-orange'
        elif color == 'run-yellow' or color == 'run-red':
            color = 'run-comb-red-yellow'
        else:
            color = color + '-same'
        aggregate[color, visible, question].append(value)
    aggregate = {k: combineTwoRows(v) for k, v in aggregate.items()}  #
    return aggregate

def averageForPillVsRun(averages):
    # print(averages)
    runVpillAverage = defaultdict(lambda: [0, 0, 0, 0, key[0][:3]])
    for key, values in averages.items():
        runVpillAverage[key[1], key[2]][0] += float(values[0])
        runVpillAverage[key[1], key[2]][1] += float(values[1])
        runVpillAverage[key[1], key[2]][2] = runVpillAverage[key[1], key[2]][0] / runVpillAverage[key[1], key[2]][1]
        runVpillAverage[key[1], key[2]][3] = 100 if runVpillAverage[key[1], key[2]][2] > 5 else 5
    # print(runVpillAverage)

    with open('learnedVunlearnedForSeppi' + tempVar + '.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for key, value in runVpillAverage.items():
            # print(key, value)
            row = [tempVar]
            row.extend(value)
            row.extend(key)
            # print(row)
            csvwriter.writerow(row)

def makeListsByKeys(points):
    hiddenValAndVideoName = defaultdict(list)
    for point in points:
        # print(point)
        hiddenValue = getattr(point, 'hiddenValue')
        subVideoName = getattr(point, 'videoName')[:4]
        quesText = getattr(point, 'quesText')
        quesAnswer = int(getattr(point, 'quesAnswer'))
        surveyOrTask = getattr(point, 'videoName')
        if surveyOrTask[-6:] == 'survey':
            surveyOrTask = 'survey'
        else:
            surveyOrTask = 'annotation'
        # print(surveyOrTask)
        hiddenValAndVideoName[hiddenValue, subVideoName, quesText,surveyOrTask].append(quesAnswer)
    return hiddenValAndVideoName

def boxAndWhiskerIt(toBeAveraged):
    # print(toBeAveraged)

    # print(os.getcwd())
    for graph, points in toBeAveraged.items():
        plt.figure()
        plt.boxplot(points, 0, 'gD')
        plt.title(graph[0] + '\n' + graph[1] + '\n' + graph[2]) # what was hidden, run- or pill, actual question

        plt.savefig('subjectiveAnswersHiddenValRunOrPillActualQuestion/boxAndWhisker/' + str(graph) + '.png')

def describeTheData(toBeAveraged):
    # print(s.describe())
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/' + 'DataDescribeOutput.txt', 'w')
    for graph, points in toBeAveraged.items():
        s = pd.Series(points)
        f.write(str(graph))
        f.write('\n')
        f.write(str(s.describe()))
        #print(s.describe())
        f.write('\n\n')
    f.close()

def isItNormal(toBeAveraged):
    # print("hi")
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/normalization.txt', 'w')
    for graph, points in toBeAveraged.items():
        f.write(str(graph))
        f.write('\n')
        if sum(points) == 0:
            f.write("sum of all values is zero")
            f.write('\n')
            continue
        if len(points) < 8:
            f.write("less than eight points were given, this cannot be run")
            continue
        f.write(str(scipy.stats.mstats.normaltest(points)))
        f.write('\n\n')
    f.close()

def wilcoxonTest(analyzableData): #non parametric test
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/wilcoxon.txt', 'w')
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
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/OneSampleTTest.txt', 'w')
    f.write('RuntimeWarning: Degrees of freedom <= 0 for slice \n')
    f.write('RuntimeWarning: invalid value encountered in double_scalars ret = ret.dtype.type(ret / rcount) \n\n')
    for graph, points in analyzableData.items():
        f.write(str(graph))
        f.write('\nlen(datapoints): ')
        f.write(str(len(points)))
        f.write('\n')
        f.write(str(scipy.stats.ttest_1samp(points, 0)))
        f.write('\n')
        f.write('\n')
    f.close()

def mannWhitneyUTest(analyzableData):
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/mannWhitneyUTest.txt', 'w')
    possible 

    # f.write(str(scipy.stats.mannwhitneyu(points, secondArray, 0, 'less'))) # 'less', 'two-sided' or 'greater'

    f.close()


def makeBarGraph(someInfo):
    toBeGraphed = defaultdict(list)
    counter = 0
    for key, value in someInfo.items():
        # print(key, value)
        yMax = 5
        if value[2] > 5:
            yMax = 100
        toBeGraphed[key[0], key[1], yMax].append((key[2], value[2]))

    for graph, items in toBeGraphed.items():
        counter += 1
        yMax = graph[2]
        plt.title(graph)
        plt.xlabel('questions')
        plt.ylabel('answers')
        xvalueQuesText = []
        yvalueQuesAns = []
        for item in items:
            # print(item)
            xvalueQuesText.append(item[0])
            yvalueQuesAns.append(item[1])
        y_pos = np.arange(len(xvalueQuesText))
        if len(xvalueQuesText) == 4:
            xvalueQuesText = ['\n'.join(wrap(l, 18)) for l in xvalueQuesText]
        else:
            xvalueQuesText = ['\n'.join(wrap(l, 28)) for l in xvalueQuesText]
        plt.bar(y_pos, yvalueQuesAns, align='center', alpha=0.5)
        plt.xticks(y_pos, xvalueQuesText) # , rotation=40, ha='right'
        plt.ylim(0, graph[2])

        plt.savefig('subjectiveAnswersHiddenValRunOrPillActualQuestion/barGraphs/' + str(counter) + '.png')

#         plt.show()

        # plt.savefig('subjectiveAnswersHiddenValRunOrPillActualQuestion/barGraphs/' + str(graph) + str(graph[2]) +'.png')


options = ['studyA', 'studyB', 'studyC', 'studyD']
# options = ['studyA', 'studyB']
# options = ['studyC', 'studyD']
tempVar = 'ABCD' # C_D

points = runVariousSurveys(options) # this holds all 1200 things
# rawDataCSV(points)

# need to os.chdir because in a survey folder still
os.chdir(resultOutput)


hiddenValAndVideoName = makeListsByKeys(points)
mannWhitneyUTest(hiddenValAndVideoName) # or describeTheData or boxAndWhiskerIt or wilcoxonTest or oneSampleTTest

#
# # # this takes the sum and count to calculate averages
# averages = calculateTotalAnswersPerQuestion(points) # hiddenValAndVideoName
# averages = calculateAverageAnswer(averages)
#
# # # according to run v. pill
# # runVpillAverage = averageForPillVsRun(averages)
#
# # THINGS BROKEN UP # about 52 data-points
# # makeAveragedCSV(averages)
#
# # this puts all run-yellow with run-red AND pills-red with pills-orange #about 20 data points
# # averageTogether = correctForLearningEffect(averages)
# # makeAveragedCSV(averageTogether)
#
# # this combines run-yellow with run-red BUT leaves pills and run separate
# pillsAndRunSep = calculatePillsAndRunSeparate(averages)
# makeAveragedCSV(pillsAndRunSep)
# makeBarGraph(pillsAndRunSep)