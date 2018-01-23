import json 
import csv
from collections import defaultdict

SURVEY_PATH = '/home/naomi/Documents/AML/vat_analyzer/surveyResultsForPython_raw_cleaned_data____orig'

def findFScores():
	with open('perPersonFScores.json', 'r') as file:
		userFScores = json.load(file)

	eachUser = defaultdict(lambda: [0, 0, 0])
	for key, value in userFScores.items():
		print(key)
		for video in value:
    		# sum, count, average
			#print(video)
			eachUser[key][0] = eachUser[key][0] + value[video]
			# print(value[video])
			eachUser[key][1] += 1

	for value in eachUser.values():
		value[2] = value[0] / value[1]
		print(value[0], value[1], value[2])

	#print(eachUser)
	return eachUser

def makeAveragedCSV(averages):
	with open('perPersonFScore.csv', 'w') as csvfile:
		csvwriter = csv.writer(csvfile)
		for key, value in averages.items():
			row = [4] # there will always be four things bc key, sum, count, averages 
			row[0] = key
			row.extend(value)
			csvwriter.writerow(row)

var = findFScores()
makeAveragedCSV(var)