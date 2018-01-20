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
                   'quesText, quesAnswer, quesNum, responseType, surveyFamily')

def runVariousSurveys():
    points = []
    for study in ['studyA', 'studyB', 'studyC', 'studyD']: #
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
    # sum, count, average
    averages = defaultdict(lambda: [0, 0, 0])
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
    with open('pillsAndRunSepFirstVsSecondRounds.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for key, value in averages.items(): 
            # print(key, value) 
            row = []
            row.extend(value)
            row.extend(key)
            # print(row)
            csvwriter.writerow(row)

def runOneVariationOfSurveys(studyType):
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
    #print('quesInfo', quesInfo)
    # allTasks is a list of order videos/surveys
    #print('task')
    for task in guidelines['tasks']:
        #print(task)
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
            # print("SOLVING BUG HERE!")
            # print(videoNames, hidden, survey)
    #print('\n')
    #print('studyInfo', studyInfo)
    #go to the folder with all users' data/results
    os.chdir(os.path.join(SURVEY_PATH, studyType))
    # cwd = os.getcwd()
    # print(cwd)

    #only allow users 001-045
    validFiles = list(filter(lambda x: x.split('.')[0]<='045.info.json',
                             glob.glob('*.info.json')))

    points = []
    for fileName in validFiles:
        with open(fileName, 'r') as file:
            information = json.load(file)
        userName = fileName.split('.')[0]
        allSurveys = information['surveys']
        #print('set(allSurveys.keys()): ', set(allSurveys.keys()))
        #print('set(studyInfo.keys()): ', set(studyInfo.keys()))
        #key=name of video, value={'q1'='ans',...}
        for key, value in allSurveys.items():
            if key not in ['user-info', 'practice-first',
                           'practice-second', 'practice-third',
                           'practice-survey']:
                # 'has-both' or 'no-video' or 'post-section'
                hiddenThing, surveyFamily = studyInfo[key]
                questions = ['question' + str(i)
                             for i in range(1, len(value)+1)]
                answers = [value[q] for q in questions]

                for quesNum, quesAnswer in zip(questions, answers):
                    quesType, quesText = quesInfo[(surveyFamily, quesNum)]
                    # Adjust (-2 to +2) to (1 to 5)
                    if (quesType == 'likert' or quesType == 'likertTime'):
                        quesAnswer = int(quesAnswer) + 3
                    points.append(Point(userName, studyType, key,
                                        hiddenThing, quesText, quesAnswer,
                                        quesNum, quesType, surveyFamily))

                if key in ['run-survey', 'pills-survey']: 
                    1+2
            #         print(userName, studyType, key,
            #                             hiddenThing, quesText, quesAnswer,
            #                             quesNum, quesType, surveyFamily)
            elif key in ['user-info', 'practice-first',
                           'practice-second', 'practice-third',
                           'practice-survey']:
                1+1
            else:
                print("key: ", key, '\n', 'this was a BUG')
    return points

def compareLearedVsUnlearned(points):
    print(points)
    return points

def combineTwoRows(values):
    sum, count = 0, 0
    for sum2, count2, trashValue in values:
        sum += sum2
        count += count2
    average = sum / count
    return sum, count, average

def correctForLearningEffect(averages):
    aggregate = collections.defaultdict(list)
    for (color, visible, question), value in averages.items():
        aggregate[visible, question].append(value)
    aggregate = {k:combineTwoRows(v) for k, v in aggregate.items()} #

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

def printDictionaryCSV(someDictionary):
    with open('generalDictionaryPrinter.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for key, value in someDictionary.items():
            row = []
            row.extend(value)
            row.extend(key)
            csvwriter.writerow(row)

def printListCSV(someDictionary):
    with open('generalDictionaryPrinter.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for item in someDictionary:
            csvwriter.writerow(item)

points = runVariousSurveys()
rawDataCSV(points)

# this takes the sum and count to calculate averages
averages = calculateTotalAnswersPerQuestion(points)
averages = calculateAverageAnswer(averages)


# make a function that compares first round v. second round of pills, then does the same with running
# someDictionary = compareLearedVsUnlearned(points)
# printListCSV(someDictionary)

# THINGS BROKEN UP # about 52 data-points
makeAveragedCSV(averages)

# this puts all run-yellow with run-red AND pills-red with pills-orange #about 20 data points
# averageTogether = correctForLearningEffect(averages)
# makeAveragedCSV(averageTogether)

# this combines un-yellow with run-red BUT leaves pills and run separate
# pillsAndRunSep = calculatePillsAndRunSeparate(averages)
# makeAveragedCSV(pillsAndRunSep)
