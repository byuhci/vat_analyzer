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

# /home/naomi/Documents/
# /users/home/naomi/Documents/
survey_label_info_files = '/home/naomi/Documents/AML/data/naomiStudiesAll/user-studies' # vat_analyzer/surveyInstructionsAndResults
survey_directions = '/home/naomi/Documents/AML/data/naomiStudiesAll/user-studies'
resultOutput = '/home/naomi/Documents/AML/vat_analyzer/'

Point = namedtuple('Point', 'userName, studyName, videoName, hiddenValue, '
                            'quesText, quesAnswer, quesNum, responseType, surveyFamily, answerMax')


def runVariousSurveys(possibleSurveys):
    points = []
    for study in possibleSurveys:  # ['studyA', 'studyB', 'studyC', 'studyD'] or just two of those
        points += getData(study)
    return points

def getData(studyType):
    os.chdir(survey_directions)
    with open(studyType + '.tasks.json', 'r') as file:
        guidelines = json.load(file)
    studyInfo = getStudyInfo(guidelines)
    quesInfo = getQuesInfo(guidelines)
    file.close()
    return runOneVariationOfSurveys(studyInfo, quesInfo, studyType)

def getQuesInfo(guidelines):
    answerMax = 100
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
    return quesInfo

def getStudyInfo(guidelines):
    studyInfo = {}
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
    return studyInfo


def selectFileNames(studyType):
    # only allow users 001-056
    validFiles = list(filter(lambda x: x.split('.')[0] <= '056.info.json',
                             glob.glob('*.info.json')))
    validFiles.extend(filter(lambda x: x.split('.')[0] <= '056.info.json',
                             glob.glob('*.survey.json')))
    return validFiles

def runOneVariationOfSurveys(studyInfo, quesInfo, studyType):
    # go to the folder with all users' data/results
    # os.chdir(os.path.join(survey_label_info_files, studyType))
    print(os.listdir(os.getcwd()))
    validFiles = selectFileNames(studyType)
    points = []

    for fileName in validFiles:
        # print(fileName)
        with open(fileName, 'r') as file:
            information = json.load(file)
        userName = fileName.split('.')[0]


        if fileName[-11:] == 'survey.json':
            # then do different things because this file only has the text answers
            for sets, questions in information.items():
                for question, textAnswer in questions.items():
                    print(question, textAnswer)
                    # TODO: these are the question answers for the final likerty thing
                    # SAVE THEM
                    # and grab the question text while we're here
                    # points.append(Point(userName, studyType, key,
                    #                     hiddenThing, quesText, quesAnswer,
                    #                     quesNum, quesType, surveyFamily, answerMax))
        continue; # because we got everything out of that file


        allSurveys = information['surveys']
        # print(allSurveys)
        for key, value in allSurveys.items():
            # if key in ['question1', 'question2', 'question3', 'question4']:
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
    return points # total of 1200 are made here


def lookForMissingAnnotationsFromUsers(points):
    usersPerVideoName = defaultdict(set)
    forUserNameSeeVideo = defaultdict(set)
    # per study and video color/name, which users saw that:
    for point in points:
        videoName = getattr(point, 'videoName')
        usersName = getattr(point, 'userName')
        hiddenVal = getattr(point, 'hiddenValue')
        study = getattr(point, 'studyName')
        usersPerVideoName[study, videoName].add(int(usersName))
        forUserNameSeeVideo[study, usersName].add(videoName)

    # sort that, so users are in numerical order
    for key, value in forUserNameSeeVideo.items():
        forUserNameSeeVideo[key] = sorted(value)



def rawDataCSV(points):
    os.chdir(resultOutput)
    with open('subjectiveAnswersHiddenValRunOrPillActualQuestion/things/allRawResultsWithFeb.csv', 'w') as csvfile:
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

def calculateAverageAnswer(averages):
    # sum, count, average
    for value in averages.values():
        value[2] = value[0] / value[1]
    return averages

def makeAveragedCSV(averages):
    # print(averages)
    with open('subjectiveAnswersHiddenValRunOrPillActualQuestion/barGraphsWithFeb/' + tempVar + 'WithFeb.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for key, value in averages.items():
            # print(key, value)
            row = [tempVar]
            row.extend(value)
            row.extend(key)
            # print(key, value)
            csvwriter.writerow(row)


def compareLearedVsUnlearned(points):
    with open('../subjectiveAnswersHiddenValRunOrPillActualQuestion/things/learnedVsUnlearnedWithFeb.csv', 'w') as csvfile:
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

    with open('learnedVunlearnedForSeppi' + tempVar + 'WithFeb.csv', 'w') as csvfile:
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
    # subjectiveAnswersHiddenValRunOrPillActualQuestion/boxAndWhisker # name of folder I should be in
    # print(toBeAveraged)
    # xvalueQuesText = ['\n'.join(wrap(l, 18)) for l in xvalueQuesText]
    for graph, points in toBeAveraged.items():
        plt.figure()
        yMin = 0
        yMax = 5
        if points[0] > 5:
            yMax = 100
        plt.ylim((yMin, yMax))
        plt.boxplot(points, 0, 'gD')
        titleVar = graph[2] + '\n' + graph[1] + '\n' + graph[0] + '\n' + 'length of points list: ' + str(len(points))
        plt.title(titleVar) # what was hidden, run- or pill, actual question

        plt.savefig('subjectiveAnswersHiddenValRunOrPillActualQuestion/boxAndWhisker/' + titleVar + '.png')

def describeTheData(toBeAveraged):
    # print(s.describe())
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/DataDescribeOutputWithFeb.txt', 'w')
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
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/normalizationWithFeb.txt', 'w')
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
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/wilcoxonWithFeb.txt', 'w')
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
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/OneSampleTTestWithFeb.txt', 'w')
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
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/mannWhitneyUTestWithFeb.txt', 'w')
    # possible

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



# lookForMissingAnnotationsFromUsers(points) # not necessarily needed #
rawDataCSV(points)

# need to os.chdir because in a survey folder still
os.chdir(resultOutput) #  /AML/vat_analyzer
# print(os.getcwd())


hiddenValAndVideoName = makeListsByKeys(points)
boxAndWhiskerIt(hiddenValAndVideoName)
describeTheData(hiddenValAndVideoName)
wilcoxonTest(hiddenValAndVideoName)
oneSampleTTest(hiddenValAndVideoName)


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