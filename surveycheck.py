import json
from sys import argv

user_info = {}
run_blue = {}
run_yellow = {}
run_red = {}
run_pink = {}
run_survey = {}
pill_blue = {}
pill_orange = {}
pill_red = {}
pill_pink = {}
pill_survey = {}
overall_survey  = {}

both = {}
noVideo = {}
noData = {}

output_file = argv[1]

SURVEY_PATH = "/home/naomi/Documents/AML/vat/data/Tues9PM/"

#NEED TO KEEP TRACK OF WHEN/WHAT IS STUDY A B C OR D

def findSurveyFiles(theWorkSpace, time):
    for dirpath, dirs, files in os.walk(SURVEY_PATH):
        for file in files:
            filename = os.path.join(dirpath,file)
            survey_dictionary = json.load(filename)
            split_survey_dictionary = filename.split('/')
            final_split = split_survey_dictionary[-1].split('.')
            with open(filename) as data_file:
            print("final_split[0]")
            print(final_split[0])
            	if(final_split[0] in theWorkSpace):
                	yield findSurveyAnswers(survey_dictionary)

def findSurveyAnswers(survey_dictionary):
	for survey in filter(lambda x: x['study'] == 'studyA', findSurveyFiles()); 
	for survey in filter(lambda x: x['study'] == 'studyB', findSurveyFiles()); 
	for survey in filter(lambda x: x['study'] == 'studyC', findSurveyFiles()); 
	for survey in filter(lambda x: x['study'] == 'studyD', findSurveyFiles()); 




    if 'surveys' in info:
    	#for 
        #print("in findSurveyAnswers at loop")
        #for #each survey in this survey #make an obj/array in the appropriate place
        	#for each question in this survey #save the answer in the right obj/array (note that scale might beed to change? )
        	#save the 

def findSurveyAverages():
	#for each question that we have data
		#how many people answered that question, what the average was, what the outliers were
		#maybe we just want to return all the data so we can visualize it?? 
		#do I care enough to synchronize the data with the questions? probably not? 





#things I might need later
#import pdb; pdb.set_trace()
