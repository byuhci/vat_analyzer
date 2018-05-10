import csv
import scipy.stats
from scipy.stats import mannwhitneyu
from time import strftime


# stuff I found in subjectiveAnswer.py

def mannWhitney(hasData, hasVideo, type, whatLookingAt):  # non parametric test
    f = open('subjective_5may_results/' + type + '______' + numToEnglish[whatLookingAt] + 'wilcoxon.txt', 'w')
    f.write(type + ' numToEnglish[whatLookingAt]: ' + numToEnglish[whatLookingAt] + '\n')
    f.write('comparing hasData to hasVideo: ' + type + '\n')
    # f.write("hasData: " + str(hasData))
    # f.write("hasVideo:" + str(hasVideo))
    f.write(str(mannwhitneyu(hasData, hasVideo)) + '\n')
    # f.write(str(scipy.stats.wilcoxon(hasData, hasVideo)))
    f.close()


def readInData(whatLookingAt):
    # hidden	% correct	% mislabelled	% off	% wrong	% missed
    has_video_pills = []
    has_data_pills = []
    has_video_run = []
    has_data_run = []

    videoSetOfList = []
    dataSetOfList = []
    # read in percentComplete.csv # for percent complete, paired with hidden value

    # format of percentCompleteAllColumns.csv
    # hidden	correct	not type & bounds	type & not bounds	not type & not bounds	missed
    # hidden	% correct	% mislabelled	% off	% wrong	% missed	not type, (bounds || not bounds)
    first = True
    with open('stackedData.csv', 'r') as csvfile:
        allRows = csv.reader(csvfile, delimiter=',')  # , quotechar='|'
        for row in allRows:
            # print(len(row))
            for column in row:
                if first:
                    continue
                if row[0] == 'data' and row[7] == 'running':  # data is hidden
                    has_data_run.append(row[whatLookingAt])
                elif row[0] == 'data' and row[7] == 'pills':  # data is hidden
                    has_data_pills.append(row[whatLookingAt])
                elif row[0] == 'video' and row[7] == 'running':  # video is hidden
                    has_video_run.append(row[whatLookingAt])
                elif row[0] == 'video' and row[7] == 'pills':  # video is hidden
                    # store in other
                    has_video_pills.append(row[whatLookingAt])
            first = False

    return has_data_run, has_video_run, has_data_pills, has_video_pills


# hidden	correct	type & bounds	type & not bounds	not type & not bounds	missed
numToEnglish = {
    0: 'hidden',  # what was hidden (video or data)
    1: 'correct (type and bounds)',  # (got everything right)
    2: 'mislabeled (not type and bounds)',  #
    3: 'off (type and not bounds)',
    4: 'wrong (not type and not bounds)',
    5: 'missed',
    6: 'mislabled AND off (ANY not type)',  # what is happening here??
    7: 'combo (anything with wrong type)'
    # we actually want it to be ORANGE and RED (in other words, noting ANYTIME that type is wrong (whether bounds are right or wrong)
    # this would be mislabeled (aka 2) OR wrong (aka 4)
}


def main():
    for key in numToEnglish.keys():
        if numToEnglish.get(key) == 'combo':
            continue
        whatLookingAt = key
        print(key)
        has_data_run, has_video_run, has_data_pills, has_video_pills = readInData(whatLookingAt)
        mannWhitney(has_data_run, has_video_run, 'run', whatLookingAt) # just runs that by itself aka regularly
        mannWhitney(has_data_pills, has_video_pills, 'pills', whatLookingAt)

def combo():
    # global vars = the best
    whatLookingAt = 2  # changing this changes everything
    has_data_run, has_video_run, has_data_pills, has_video_pills = readInData(whatLookingAt)
    # mannWhitney(has_data_run, has_video_run, 'run') # just runs that by itself aka regularly
    # mannWhitney(has_data_pills, has_video_pills, 'pills')

    whatLookingAt = 4
    second_has_data_run, second_has_video_run, second_has_data_pills, second_has_video_pills = readInData(whatLookingAt)
    whatLookingAt = 7
    mannWhitney(second_has_data_run + has_data_run, second_has_video_run + has_video_run, 'run', whatLookingAt)
    mannWhitney(second_has_data_pills + has_data_pills, second_has_video_pills + has_video_pills, 'pills', whatLookingAt)



combo()