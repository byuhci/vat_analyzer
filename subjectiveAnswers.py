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
survey_label_info_files = '/home/naomi/Documents/AML/data/naomiStudiesAll/user-studies'  # vat_analyzer/surveyInstructionsAndResults
survey_directions = '/home/naomi/Documents/AML/data/naomiStudiesAll/user-studies'
resultOutput = '/home/naomi/Documents/AML/vat_analyzer/'

Point = namedtuple('Point', 'userName, studyName, videoName, hiddenValue, '
                            'quesText, quesAnswer, quesNum, responseType, surveyFamily')


def runVariousSurveys(possibleSurveys):
    points = []
    for study in possibleSurveys:  # ['studyA', 'studyB', 'studyC', 'studyD'] or just two of those
        points += getData(study)
    # print(points)
    return points


def getData(studyType):
    os.chdir(survey_directions)
    with open(studyType + '.tasks.json', 'r') as file:
        guidelines = json.load(file)
    studyInfo = getStudyInfo(guidelines)
    quesInfo = getQuesInfo(guidelines)
    file.close()
    points = runOneVariationOfSurveys(studyInfo, quesInfo, studyType)
    return points


def getQuesInfo(guidelines):
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
    noDuplicatePoints = set()
    # go to the folder with all users' data/results
    folderStudySpecific = os.path.join(survey_label_info_files, studyType)
    os.chdir(folderStudySpecific)

    foldersFromStudy = os.listdir(os.getcwd())

    for folder in foldersFromStudy:
        os.chdir(os.path.join(survey_label_info_files, studyType, folder))
        # print(folder)
        noDuplicatePoints = noDuplicatePoints | runWholeFolder(studyInfo, quesInfo, studyType)
    # print(points)
    # print(noDuplicatePoints)
    return noDuplicatePoints  # total of 1200 are made here


def runWholeFolder(studyInfo, quesInfo, studyType):
    points = set()
    eachFileOfData = os.listdir(os.getcwd())
    taskFolderName = (os.getcwd().split('/'))[-1:][0]
    # print((os.getcwd().split('/')))
    for oneFile in eachFileOfData:
        with open(oneFile, 'r') as file:
            information = json.load(file)
        userName = oneFile.split('.')[0]
        points = points | runOneFile(studyInfo, quesInfo, information, userName, oneFile, studyType, taskFolderName)
    # print(points)
    return points


# global numEmptyFiles

def runOneFile(studyInfo, quesInfo, information, userName, oneFile, studyType, taskFolderName):
    # validFiles = selectFileNames(studyType) # manually cleaned data, should not be issue
    points = set()
    if oneFile[-9:] == 'info.json':
        points = points | infoFiles(studyInfo, quesInfo, information, userName, studyType, taskFolderName)
        # print(points)
    elif oneFile[-11:] == 'survey.json':
        points = points | surveyFiles(studyInfo, quesInfo, information, userName, studyType, taskFolderName)
    elif not oneFile[-11:] == 'labels.json':
        print("unknown file name syntax: ", oneFile)
    #if points == set() and not oneFile[-11:] == 'labels.json':
        # TODO: are we concerned all of these are empty??
        #print('runOneFile leaving empty', userName, oneFile, studyType, taskFolderName)
        # numEmptyFiles += 1
    return points


def infoFiles(studyInfo, quesInfo, information, userName, studyType, taskFolderName):
    points = set()
    allSurveys = information['surveys']
    # print(allSurveys)
    for videoColorOrTask, value in allSurveys.items():
        if videoColorOrTask not in ['user-info', 'practice-first',
                                    'practice-second', 'practice-third',
                                    'practice-survey']:
            # print(videoColorOrTask, taskFolderName)
            # 'has-both' or 'no-video' or 'post-section'
            hiddenThing, surveyFamily = studyInfo[videoColorOrTask]
            # print(hiddenThing, surveyFamily)
            questions = ['question' + str(i)
                         for i in range(1, len(value) + 1)]
            answers = [value[q] for q in questions]

            for quesNum, quesAnswer in zip(questions, answers):
                quesType, quesText = quesInfo[(surveyFamily, quesNum)]
                # Adjust (-2 to +2) to (1 to 5)
                # print(int(userName) < 045)
                if ((quesType == 'likert' or quesType == 'likertTime') and int(userName) < 045):
                    # the original version was scaled from -2 to +2 points (not 1-5)

                    quesAnswer = int(quesAnswer) + 3

                newPoint = Point(userName, studyType, videoColorOrTask,
                                 hiddenThing, quesText, int(quesAnswer),
                                 quesNum, quesType, surveyFamily)
                points.add(newPoint)
    return points


