import csv
import scipy.stats
from scipy.stats import mannwhitneyu
from time import strftime


# stuff I found in subjectiveAnswer.py

def mannWhitney(hasData, hasVideo):  # non parametric test
    print(strftime("%Y-%m-%d %H:%M"))
    f = open('results_mann_whitney/wilcoxon_' + strftime("%Y-%m-%d %H:%M") + '.txt', 'w')
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
    # format of various_percents_for_mann_whitney.csv
    # hidden,correct,"not type, bounds","type, not bounds","not type, not bounds",missed,"not type, (bounds || not bounds)"
    # hidden,% correct,% mislabelled,% off,% wrong,% missed,% mislabelled && off
    with open('various_percents_for_mann_whitney.csv', 'r') as csvfile:
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
whatLookingAt = 1


numToEnglish = {
    0: 'hidden',
    1: 'correct',
    2: 'mislabeled',
    3: 'off',
    4: 'wrong',
    5: 'missed',
    6: 'mislabled AND off'
}



hasData, hasVideo = readInData()
print(len(hasVideo), len(hasData))
print("hasVideo", hasVideo)
print("hasData", hasData)
mannWhitney(hasData, hasVideo)
print('finished')
