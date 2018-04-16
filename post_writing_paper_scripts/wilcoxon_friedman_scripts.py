import csv
import scipy.stats
from scipy.stats import mannwhitneyu
from time import strftime


# stuff I found in subjectiveAnswer.py

def wilcoxonTest(hasData, hasVideo):  # non parametric test
    print(strftime("%Y-%m-%d %H:%M"))
    f = open('wilcoxon_' + strftime("%Y-%m-%d %H:%M") + '.txt', 'w')
    f.write('\n')
    # f.write(str(mannwhitneyu(hasData, hasVideo)))
    f.write(str(scipy.stats.wilcoxon(hasData, hasVideo)))
    f.close()


def friedmanLikertTest(analyzableData):
    print(strftime("%Y-%m-%d %H:%M"))


def readInData():
    hasVideo = []
    hasData = []
    # read in percentComplete.csv # for percent complete, paired with hidden value
    with open('percentComplete.csv', 'r') as csvfile:
        allRows = csv.reader(csvfile, delimiter=',')  # , quotechar='|'
        for row in allRows:
            if row[1] == 'data':  # data is hidden
                # store in one place
                hasVideo.append(row[0])
            elif row[1] == 'video':  # video is hidden
                # store in other
                hasData.append(row[0])
            elif row[1] == 'none':
                # do nothing
                1 + 1
            else:
                print(row[1])
            # print(row[0], row[1])
    return hasData, hasVideo


hasData, hasVideo = readInData()
print(len(hasVideo), len(hasData))
wilcoxonTest(hasData, hasVideo)
print('finished')