def surveyFiles(studyInfo, quesInfo, information, userName, studyType, taskFolderName):
    points = set()
    videoColorOrTask = taskFolderName  # list with one thing in it
    for sets, questions in information.items():
        for quesNum, quesAnswer in questions.items():
            if quesNum in ['lastname', 'firstname', 'email']:
                continue
            # print(studyInfo[videoColorOrTask])
            hiddenThing, surveyFamily = studyInfo[videoColorOrTask]
            quesType, quesText = quesInfo[(surveyFamily, quesNum)]

            # print(type(quesAnswer))
            try:
                int(quesAnswer)
                quesAnswer = int(quesAnswer)
            except ValueError:
                1 + 1
            points.add(Point(userName, studyType, videoColorOrTask,
                             hiddenThing, quesText, quesAnswer,
                             quesNum, quesType, surveyFamily))

    if points == set():
        print('no \'survey\' in this file: ', userName, studyType, taskFolderName)
    return points


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
        responseType = getattr(point, 'responseType')
        if responseType == 'textMulti':
            continue
        # Increment sum by answer, then increment count by 1
        averages[point[2:5]][0] += int(point.quesAnswer)
        averages[point[2:5]][1] += 1
    return averages


def calculateAverageAnswer(averages):
    # sum, count, average
    maxAnswers = {}
    # print(averages)
    for colorHiddenQuestion, sumCountAvgMax in averages.items():
        if sumCountAvgMax == [0, 0, 0, 0]:
            continue
        sumCountAvgMax[2] = sumCountAvgMax[0] / sumCountAvgMax[1]
        if sumCountAvgMax[2] > 5:
            sumCountAvgMax[3] = 100
        else:
            sumCountAvgMax[3] = 5
        maxAnswers[colorHiddenQuestion[2]] = sumCountAvgMax[3]
    # print(averages)
    return averages, maxAnswers


