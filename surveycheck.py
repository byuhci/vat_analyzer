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

SURVEY_PATH = "/home/austin/workspacegold"

def findSurveyFiles(theWorkSpace, time):
    for root, dirs, files in os.walk(SURVEY_PATH):
        for file in files:
            filename = os.path.join(root,file)
            survey_filename = json.load(data_file)
            split_survey_filename = filename.split('/')
            final_split = split_survey_filename[-1].split('.')
            with open(filename) as data_file:
            # print("final_split[0]")
            # print(final_split[0])
            	if(final_split[0] in theWorkSpace):
                	return findSurveyAnswers(survey_filename)
    return "No surveys in hardcoded directory"

def findSurveyAnswers(survey_filename):
    for surveys in survey_filename:
        #print("in findSurveyAnswers at loop")
        #for #each survey in this survey #make an obj/array in the appropriate place
        	#for each question in this survey #save the answer in the right obj/array (note that scale might beed to change? )
        	#save the 
    	return "cool error message because the files didn't have surveys?!"

def findSurveyAverages():
	#for each question that we have data
		#how many people answered that question, what the average was, what the outliers were
		#maybe we just want to return all the data so we can visualize it?? 
		#do I care enough to synchronize the data with the questions? probably not? 
	return "not doing anything here yet"