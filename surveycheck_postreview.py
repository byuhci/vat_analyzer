import glob
import json
import os
import csv
from sys import argv

name = 'studyA'
SURVEY_PATH = "/home/naomi/Documents/AML/vat_analyzer/surveyResultsForPython_raw_cleaned_data/"

def runVariousSurveys():
    rounds = []
    rounds = runOneVariationOfSurveys('studyA')
    rounds += runOneVariationOfSurveys('studyB')
    rounds += runOneVariationOfSurveys('studyC')
    rounds += runOneVariationOfSurveys('studyD')
    return rounds

def rawDataCSV(rounds):
    destination = os.path.join(SURVEY_PATH)
    os.chdir(destination)

    with open('allRawResults.csv','w') as csvfile: 
        csvwriter = csv.writer(csvfile)
        for tup in sorted(rounds): # makes a CSV, actual real file: 
            csvwriter.writerow(tup)

def calculateTotalAnswersPerQuestion(rounds): 
    # figure out how many videos and data statuses there are
    possibleVideoNameSets = []
    possibleHiddenValue = []
    possibleQuestionText = []
    possibleSurveyGroupTypes = []
    possibleSurveyTypes = []
    for round in rounds:
        if round[2] not in possibleVideoNameSets:
            possibleVideoNameSets.append(round[2])

        if round[3] not in possibleHiddenValue:
            possibleHiddenValue.append(round[3])

        if round[4] not in possibleQuestionText:
            possibleQuestionText.append(round[4])

        if round[8] not in possibleSurveyGroupTypes:
            possibleSurveyGroupTypes.append(round[8])

        if round[1] not in possibleSurveyTypes:
            possibleSurveyTypes.append(round[1])

    averageCalc = {} # sum, count, average
    possibilites = (len(possibleVideoNameSets)*len(possibleHiddenValue)*len(possibleQuestionText))
    for i in range(0,int(possibilites)):
        for videoDataSet in possibleVideoNameSets: # r2
            for hiddenType in possibleHiddenValue: # r3
                for questionText in possibleQuestionText: # r4
                    for round in rounds:
                        if ((round[2]==videoDataSet) and (round[3]==hiddenType) and (round[4]==questionText)):
                            if (videoDataSet+hiddenType+questionText) not in averageCalc:  
                                averageCalc[videoDataSet+hiddenType+questionText] = (round[5], 1, '?', videoDataSet, hiddenType, questionText)
                            else:
                                things = averageCalc.get(videoDataSet+hiddenType+questionText)
                                # print(things)
                                newThings = [int(things[0])+int(round[5]), int(things[1])+1, '?', videoDataSet, hiddenType, round[6], questionText]
                                # print(newTup)
                                averageCalc[videoDataSet+hiddenType+questionText] = newThings
    return averageCalc

def calculateAverageAnswer(averageCalc):
    for key, value in averageCalc.items():
        value[2] = int(value[0])/int(value[1]) 
        # print(value[2])
    return averageCalc

def makeAveragedCSV(averageCalc):
    with open('averagesPerQuestionPerVideoPerDataResults.csv','w') as csvfile: 
        csvwriter = csv.writer(csvfile)
        for key, value in averageCalc.items(): # makes a CSV, actual real file: 
            csvwriter.writerow(value)

def runOneVariationOfSurveys(name):
    outputFile = name # see which folder we want to use, pick set of rules/pairings 
    surveyType = name # check rules based on what kind of survey we're doing
    rulesLocation = name + '.tasks.json'
    convertToFiveRulesLocation = os.path.join(SURVEY_PATH)
    os.chdir(convertToFiveRulesLocation)

    videoAndDataPairings = {}
    videoAndQuestionPairings = {} 
    with open(rulesLocation, 'r') as file:
        fileOfSurveyGuidlines = json.load(file)
    surveys = fileOfSurveyGuidlines['surveys'] # this is a dictionary

    for key, value in surveys.items(): # loop through each diff survey style ('has-both', 'no-vid', etc)
        # loop through each question in the survey:
        if key not in ['userinfo', 'practice-task', 'empty-task']:
            # print(key) # key values: 'has-both', 'no-vid', etc
            for question in value:
                quesType = question['type'] # likert, likertPercentage, likertTime, etc
                quesNum = ((question['name']).lower()).replace(" ", "") #ques1, ques2, etc
                quesText = question['text']
                videoAndQuestionPairings[key+quesNum] = (quesType,quesNum,quesText)
    # print('videoAndQuestionPairings', videoAndQuestionPairings, '\n')

    allTasks = fileOfSurveyGuidlines['tasks']
    for task in allTasks: # allTasks is a list of which videos they'll annotate/surveys they'll take & the order
        name = task['name'] # string
        itemType = task['type']
        if itemType not in ['survey']:
            data = task['data']
            if len(data.items())==2: # this means there is no value for the variable "hide" only "timelimit" and "workspace"
                hidden = 'has-both-task' # neither is hidden
            else:
                hidden = data['hide']
                if data['hide']=='data':
                    hidden = 'no-data-task'
                elif data['hide']=='video':
                    hidden = 'no-video-task'
            survey = task['survey']
        else: 
            survey = task['survey']
            hidden = itemType # holds the fact that it is a survey
        videoAndDataPairings[name] = (hidden, survey) 
    # print('videoAndDataPairings', videoAndDataPairings, '\n')
    return getUserStudyInfo(videoAndDataPairings, videoAndQuestionPairings, surveyType)

