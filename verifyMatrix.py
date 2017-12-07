import json
import ankura
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
            if workspace in run_workspaces:
                for i, k in enumerate(['None', 'run', 'skip']):
                    row = c[k]
                    for j, kk in enumerate(['None', 'run', 'skip']):
                        val = row.get(kk,0)
                        matrix[i][j] = val
            elif workspace in cane_andor_practice_workspaces:
                continue
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
    recall = c.diagonal()/c.sum(axis=1)
    #print(recall)
    precision = c.diagonal()/c.sum(axis=0)
    #print(precision)
    return 2 * ((recall * precision) / (recall + precision))

# def get_f_score_per_Person_confusion(perPersonConfusionMatrices):
#     fscores = {}
#     for person in perPersonConfusionMatrices:
#         for workspace in perPersonConfusionMatrices[person]:
#             c = ankura.validate.Contingency()
#             for gold in perPersonConfusionMatrices[person][workspace]:
#                 for user in perPersonConfusionMatrices[person][workspace][gold]:
#                     c[gold,user] = perPersonConfusionMatrices[person][workspace][gold][user]
#                     print("c[gold][user]")
#                     print(c[gold,user])
#             #it works up to here, then breaks at the fmeasure
#             print("c.self.table")
#             print(c.table)
#             score = c.fmeasure(None, None)
#             print("score")
#             print(score)
#             if workspace in fscores:
#                 fscores[workspace][1] += score
#                 fscores[workspace][0] += 1
#             else:
#                 fscores[workspace] = [1, score]
#
#
#     return fscores

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


def getfscore(c):
    print("in getfscore")
    recall = getRecall(c)
    precision = getPrecision(c)
    return 2 * ((recall * precision) / (recall + precision))

def getRecall(c):
    print("in getRecall")
    my_recalls = []
    for gold in c:
        TP = -1
        my_sum = []
        for user in c[gold]:
            my_sum.append(c[gold][user])
            if user == gold:
                TP = c[gold][user]
        one_recall = TP / sum(my_sum)
        my_recalls.append(one_recall)
    final_recall = float(sum(my_recalls)) / max(len(my_recalls), 1)
    return final_recall

def getPrecision(c):
    print("in getPrecision")
    prec_list = []
    max_size_list = []
    gold_size = 0
    for gold in c:
        gold_size+=1
        size = 0
        for user in c[gold]:
            size+=1
        max_size_list.append(size)
        max_size_list.append(gold_size)
    max_size_num = max(max_size_list)

    zeros = [[0 for i in range(max_size_num)] for j in range(max_size_num)]
    print("c")
    print(c)
    print("max_size_list")
    print(max_size_list)
    print("zeros pre ")
    print(zeros)


    gold_index = 0
    tp_list = []
    for gold in c:
        user_index = 0
        for user in c[gold]:
            print("gold_index")
            print(gold_index)
            print("user_index")
            print(user_index)
            zeros[gold_index][user_index] = c[gold][user]
            if gold == user:
                tp_list.append((gold_index,user_index))
            user_index+=1
        gold_index+=1

    print("zeros")
    print(zeros)

    my_precisions = []
    for j in range(max_size_num):
        TP = -1
        sum_list = []
        for i in range(max_size_num):
            sum_list.append(zeros[i][j])
            if (i,j) in tp_list:
                TP = zeros[i][j]
        one_precision = TP / sum(sum_list)
        my_precisions.append(one_precision)
    final_precision = float(sum(my_precisions)) / max(len(my_precisions), 1)
    return final_precision

#print("fscores\n " + get_f_score_per_Person_confusion(myFile))
np_arrs, f_scores = putInNumpyMatrix(myFile)
print("np_arrs")
print(np_arrs)
print("f_scores")
print(f_scores)
# print(f_scores)
# theScores = get_f_score_per_Person_confusion(myFile)
# print(theScores)

# for person in myFile:
#     print "this is person"
#     print person
#     for workspace in myFile[person]:
#         print "this is workspace"
#         print workspace
#         for gold in myFile[person][workspace]:
#             print "this is gold"
#             print gold
#     #         break
#     #     break
#     # break

#I NEED to know two things: best way to integrate functions of Ankura from github, AND how to put this matrix into those functios
