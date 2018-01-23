from __future__ import division
import glob
import json
import os
import csv
from sys import argv
import collections
from collections import defaultdict, namedtuple

SURVEY_PATH = '/home/naomi/Documents/AML/vat_analyzer/surveyResultsForPython_raw_cleaned_data'

Point = namedtuple('Point', 'userName, studyName, videoName, hiddenValue, '
                            'quesText, quesAnswer, quesNum, responseType, surveyFamily, answerMax')


def runVariousSurveys(possibleSurveys):
    points = []
    for study in possibleSurveys:  # ['studyA', 'studyB', 'studyC', 'studyD']
        points += runOneVariationOfSurveys(study)
    return points


def rawDataCSV(points):
    os.chdir(SURVEY_PATH)
    with open('allRawResults.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for tup in sorted(points):
            csvwriter.writerow(tup)
            # or csvfile.write(*tup, sep=', ')


def calculateTotalAnswersPerQuestion(points):
    # sum, count, average, maxAverage
    averages = defaultdict(lambda: [0, 0, 0, 0])
    for point in points:
        # Increment sum by answer, then increment count by 1
        averages[point[2:5]][0] += int(point.quesAnswer)
        averages[point[2:5]][1] += 1
    return averages


def calculateAverageAnswer(averages):
    # sum, count, average
    for value in averages.values():
        value[2] = value[0] / value[1]
    return averages


def makeAveragedCSV(averages):
    tempVar = 'A_B'  # C_D
    print(averages)
    with open('runFirstThenPills' + tempVar + '.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for key, value in averages.items():
            # print(key, value)
            row = [tempVar]
            row.extend(value)
            row.extend(key)
            # print(row)
            csvwriter.writerow(row)


def runOneVariationOfSurveys(studyType):
    answerMax = 100
    os.chdir(SURVEY_PATH)
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
    return points


def compareLearedVsUnlearned(points):
    with open('learnedVsUnlearned.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # points.type() # list
        newMap = {}
        print(points)
        for key, value in averages.items():
            row = []
        csvwriter.writerow(row)
        print(newMap)

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


# options = ['studyA', 'studyB', 'studyC', 'studyD']
options = ['studyA', 'studyB']
# options = ['studyC', 'studyD']


points = runVariousSurveys(options)
# print(points)
rawDataCSV(points)

# this takes the sum and count to calculate averages
averages = calculateTotalAnswersPerQuestion(points)
averages = calculateAverageAnswer(averages)

# make a function that compares first round v. second round of pills, then does the same with running
# someDictionary = compareLearedVsUnlearned(points) # I decided to not use this
# printListCSV(someDictionary) # can't use this either

# THINGS BROKEN UP # about 52 data-points
# makeAveragedCSV(averages)

# this puts all run-yellow with run-red AND pills-red with pills-orange #about 20 data points
# averageTogether = correctForLearningEffect(averages)
# makeAveragedCSV(averageTogether)

# this combines un-yellow with run-red BUT leaves pills and run separate
# pillsAndRunSep = calculatePillsAndRunSeparate(averages)
# makeAveragedCSV(pillsAndRunSep)
