import csv
import scipy.stats
from scipy.stats import mannwhitneyu
from time import strftime


# stuff I found in subjectiveAnswer.py

def mannWhitney(hasData, hasVideo):  # non parametric test
    print(strftime("%Y-%m-%d %H:%M"))
    f = open('wilcoxon_' + strftime("%Y-%m-%d %H:%M") + '.txt', 'w')
    f.write('\n')
    f.write(str(mannwhitneyu(hasData, hasVideo)))
    # f.write(str(scipy.stats.wilcoxon(hasData, hasVideo)))
    f.close()


def friedmanLikertTest(analyzableData):
    print(strftime("%Y-%m-%d %H:%M"))


def readInData():
    # hidden	% correct	% mislabelled	% off	% wrong	% missed
    hasVideo = []
    hasData = []
    # read in percentComplete.csv # for percent complete, paired with hidden value
    # format of various_percents_for_mann_whitney.csv
    # hidden,correct,"not type, bounds","type, not bounds","not type, not bounds",missed,"not type, (bounds || not bounds)"
    # hidden,% correct,% mislabelled,% off,% wrong,% missed,% mislabelled && off
    with open('various_percents_for_mann_whitney.csv', 'r') as csvfile:
        allRows = csv.reader(csvfile, delimiter=',')  # , quotechar='|'
        for row in allRows:
            if row[0] == 'data':  # data is hidden
                # store in one place
                hasVideo.append(row[0])
            elif row[0] == 'video':  # video is hidden
                # store in other
                hasData.append(row[0])

    return hasData, hasVideo


hasData, hasVideo = readInData()
print(len(hasVideo), len(hasData))
mannWhitney(hasData, hasVideo)
print('finished')
