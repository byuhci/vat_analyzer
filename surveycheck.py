import glob
import json
import os
import csv
# from sys import argv

rounds = []

name = 'studyA'
SURVEY_PATH = "/home/naomi/Documents/AML/vat_analyzer/surveyResultsForPython_raw_cleaned_data/"

def runOneVariationOfSurveys(rounds, name):
    outputFile = name #argv[1]
    surveyType = name #argv[1] #value should be 'surveyA' or 'surveyB', etc.

    #check rules based on what kind of survey we're doing
    rulesLocation = name + '.tasks.json'
    convertToFiveRulesLocation = os.path.join(SURVEY_PATH)
    os.chdir(convertToFiveRulesLocation)

    videoAndDataPairings = {}
    videoAndQuestionPairings = {} 

    with open(rulesLocation, 'r') as file:
        fileOfSurveyGuidlines = json.load(file)
    surveys = fileOfSurveyGuidlines['surveys'] #this is a dictionary

    #print(*surveys, sep='\n')

    for key, value in surveys.items(): #loop through each diff survey style ('has-both', 'no-vid', etc)
        #loop through each question in the survey:
        if key not in ['userinfo', 'practice-task', 'empty-task']:
            #print(key) #key values: 'has-both', 'no-vid', etc
            for question in value:
                quesType = question['type'] #likert, likertPercentage, likertTime, etc
                quesNum = ((question['name']).lower()).replace(" ", "") #ques1, ques2, etc
                quesText = question['text']
                videoAndQuestionPairings[key+quesNum] = (quesType,quesNum,quesText)

    allTasks = fileOfSurveyGuidlines['tasks']
    #print(allTasks)
    for task in allTasks: #allTasks is a list of which videos they'll annotate/surveys they'll take & the order
        name = task['name'] #string
        itemType = task['type']
        if itemType not in ['survey']:
            data = task['data']
            if len(data.items())==2: #this means there is no value for the variable "hide" only "timelimit" and "workspace"
                hidden = 'has-both-task' #neither is hidden
            else:
                hidden = data['hide']
                if data['hide']=='data':
                    hidden = 'no-data-task'
                elif data['hide']=='video':
                    hidden = 'no-video-task'
            survey = task['survey']
        else: 
            survey = task['survey']
            hidden = itemType #holds the fact that it is a survey
        videoAndDataPairings[name] = (hidden, survey) 

    #go to the folder with all users' data/results
    destination = os.path.join(SURVEY_PATH, surveyType)
    os.chdir(destination)

    #see what files are in this folder
    glob.glob('*.info.json')

    validUsers = []

    #only allow users 001-045
    validFiles = list(filter(lambda x: x.split('.')[0]<='045.info.json', glob.glob('*.info.json')))#make sure we're ignoring users 2020 and 4040
    #print(validFiles)#shows which user ids are saved in this folder

    for fileName in validFiles:
        #print(validFiles)
        with open(fileName, 'r') as file:
            #print(information['user_id'])
            information = json.load(file)
            #print(fileName)
            userName = fileName[:3]
            #userName = (information['user_id'])[:3]#take substring of file name here
            #print(userName)
            allSurveys = information['surveys']
            #print(allSurveys)
            for key, value in allSurveys.items(): #key=name of video, value={'q1'='ans',...}
                if key not in ['user-info', 'practice-first', 'practice-second', 'practice-third', 'practice-survey']:
                    quesGroupName = videoAndDataPairings[key][1] #SURVEY TYPE aka hat was hidden (like 'has-both' or 'no-video' or 'post-section')
                    #[item for item in videoAndDataPairings if item[0] == key] #gets pair vidName and hiddenThing
                    hiddenThing = videoAndDataPairings[key][0] #less helpful bc all surveys get replaced w/ 'survey'
                    questions = ['question' + str(i+1) for i in range(len(value))]
                    answers = [value[q] for q in questions]
                    for i in range(len(value)): #length of value = number of questions there were in this set
                        quesAnswer = answers[i]
                        quesNum = questions[i]
                        groupSurvey = videoAndDataPairings[key][1] #SURVEY TYPE aka hat was hidden (like 'has-both' or 'no-video' or 'post-section')
                        #the line below is the broken line
                        quesText = videoAndQuestionPairings[groupSurvey+quesNum][2] #actual question 
                        quesType = videoAndQuestionPairings[groupSurvey+quesNum][0] #likert type
                        if (quesType == 'likert' or quesType == 'likertTime'):
                            quesAnswer = int(quesAnswer)+3 #because it was on a scale of -2 to +2 (adjusting it to 1 to 5)
                        rounds.append((userName, surveyType, key, hiddenThing, quesText, quesAnswer, quesNum, quesType, groupSurvey))
    return rounds

