import glob
import json
import os
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
videoAndDataPairings = []
videoAndQuestionPairings = [] #holds video name, question type, ques number, and question text

with open(rulesLocation, 'r') as file:
    fileOfSurveyGuidlines = json.load(file)

    surveys = fileOfSurveyGuidlines['surveys']
    #print(*surveys, sep='\n')

    for survey in surveys:
        print(survey)
        #quesDetailsOne = survey[1]
        #print(quesDetailsOne)
        #holds video name (key), question type, question number, and question text


    allTasks = fileOfSurveyGuidlines['tasks']
    #print(allTasks)
    for task in allTasks:
        name = task['name']
        #print(name)

        #error on next line: 
        #data = task['data']
        #print(data)
        #situation = task['data']'s ['hide']
        #videoAndDataPairings.append((name, situation))





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
                ques1 = value['question1']
                ques2 = value['question2']
                ques3 = value['question3']
                ques4 = value['question4']
                rounds.append((userName, surveyType, key, ques1, ques2, ques3, ques4))
#print(*sorted(rounds), sep='\n') #easy to look at tuples
#for tup in sorted(rounds): #makes a CSV: 
 #   print(*tup, sep=',')





#things to put in tuple: userName, surveyType, key (aka name of video), ques1-4


#grab their user id, grab name of first video
#make a tuple with name, video name, and then Q1-4 data points
#repeat for each video