def getUserStudyInfo(videoAndDataPairings, videoAndQuestionPairings, surveyType):
    # go to the folder with all users' data/results
    destination = os.path.join(SURVEY_PATH, surveyType)
    os.chdir(destination)

    # see what files are in this folder
    glob.glob('*.info.json')

    # only allow users 001-045
    validFiles = list(filter(lambda x: x.split('.')[0]<='045.info.json', glob.glob('*.info.json')))#make sure we're ignoring users 2020 and 4040
    # print(validFiles) # shows which user ids are saved in this folder
    return putTuplesInRounds(validFiles, videoAndDataPairings, videoAndQuestionPairings, surveyType)

def putTuplesInRounds(validFiles, videoAndDataPairings, videoAndQuestionPairings, surveyType):
    rounds = []
    for fileName in validFiles:
        # print(validFiles)
        with open(fileName, 'r') as file:
            # print(information['user_id'])
            information = json.load(file)
            # print(fileName)
            userName = fileName[:3]
            # userName = (information['user_id'])[:3]#take substring of file name here
            # print(userName)
            allSurveys = information['surveys']
            # print(allSurveys)
            for key, value in allSurveys.items(): # key=name of video, value={'q1'='ans',...}
                if key not in ['user-info', 'practice-first', 'practice-second', 'practice-third', 'practice-survey']:
                    quesGroupName = videoAndDataPairings[key][1] # SURVEY TYPE aka hat was hidden (like 'has-both' or 'no-video' or 'post-section')
                    # [item for item in videoAndDataPairings if item[0] == key] #gets pair vidName and hiddenThing
                    hiddenThing = videoAndDataPairings[key][0] # less helpful bc all surveys get replaced w/ 'survey'
                    questions = ['question' + str(i+1) for i in range(len(value))]
                    answers = [value[q] for q in questions]
                    for i in range(len(value)): # length of value = number of questions there were in this set
                        quesAnswer = answers[i]
                        quesNum = questions[i]
                        groupSurvey = videoAndDataPairings[key][1] # SURVEY TYPE aka what was hidden (like 'has-both' or 'no-video' or 'post-section')
                        quesText = videoAndQuestionPairings[groupSurvey+quesNum][2] # actual question 
                        quesType = videoAndQuestionPairings[groupSurvey+quesNum][0] # likert type
                        if (quesType == 'likert' or quesType == 'likertTime'):
                            quesAnswer = int(quesAnswer)+3 # because it was on a scale of -2 to +2 (adjusting it to 1 to 5)
                        rounds.append((userName, surveyType, key, hiddenThing, quesText, quesAnswer, quesNum, quesType, groupSurvey))
    return rounds

def correctForLearningEffect(averageCalc):
    print('\n')
    for i in range(len(averageCalc)):
        for j in range(len(averageCalc)):
            print('\n')
            # need data/vid type ()to match and question name to match
            # if ((rounds[i][3] == rounds[j][3]) && (rounds[i][4] == rounds[j][4])):
                # print(rounds[i][3], rounds[i][4]) # it is a match
                # so i will merge them




rounds = runVariousSurveys()
rawDataCSV(rounds)

averageCalc = calculateTotalAnswersPerQuestion(rounds)
averageCalc = calculateAverageAnswer(averageCalc)
print(averageCalc)
# averageCalc = correctForLearningEffect(averageCalc)

makeAveragedCSV(averageCalc)