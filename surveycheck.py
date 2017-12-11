import glob
import json
import os
import csv
from sys import argv

outputFile = argv[1]

SURVEY_PATH = "/home/naomi/Documents/AML/vat/data/surveyResultsForPython/"

#see which folder we want to use, pick set of rules 
surveyType = argv[1]#value should be 'surveyA' or 'surveyB', etc.

#check rules based on what kind of survey we're doing
rulesLocation = argv[1] + '.tasks.json'
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
#print(*sorted(videoAndQuestionPairings), sep='\n')
#print(videoAndQuestionPairings, '\n\n\n\n\n')


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

rounds = []
validUsers = []

#only allow users 001-045
validFiles = list(filter(lambda x: x.split('.')[0]<='045', glob.glob('*.info.json')))#make sure we're ignoring users 2020 and 4040
#print(validFiles)#shows which user ids are saved in this folder

for fileName in validFiles:
    #print(validFiles)
    with open(fileName, 'r') as file:
        #print(information['user_id'])
        information = json.load(file)
        userName = information['user_id']
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
                    #print(userName, surveyType, key, hiddenThing, quesText, quesAnswer, quesNum, quesType)
                    rounds.append((userName, surveyType, key, hiddenThing, quesText, quesAnswer, quesNum, quesType))
        

destination = os.path.join(SURVEY_PATH)
os.chdir(destination)

with open(surveyType+'autoResults.csv','w') as csvfile: 
    csvwriter = csv.writer(csvfile)
    for tup in sorted(rounds): #makes a CSV, actual real file: 
        csvwriter.writerow(tup)

# with open('asdf.txt','w') as outfile:
#     outfile.write('asdf')

# for tup in sorted(rounds): #makes a CSV, printed to terminal: 
#     print(*tup, sep=',')