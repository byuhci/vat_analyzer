import glob
import json
import os
import csv
from sys import argv

outputFile = argv[1]

SURVEY_PATH = "/home/naomi/Documents/AML/vat/data/surveyResultsForPython/"

#see which folder we want to use, pick set of rules 
surveyType = argv[1]

#check rules based on what kind of survey we're doing
rulesLocation = argv[1] + '.tasks.json'
convertToFiveRulesLocation = os.path.join(SURVEY_PATH)
os.chdir(convertToFiveRulesLocation)

#store name of video with "situation" type
videoAndDataPairings = {}
videoAndQuestionPairings = {} #holds video name, question type, ques number, and question text

with open(rulesLocation, 'r') as file:
    fileOfSurveyGuidlines = json.load(file)
surveys = fileOfSurveyGuidlines['surveys'] #this is a dictionary
#print(*surveys, sep='\n')
#print(surveys)
#exampleThing = {"surveys": {"empty-task": [],"practice-task": [{"type": "likert","name": "Question1","text": "After the practice rounds, you will be given a survey after each task. Most questions will be on a scale of one to five."}]}}

for key, value in surveys.items(): #loop through each diff survey style
    #loop through each question in the survey:
    if key not in ['userinfo', 'practice-task', 'empty-task']:
        #print(key)
        for question in value:
            #print(question)
            quesType = question['type']
            #print(quesType)
            quesNum = question['name']
            quesText = question['text']
            #print("quesText: ", quesText)
            videoAndQuestionPairings[key] = (quesType,quesNum,quesText)

            #print(key,quesType,quesNum,quesText)
            #holds video name (key), question type, question number, and question text
    #else:
        #print("reject: ", key)
#print(videoAndQuestionPairings)
#print(*sorted(videoAndQuestionPairings), sep='\n')

allTasks = fileOfSurveyGuidlines['tasks']
#print(allTasks)
for task in allTasks: #allTasks is a list
    #print(task)
    name = task['name'] #string
    itemType = task['type']
    if itemType not in ['survey']:
        #print(itemType)
        data = task['data']
        #print(data)
        #print(len(data.items()))
        if len(data.items())==2:
            hidden = 'has-both-task' #neither is hidden
        else:
            hidden = data['hide']
            #print(hidden)
            if data['hide']=='data':
                hidden = 'no-data-task'
            elif data['hide']=='video':
                hidden = 'no-video-task'
        #print(name, hidden)
        survey = task['survey']
    else: 
        #print(task)
        survey = task['survey']
        hidden = itemType #holds the fact that it is a survey
        #print(name, hidden, survey)
    #videoAndDataPairings.append((name, hidden, survey))
    videoAndDataPairings[name] = (hidden, survey) 
    #print(name, hidden, survey)

#print(*videoAndDataPairings, sep='\n')
#print(videoAndDataPairings)


#go to the correct folder
destination = os.path.join(SURVEY_PATH, surveyType)
os.chdir(destination)

#see what files are in this folder
glob.glob('*.info.json')

rounds = []

#only allow users 001-045
validFiles = list(filter(lambda x: x.split('.')[0]<='045', glob.glob('*.info.json')))#make sure we're ignoring 2020 and 4040
#print(validFiles)
for fileName in validFiles:
    #print(validFiles)
    with open(fileName, 'r') as file:
        #print(information['user_id'])
        information = json.load(file)
        userName = information['user_id']
        allSurveys = information['surveys']
        #print(type(allSurveys))
        for key, value in allSurveys.items():
            if key not in ['user-info', 'practice-first', 'practice-second', 'practice-third', 'practice-survey']:
                quesGroupName = videoAndDataPairings[key][1]
                #[item for item in videoAndDataPairings if item[0] == key] #gets pair vidName and hiddenThing
                #print(quesGroupName)
                hiddenThing = videoAndDataPairings[key][0]
                #print(hiddenThing)
                # print(key, value)
                # print(value.values())
                # print(len(value))
                questions = ['question' + str(i+1) for i in range(len(value))]
                answers = [value[q] for q in questions]
                for i in range(len(value)):
                    quesAnswer = answers[i]
                    quesNum = questions[i]
                    groupSurvey = videoAndDataPairings[key][1]
                    #print(groupSurvey)
                    quesText = videoAndQuestionPairings[groupSurvey][2]
                    rounds.append((userName, surveyType, key, hiddenThing, quesText, quesAnswer, quesNum, quesType))


                    #print(quesText)
                    #key = name of video


                    #print(quesAnswer, quesNum)
                    #print(hiddenThing)#quesAnswer, quesNum
                    #quesText = videoAndQuestionPairings[hiddenThing][2] #quesType,quesNum,quesText
                    #print(quesAnswer, quesNum, quesText)
                    # quesType = 
                    # quesGroup = 
                    # print(quesAnswer, quesNum) #quesText, quesType)
                
                    #rounds.append(userName, surveyType, key, hiddenThing, quesAnswer, quesText, quesNum, quesType)

#print(*sorted(rounds), sep='\n') #easy to look at tuples

# with open(surveyType+'results.csv','w') as csvfile: 
#     csvwriter = csv.writer(csvfile,delimiter='^')
#     for tup in sorted(rounds): #makes a CSV: 
#         print('^'.join(tup))
#         csvwriter.writerow('^'.join(tup))

# with open('asdf.txt','w') as outfile:
#     outfile.write('asdf')

for tup in sorted(rounds): #makes a CSV: 
     print(*tup, sep=',')