rounds = runOneVariationOfSurveys(rounds, 'studyA')
rounds = runOneVariationOfSurveys(rounds, 'studyB')
rounds = runOneVariationOfSurveys(rounds, 'studyC')
rounds = runOneVariationOfSurveys(rounds, 'studyD')

destination = os.path.join(SURVEY_PATH)
os.chdir(destination)

with open('allRawResults.csv','w') as csvfile: 
    csvwriter = csv.writer(csvfile)
    for tup in sorted(rounds): #makes a CSV, actual real file: 
        csvwriter.writerow(tup)
        #print(tup)

#figure out how many videos and data statuses there are
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

averageCalc = {} #sum, count, average

#while there are more combinations
possibilites = (len(possibleVideoNameSets)*len(possibleHiddenValue)*len(possibleQuestionText))
#print(possibilites)
for i in range(0,int(possibilites)):
    for videoDataSet in possibleVideoNameSets:#r2
        for hiddenType in possibleHiddenValue:#r3
            for questionText in possibleQuestionText:#r4
                for round in rounds:
                    if ((round[2]==videoDataSet) and (round[3]==hiddenType) and (round[4]==questionText)):
                        if (videoDataSet+hiddenType+questionText) not in averageCalc:  
                            averageCalc[videoDataSet+hiddenType+questionText] = (round[5], 1, '?', videoDataSet, hiddenType, questionText)
                        else:
                            things = averageCalc.get(videoDataSet+hiddenType+questionText)
                            #print(things)
                            newThings = [int(things[0])+int(round[5]), int(things[1])+1, '?', videoDataSet, hiddenType, round[6], questionText]
                            #print(newTup)
                            averageCalc[videoDataSet+hiddenType+questionText] = newThings



                        
                #averageCalc(questionText) = (videoDataSet, hiddenType, questionText)
    # tup = (questionText, videoDataSet, hiddenType, average)
    # average = summation/counter
    # averageCalc.append(tup)
for key, value in averageCalc.items():
    value[2] = int(value[0])/int(value[1]) 
    print(value)
    #row[2] = int(row[0])/int(row[1]) 

print('\n\n\n\n\n\n')

print(averageCalc)

print('\n\n\n\n\n\n')

with open('averagesPerQuestionPerVideoPerDataResults.csv','w') as csvfile: 
    csvwriter = csv.writer(csvfile)
    for key, value in averageCalc.items(): #makes a CSV, actual real file: 
        csvwriter.writerow(value)
        #print(tup)
        userName = fileName.split('.')[0]
        allSurveys = information['surveys']
        #print('set(allSurveys.keys()): ', set(allSurveys.keys()))
        #print('set(studyInfo.keys()): ', set(studyInfo.keys()))
        #key=name of video, value={'q1'='ans',...}
        for key, value in allSurveys.items():
            # if key in ['run-survey', 'pills-survey']: 
                #print("'run-survey', 'pills-survey' BUG")
                # hiddenThing = 'not applicable'
                # userName is already set, studyType is = studyA/B/C/D
                # hiddenThing, surveyFamily = studyInfo[key]
                # quesText = 
                # quesAnswer = 
                # quesNum = 
                # quesType = 
                # surveyFamily = 
                # if (quesType == 'likert' or quesType == 'likertTime'):
                #         quesAnswer = int(quesAnswer) + 3
                # print('BUG', userName, studyType, key,
                #                         hiddenThing, quesText, quesAnswer,
                #                         quesNum, quesType, surveyFamily)
                # points.append(Point(userName, studyType, key,
                #                         hiddenThing, quesText, quesAnswer,
                #                         quesNum, quesType, surveyFamily))

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
# return points

points = runVariousSurveys()
rawDataCSV(points)

averages = calculateTotalAnswersPerQuestion(points)
averages = calculateAverageAnswer(averages)
makeAveragedCSV(averages)

