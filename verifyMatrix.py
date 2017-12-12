import json
#import ankura
import numpy as np
import copy

FILE = 'perpersonconfusion.json'

video_lengths = {"cane.cane-vid1-dat2" : 107.26, "cane.cane-vid3-dat3" : 86.91, "cane.cane-yellow" : 73.81, "newrun.run-pink" : 640.70, "newrun.run-thurs-seven-attempt" : 641.02, "newrun.Run-thurs-five-fixed-finally" : 668.36, "newrun.run-thurs-six-finally" : 676.13, "pill.pills-pink" :  616.23, "pill.pills-blue" : 612.22, "pill.pills-orange" : 621.25, "pill.pills-red" : 629.30 }
run_workspaces = ["newrun.run-pink", "newrun.run-thurs-seven-attempt", "newrun.Run-thurs-five-fixed-finally", "newrun.run-thurs-six-finally"]
cane_andor_practice_workspaces = ["cane.cane-vid1-dat2", "cane.cane-vid3-dat3", "cane.cane-yellow"]
pill_workspaces = ["pill.pills-pink", "pill.pills-blue", "pill.pills-orange", "pill.pills-red"]

with open(FILE, 'r') as fp:
    myFile = json.load(fp)

def putInNumpyMatrix(perPersonConfusionMatrices):
    new_ppcm = copy.deepcopy(perPersonConfusionMatrices)
    f_scores_ppcm = copy.deepcopy(perPersonConfusionMatrices)
    for person in perPersonConfusionMatrices:
        for workspace in perPersonConfusionMatrices[person]:
            c = createConfusion(perPersonConfusionMatrices, person, workspace)
            matrix = [[0] * 3 for q in range(3)]
            print(person)
            print(workspace)
            if workspace in run_workspaces:
                for i, k in enumerate(['None', 'run', 'skip']):
                    print(c)
                    row = c[k]
                    for j, kk in enumerate(['None', 'run', 'skip']):
                        val = row.get(kk,0)
                        matrix[i][j] = val
            elif workspace in cane_andor_practice_workspaces:
                for i, k in enumerate(['None', 'ground']):
                    row = c[k]
                    for j, kk in enumerate(['None', 'ground']):
                        val = row.get(kk,0)
                        matrix[i][j] = val
            elif workspace in pill_workspaces:
                for i, k in enumerate(['None', 'move', 'pill']):
                    row = c[k]
                    for j, kk in enumerate(['None', 'move', 'pill']):
                        val = row.get(kk,0)
                        matrix[i][j] = val
            np_arr = np.array(matrix)
            f_score = getFFromConfusion(np_arr)
            new_ppcm[person][workspace] = np_arr
            f_scores_ppcm[person][workspace] = f_score
    return new_ppcm, f_scores_ppcm

def createConfusion(perPersonConfusionMatrices, person, workspace):
    c = {}
    for gold in perPersonConfusionMatrices[person][workspace]:
        for user in perPersonConfusionMatrices[person][workspace][gold]:
            if gold in c:
                c[gold].update({user : perPersonConfusionMatrices[person][workspace][gold][user]})
            else:
                c[gold] = {}
                c[gold].update({user : perPersonConfusionMatrices[person][workspace][gold][user]})
    return c

def getFFromConfusion(c):
    #note: recall row, axis=1 is row. precision column, axis=0 is column
    print("c.diagonal" + str(c.diagonal()) + " c.sum(axis=1) " + str(c.sum(axis=1)) + " c.sum(axis=0) " + str(c.sum(axis=0)))
    #will both be 1 x 3 matrices
    # recall = c.diagonal()/c.sum(axis=1)
    with np.errstate(divide='ignore'):
        recall = c.diagonal() / c.sum(axis=1)
        recall[np.isnan(recall)] = 0
        precision = c.diagonal()/c.sum(axis=0)
        precision[np.isnan(precision)] = 0
    # recall = np.divide(c.diagonal(), c.sum(axis=1), out=np.zeros_like(c.diagonal()), where=c.sum(axis=1)!=0)
    #print(recall)
    #precision = c.diagonal()/c.sum(axis=0)
    # precision = np.divide(c.diagonal(), c.sum(axis=0), out=np.zeros_like(c.diagonal()), where=c.sum(axis=0)!=0)
    #np.divide(a, b, out=np.zeros_like(a), where=b!=0)
    #print(precision)
    ave_recall = sum(recall) / len(recall)
    ave_precision = sum(precision) / len(precision)
    return 2 * ((ave_recall * ave_precision) / (ave_recall + ave_precision))

def getAveragePerPersonFScore(fscores):
    f_list = []
    workspacePerPersonAve = {}
    for person in fscores:
        for workspace in fscores[person]:
            f_list.append(fscores[person][workspace])
            if workspace in workspacePerPersonAve:
                workspacePerPersonAve[workspace].append(fscores[person][workspace])
            else:
                workspacePerPersonAve[workspace] = [fscores[person][workspace]]
    return sum(f_list) / len(f_list), workspacePerPersonAve

def getAverageWorkspacePerPerson(wppa):
    for workspace in wppa:
        wppa[workspace] = sum(wppa[workspace]) / len(wppa[workspace])

def get_f_score_per_Person_confusion(perPersonConfusionMatrices):
    fscores = {}
    for person in perPersonConfusionMatrices:
        for workspace in perPersonConfusionMatrices[person]:
            # c = ankura.validate.Contingency()
            c = {}
            for gold in perPersonConfusionMatrices[person][workspace]:
                for user in perPersonConfusionMatrices[person][workspace][gold]:
                    if gold in c:
                        c[gold].update({user : perPersonConfusionMatrices[person][workspace][gold][user]})
                    else:
                        c[gold] = {}
                        c[gold].update({user : perPersonConfusionMatrices[person][workspace][gold][user]})
            #it works up to here, then breaks at the fmeasure
            print("person")
            print(person)
            print("workspace")
            print(workspace)
            print("c of perPersonConfusionMatrices")
            print(c)
            score = getfscore(c)
            print("score")
            print(score)
            if workspace in fscores:
                fscores[workspace][1] += score
                fscores[workspace][0] += 1
            else:
                fscores[workspace] = [1, score]


    return fscores


#print("fscores\n " + get_f_score_per_Person_confusion(myFile))
np_arrs, f_scores = putInNumpyMatrix(myFile)
print("np_arrs\n\n\n")
print(np_arrs)
print("f_scores\n\n\n")
print(f_scores)
print("\n\n\naverage per person fscore")
all_ave, wppa = getAveragePerPersonFScore(f_scores)
getAverageWorkspacePerPerson(wppa)
print(all_ave)
print("\n\n\naverages per workspace per person")
print(wppa)



#I NEED to know two things: best way to integrate functions of Ankura from github, AND how to put this matrix into those functios
