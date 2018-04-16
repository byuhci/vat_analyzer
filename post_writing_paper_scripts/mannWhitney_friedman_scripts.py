import csv
import scipy.stats
from scipy.stats import mannwhitneyu
from time import strftime


# stuff I found in subjectiveAnswer.py

def mannWhitney(hasData, hasVideo):  # non parametric test
    print(strftime("%Y-%m-%d %H:%M"))
    f = open('results_mann_whitney/wilcoxon_' + numToEnglish[whatLookingAt] + '.txt', 'w')
    f.write('numToEnglish[whatLookingAt]: ' + numToEnglish[whatLookingAt] + '\n')
    f.write('comparing hasData to hasVideo: ' + '\n')
    # f.write("hasData: " + str(hasData))
    # f.write("hasVideo:" + str(hasVideo))
    f.write(str(mannwhitneyu(hasData, hasVideo)) + '\n')
    # f.write(str(scipy.stats.wilcoxon(hasData, hasVideo)))
    f.close()


def friedmanLikertTest(analyzableData):
    print(strftime("%Y-%m-%d %H:%M"))


def readInData():
    # hidden	% correct	% mislabelled	% off	% wrong	% missed
    hasVideo = []
    hasData = []

    videoSetOfList = []
    dataSetOfList = []
    # read in percentComplete.csv # for percent complete, paired with hidden value

    # format of percentCompleteAllColumns.csv
    # hidden	correct	not type & bounds	type & not bounds	not type & not bounds	missed
    # hidden	% correct	% mislabelled	% off	% wrong	% missed	not type, (bounds || not bounds)
    first = True
    with open('percentCompleteAllColumns.csv', 'r') as csvfile:
        allRows = csv.reader(csvfile, delimiter=',')  # , quotechar='|'
        for row in allRows:
            # print(len(row))
            for column in row:
                if first:
                    continue

                if row[0] == 'data':  # data is hidden
                    # store in one place
                    hasVideo.append(row[whatLookingAt])
                elif row[0] == 'video':  # video is hidden
                    # store in other
                    hasData.append(row[whatLookingAt])
            first = False

    return hasData, hasVideo

# global vars = the best
whatLookingAt = 6


numToEnglish = {
    0: 'hidden',
    1: 'correct (type and bounds)',
    2: 'mislabeled (not type and bounds)',
    3: 'off (type and not bounds)',
    4: 'wrong (not type and not bounds)',
    5: 'missed',
    6: 'mislabled AND off (ANY not type)'
}



hasData, hasVideo = readInData()
print(len(hasVideo), len(hasData))
print("hasVideo", hasVideo)
print("hasData", hasData)
mannWhitney(hasData, hasVideo)
print('finished')