def makeAveragedCSV(averages):
    # print(averages)
    print(tempVar)
    with open('subjectiveAnswersHiddenValRunOrPillActualQuestion/things/' + tempVar + 'WithFeb.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for key, value in averages.items():
            # print(key, value)
            row = [tempVar]
            row.extend(value)
            row.extend(key)
            # print(key, value)
            csvwriter.writerow(row)


def makeOutputOfTextQuestion(points):
    with open('subjectiveAnswersHiddenValRunOrPillActualQuestion/things/textQuestionsWithFeb.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        pairs = []
        for point in points:
            responseType = getattr(point, 'responseType')
            if not responseType == 'textMulti':
                continue
            quesAnswer = getattr(point, 'quesAnswer')
            quesText = getattr(point, 'quesText')

            pairs.append((quesText, quesAnswer))
        pairs.sort()
        for pair in pairs:
            quesText = pair[0]
            quesAnswer = pair[1]
            row = [quesText, quesAnswer]
            csvwriter.writerow(row)


def compareLearedVsUnlearned(points):
    with open('../subjectiveAnswersHiddenValRunOrPillActualQuestion/things/learnedVsUnlearnedWithFeb.csv',
              'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # points.type() # list
        newMap = {}
        # print(points)
        for key, value in points.items():
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


def makeListsByKeys(points, maxAnswers):
    hiddenValAndVideoName = defaultdict(list)
    for point in points:
        # print(point)
        hiddenValue = getattr(point, 'hiddenValue')
        subVideoName = getattr(point, 'videoName')[:4]
        quesText = getattr(point, 'quesText')
        quesAnswer = getattr(point, 'quesAnswer')
        surveyOrTask = getattr(point, 'videoName')
        if surveyOrTask[-6:] == 'survey':
            surveyOrTask = 'survey'
        else:
            surveyOrTask = 'annotation'
        # print(surveyOrTask)
        if maxAnswers.has_key(str(quesText)):
            numMaxAnswer = maxAnswers[str(quesText)]
        else:
            numMaxAnswer = 'string'
        hiddenValAndVideoName[hiddenValue, subVideoName, quesText, surveyOrTask, numMaxAnswer].append(quesAnswer)
    print(hiddenValAndVideoName)
    return hiddenValAndVideoName


def boxAndWhiskerIt(toBeAveraged):
    # subjectiveAnswersHiddenValRunOrPillActualQuestion/boxAndWhisker # name of folder I should be in
    # print(repr(toBeAveraged))

    for graph, points in toBeAveraged.items():
        plt.figure()
        yMin = 0
        yMax = 5
        if points[0] > 5:
            yMax = 100
        plt.ylim((yMin, yMax))
        if type(points[0]) is not int:
            continue
        plt.boxplot(points, 0, 'gD')
        titleVar = graph[2] + '\n' + graph[1] + '    ' + graph[0]  + '    length of points list: ' + str(len(points))
        plt.title(titleVar)  # what was hidden, run- or pill, actual question

        plt.savefig('subjectiveAnswersHiddenValRunOrPillActualQuestion/boxAndWhisker/' + titleVar + '.png')


def describeTheData(toBeAveraged):
    # print(s.describe())
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/DataDescribeOutputWithFeb.txt', 'w')
    for graph, points in toBeAveraged.items():
        s = pd.Series(points)
        f.write(str(graph))
        f.write('\n')
        f.write(str(s.describe()))
        # print(s.describe())
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


def wilcoxonTest(analyzableData):  # non parametric test
    f = open('subjectiveAnswersHiddenValRunOrPillActualQuestion/wilcoxonWithFeb.txt', 'w')
    f.write(
        '(this error kept printing to the console) UserWarning: Warning: sample size too small for normal approximation. ')
    f.write('\n')
    for graph, points in analyzableData.items():
        if type(points[0]) is not int:
            continue
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
        if type(points[0]) is not int:
            continue
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
        plt.xticks(y_pos, xvalueQuesText)  # , rotation=40, ha='right'
        plt.ylim(0, graph[2])

        plt.savefig('subjectiveAnswersHiddenValRunOrPillActualQuestion/barGraphs/' + str(counter) + '.png')


#         plt.show()

# plt.savefig('subjectiveAnswersHiddenValRunOrPillActualQuestion/barGraphs/' + str(graph) + str(graph[2]) +'.png')


options = ['studyA', 'studyB', 'studyC', 'studyD']
# options = ['studyA', 'studyB']
# options = ['studyC', 'studyD']
tempVar = 'ABCD'  # C_D

points = runVariousSurveys(options)  # this holds all 1200 things

# lookForMissingAnnotationsFromUsers(points) # not necessarily needed #
rawDataCSV(points)

# need to os.chdir because in a survey folder still
os.chdir(resultOutput)  # /AML/vat_analyzer
# print(os.getcwd())

# # this takes the sum and count to calculate averages
makeOutputOfTextQuestion(points)
averages = calculateTotalAnswersPerQuestion(points)  # hiddenValAndVideoName
averages, maxAnswers = calculateAverageAnswer(averages)
makeAveragedCSV(averages)

# # all of these at once demo okke-
hiddenValAndVideoName = makeListsByKeys(points, maxAnswers)
# print(hiddenValAndVideoName)
boxAndWhiskerIt(hiddenValAndVideoName)
describeTheData(hiddenValAndVideoName)
wilcoxonTest(hiddenValAndVideoName)
oneSampleTTest(hiddenValAndVideoName)


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
