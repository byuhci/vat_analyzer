from time import strftime
import csv
from collections import defaultdict, namedtuple
from scipy.stats import mannwhitneyu
import numpy as np

datapoint = namedtuple('datapoint', 'saw setOfQuestions	question taskType')


def readInData():
    # adjusted_scale_subjectiveData.csv
    # saw	answer	questionNum	set of questions	QUESTION	task-type
    hasData = defaultdict(list)
    hasVideo = defaultdict(list)
    something = defaultdict(list)
    print(strftime("%Y-%m-%d %H:%M"))
    with open('adjusted_scale_subjectiveData.csv', 'r') as csvfile:
        allRows = csv.reader(csvfile, delimiter=',')  # , quotechar='|'
        for row in allRows:
            if row[4] == 'free-response':
                continue
            newpoint = datapoint(row[0], row[3], row[4], row[5]) # 'eitherPillOrRun' row[5] # this says run or pill
            something[newpoint].append(int(row[1]))
            # something[str(row[3:6])].add(int(row[1]))

    return hasData, hasVideo, something


def printRawData(someData):
    f = open('results_mann_whitney/subjective/subjectiveData.txt', 'w')
    f.write('########################################################\n')
    for key, value in someData.items():
        f.write(str(key))
        f.write('\n')
        f.write(str(value))
        f.write('\n\n')
    f.write('########################################################')
        # f.write(str(len(value), key, value))


def selfEval(someData):
    dupli = someData
    f = open('results_mann_whitney/subjective/selfEval.txt', 'w')
    f.write('########################################################\n')
    f.write('selfEval\n\n')
    for key, value in someData.items():
        if getattr(key, 'saw') == 'both':
            continue
        for matchingKey, matchingValue in dupli.items():
            if getattr(matchingKey, 'saw') == 'both':
                continue
            if getattr(key, 'setOfQuestions') == getattr(matchingKey, 'setOfQuestions') and \
                    getattr(key, 'question') == getattr(matchingKey, 'question') \
                    and getattr(key, 'saw') == getattr(matchingKey, 'saw'):
                continue
            elif getattr(key, 'question') == getattr(matchingKey, 'question'):
                f.write(str(key) + '\n' + str(matchingKey) + '\n')
                f.write(str(value) + '\n' + str(matchingValue) + '\n')
                f.write(str(mannwhitneyu(value, matchingValue)) + '\n')
                f.write('\n\n')
        # print(key) # this part was used to find the means the night before the paper was due
        # print(np.mean(value))
        # print('\n')
        # # f.write(str('\n\n' + key))
        # # f.write(str(value))
    f.write('########################################################\n')


def howEssential(someData):
    f = open('results_mann_whitney/'
             'subjective/howEssential.txt', 'w')
    f.write('########################################################\n')
    f.write('howEssential: \n\n')
    for key, value in someData.items():
        for matchingKey, matchingValue in someData.items():
            if getattr(key, 'setOfQuestions') == 'post-section' and \
                    getattr(matchingKey, 'setOfQuestions') == 'post-section' and \
                    getattr(key, 'question')[:12] == getattr(matchingKey, 'question')[:12]:
                f.write(str(key) + '\n' + str(matchingKey) + '\n')
                f.write(str(value) + '\n' + str(matchingValue) + '\n')
                f.write(str(mannwhitneyu(value, matchingValue)) + '\n')
                f.write('\n\n')
    f.write('########################################################')


def howSatisfied(someData):
    f = open('results_mann_whitney/subjective/howSatisfied.txt', 'w')
    f.write('########################################################\n')

    f.write('howSatisfied: \n\n')
    for key, value in someData.items():
        for matchingKey, matchingValue in someData.items():
            if getattr(key, 'question')[:10] == 'satisfied:' and \
                    getattr(matchingKey, 'question')[:10] == 'satisfied:':
                f.write(str(key) + '\n' + str(matchingKey) + '\n')
                f.write(str(value) + '\n' + str(matchingValue) + '\n')
                f.write(str(mannwhitneyu(value, matchingValue)) + '\n')
                f.write('\n\n')
    f.write('########################################################')


hasData, hasVideo, something = readInData()
printRawData(something)
selfEval(something)
howEssential(something)
howSatisfied(something)

