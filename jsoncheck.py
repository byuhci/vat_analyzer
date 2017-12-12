import os
import glob
import json
import pprint

video_events = ["hotkey:restart", "hotkey:end", "video:drag", "hotkey", "video:button", "video:click", "hotkey:up", "hotkey:down", "video:button", "video:menu"]
data_events = ["data:dblclick", "data:drag"]
final_res = {}
person_totals = {}
workspace_totals = {}
#event sums is incremented every single time a label event is encountered without further consideration
event_sums = {"video": 0, "data": 0}
final_res["event_totals"] = {"video": 0, "data": 0}
directories = ["studyA", "studyB", "studyC", "studyD"]
#subdirectories = ["pill-blue", "pill-orange", "pill-red", "practice-first", "practice-second", "practice-third", "run-blue", "run-pink", "run-red", "run-yellow"]
video_lengths = {"cane.cane-vid1-dat2" : 107.26, "cane.cane-vid3-dat3" : 86.91, "cane.cane-yellow" : 73.81, "newrun.run-pink" : 640.70, "newrun.run-thurs-seven-attempt" : 641.02, "newrun.Run-thurs-five-fixed-finally" : 668.36, "newrun.run-thurs-six-finally" : 676.13, "pill.pills-pink" :  616.23, "pill.pills-blue" : 612.22, "pill.pills-orange" : 621.25, \
"pill.pills-red" : 629.30 }
cane_andor_practice_workspaces = ["cane.cane-vid1-dat2", "cane.cane-vid3-dat3", "cane.cane-yellow"]
map_gold_to_workspace = {"run-red" : "newrun.run-thurs-seven-attempt", "run-blue" : "newrun.Run-thurs-five-fixed-finally", "run-yellow" : "newrun.run-thurs-six-finally", "run-pink" : "newrun.run-pink", "pills-blue": "pill.pills-blue", "pills-orange" : "pill.pills-orange", "pills-pink" : "pill.pills-pink", "pills-red" : "pill.pills-red" }
#directories = ["bike", "pill-red", "pills-1", "pills-3", "pills-5", "practice", "practice-second", "run-blue", "run-yellow", "pill-blue", "pills", "pills-2", "pills-4", "pill-yellow", "practice-first", "practice-third", "run-red"]
label_times_list = []
person_label_times = {}
delta_t = float(1) / float(30)
PATH = '../user-studies'
GOLD_PATH = "../workspacegold2"
#PATH = '../user-studies'
#GOLD_PATH = "../workspacegold"
confusionMatrix = {}
perPersonConfusionMatrices = {}

#rough outline of loop that will give us the per frame accurracy
# for frame in frames:
# gold = findgoldlabel(frame)
# user = finduserlabel(fram)
#confusion[gold][user]++
def findGoldLabel(theWorkSpace, time):
    for root, dirs, files in os.walk(GOLD_PATH):
        for file in files:
            filename = os.path.join(root,file)
            with open(filename) as data_file:
                gold_filename = json.load(data_file)

                # print("gold_filename")
                # print(gold_filename)
                split_gold_filename = filename.split('/')
                # print("split gold filename")
                # print(split_gold_filename)
                final_split = split_gold_filename[-1].split('.')
                print("theWorkSpace")
                print(theWorkSpace)
                print("final_split[0]")
                print(final_split[0])
                try:
                    print("map_gold_to_workspace[final_split[0]]  " + str(map_gold_to_workspace[final_split[0]]))
                except KeyError:
                    print(final_split[0])
                    continue
                if map_gold_to_workspace[final_split[0]] in theWorkSpace:
                    print("returning getGoldLabelAt")
                # if final_split[0] in theWorkSpace or final_split[0] in filename: #TODO:: add or in filename. this MIGHT NOT WORK because theWorkSpace is the one we're looking for not necessarily the filename
                    return getGoldLabelAt(gold_filename, time)
                else:
                    print("more for")
    print("returning none from findGoldLabel")
    return "None"

def getGoldLabelAt(gold_filename, time):
    for event in gold_filename:
        #print("in gold label at loop")
        if event["time"] < time and event["endTime"] > time:
            return event["type"]
    return "None"

#PROBLEM is that the gold standard files don't have the same file structure as the normal .info ones
def getLabel(file, time):
    for event in file["details"]["labels"]:
        #print("in getLabel loop")
        if event["time"] < time and event["endTime"] > time:
            return event["type"]
    return "None"

#this function calculates the confusionMatrix for each workspace.
#it also calls the function that calculates the perPersonConfusionMatrices
def doConfusion(filename):
    #for file in workspace:
    # theWorkSpace = filename["workspace"].encode('utf-8')
    theWorkSpace = filename["workspace"]
    # print("theWorkSpace")
    # print(theWorkSpace)

    start_time = delta_t
    while start_time < video_lengths[theWorkSpace]:
        gold = findGoldLabel(theWorkSpace, start_time)
        user = getLabel(filename, start_time)
        # print("theWorkSpace")
        # print(theWorkSpace)
        # print("gold")
        # print(gold)
        doPerPersonMatrix(filename, theWorkSpace, gold, user)
        if theWorkSpace in confusionMatrix:
            if gold in confusionMatrix[theWorkSpace]:
                if user in confusionMatrix[theWorkSpace][gold]:
                    confusionMatrix[theWorkSpace][gold][user] = confusionMatrix[theWorkSpace][gold][user] + 1
                else:
                    confusionMatrix[theWorkSpace][gold].update({user : 1})
            else:
                confusionMatrix[theWorkSpace][gold] = {}
                confusionMatrix[theWorkSpace][gold].update({user : 1})
        else:
            confusionMatrix[theWorkSpace] = {}
            confusionMatrix[theWorkSpace][gold] = {}
            confusionMatrix[theWorkSpace][gold].update({user : 1})
        start_time += delta_t

def doPerPersonMatrix(filename, theWorkSpace, gold, user):
    personID = filename["user_id"]
    if personID in perPersonConfusionMatrices:
        if theWorkSpace in perPersonConfusionMatrices[personID]:
            if gold in perPersonConfusionMatrices[personID][theWorkSpace]:
                if user in perPersonConfusionMatrices[personID][theWorkSpace][gold]:
                    perPersonConfusionMatrices[personID][theWorkSpace][gold][user] = perPersonConfusionMatrices[personID][theWorkSpace][gold][user] + 1
                else:
                    perPersonConfusionMatrices[personID][theWorkSpace][gold].update({user : 1})
            else:
                perPersonConfusionMatrices[personID][theWorkSpace][gold] = {}
                perPersonConfusionMatrices[personID][theWorkSpace][gold].update({user : 1})
        else:
            perPersonConfusionMatrices[personID][theWorkSpace] = {}
            perPersonConfusionMatrices[personID][theWorkSpace][gold] = {}
            perPersonConfusionMatrices[personID][theWorkSpace][gold].update({user : 1})
    else:
        perPersonConfusionMatrices[personID] = {}
        perPersonConfusionMatrices[personID][theWorkSpace] = {}
        perPersonConfusionMatrices[personID][theWorkSpace][gold] = {}
        perPersonConfusionMatrices[personID][theWorkSpace][gold].update({user : 1})
    # here I would do a while loop but the bounds would be < total_time(workspace) but I don't know how to find that. So I'm in a bad spot you see.

class label_time:
    def __init__(self, person, workspace):
        self.person = person
        self.workspace = workspace
        self.label_list = []

class label_class:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


def outer_loop():
    #path = '../user-studies/'
    print(PATH)
    for root, dirs, files in os.walk(PATH):
        print("root")
        print(root)
        print("dirs")
        print(dirs)
        print(" files")
        print(files)
        for file in files:
            inner_loop(os.path.join(root,file))



#this loop attempts to get a dictionary with (person, workspace) as the key and a list of tuples (start_time, endtime)
def calc_label_times(sesh_title, person, workspace, filename):
    for index, label in enumerate(filename["details"]["labels"]):
        # one_label = label_class(label["time"], label["endTime"])
        label_times = (label["time"], label["endTime"])
        if (person, workspace) in person_label_times:
            person_label_times[(person, workspace)].append((label["time"], label["endTime"]))
        else:
            person_label_times[(person, workspace)] = []
            person_label_times[(person, workspace)].append((label["time"], label["endTime"]))
        #person_label_times.setdefault(person, workspace.setdefault("labels" : []))
        # person_label_times[person][workspace]["labels"][index]["time"] = label["time"]
        # person_label_times[person][workspace]["labels"][index]["endTime"] = label["endTime"]
        #ACTUALLY NEEDS MORE THAN THIS, AS COULD HAVE MULTIPLE LABELS


#this loop goes through each file in the subdirectory
def inner_loop(pfile):
    #for file in filenames:
    # print(file)
    if("info.json" in pfile):
        # print("file in loop")
        # print(file)
        filename = "None"
        try:
            with open(pfile) as data_file:
                filename = json.load(data_file)
        except ValueError:
            print(pfile)
        if filename != "None":
            # print("filename")
            # print(filename)
            workspace = filename["workspace"]
            # print("workspace")
            # print(workspace)
            if workspace not in cane_andor_practice_workspaces:
                doConfusion(filename)
                sesh_title = (filename["user_id"] + " " +  filename["workspace"])
                final_res[sesh_title] = {"video" : 0, "data" : 0}
                person = filename["user_id"]

                person_totals.setdefault(person, {"video" : 0, "data" : 0})
                workspace_totals.setdefault(workspace, {"video" : 0, "data" : 0})
                calc_label_times(sesh_title, person, workspace, filename)
                try_catch_inner(sesh_title, person, workspace, filename)
            else:
                print("skipped practice workspace")

#this function actively does the counts-- i.e., it evaluates whether each person had more data or video events, and also
#whether each workspace had more data or video events, and also counts the total data versus video events of the data
def try_catch_inner(sesh_title, person, workspace, filename):
    try:
        value = filename["logs"]["labelEvents"]
        # we also need to get percentage of data / video events for each workspace
        for event in filename["logs"]["labelEvents"]:
             if event["source"] in video_events:
                 final_res[sesh_title]["video"] = final_res[sesh_title]["video"] + 1
                 event_sums["video"] += 1
                 workspace_totals[workspace]["video"] += 1
                 #other stuff
             else:
                  final_res[sesh_title]["data"] = final_res[sesh_title]["data"] + 1
                  event_sums["data"] += 1
                  workspace_totals[workspace]["data"] += 1
                 #add to data events

        for event in filename["logs"]["navigationEvents"]:
             if event["source"] in video_events:
                 final_res[sesh_title]["video"] = final_res[sesh_title]["video"] + 1
                 event_sums["video"] += 1
                 workspace_totals[workspace]["video"] += 1
                 #other stuff
             else:
                  final_res[sesh_title]["data"] = final_res[sesh_title]["data"] + 1
                  event_sums["data"] += 1
                  workspace_totals[workspace]["data"] += 1
                 #add to data events


        if(final_res[sesh_title]["data"] > final_res[sesh_title]["video"]):
            #print(final_res)
            final_res["event_totals"]["data"] += 1
            person_totals[person]["data"] += 1
            #workspace_totals[workspace]["data"] += 1
        elif (final_res[sesh_title]["data"] < final_res[sesh_title]["video"]):
            final_res["event_totals"]["video"] += 1
            person_totals[person]["video"] += 1
            #workspace_totals[workspace]["video"] += 1
            #possibly should check for times where both are 0, in which case
            #neither thing should be added
        elif (final_res[sesh_title]["data"] == 0 and final_res[sesh_title]["video"] == 0):
            return
        else:
            final_res["event_totals"]["video"] += 1
            person_totals[person]["video"] += 1
            #workspace_totals[workspace]["video"] += 1

            final_res["event_totals"]["data"] += 1
            person_totals[person]["data"] += 1
            #workspace_totals[workspace]["data"] += 1
    except KeyError:
        return

def calculate_gold_totals():
    gold_totals = {}
    for (person, label) in person_label_times:
        if person == "wiffyfern":
            gold_totals[label] = person_label_times[(person, label)]
    return gold_totals


def calc_workspace_percentages(workspace_totals):
    workspace_percentages = {}
    for key,value in workspace_totals.items():

        workspace_percentages.setdefault(key, {"video": 0.0, "data": 0.0})
        total_num = value["video"] + value["data"]
        if total_num == 0:
            continue
        workspace_percentages[key]["data"] = value["data"] / float(total_num)
        workspace_percentages[key]["video"] = value["video"] / float(total_num)
    return workspace_percentages

def get_f_score_confusion(confusionMatrix):
    fscores = {}


def get_f_score_per_Person_confusion(perPersonConfusionMatrices):
    fscores = {}
    for person in perPersonConfusionMatrices:
        for workspace in perPersonConfusionMatrices[person]:
            c = ContingencyTable()
            for gold in perPersonConfusionMatrices[person][workspace]:
                for user in perPersonConfusionMatrices[person][workspace][gold]:
                    c[gold,user] = perPersonConfusionMatrices[person][workspace][gold][user]
            score = c.fmeasure()
            if workspace in fscores:
                fscores[workspace][1] += score
                fscores[workspace][0]+=1
            else:
                fscores[workspace] = [1, score]
            # c = ContingencyTable(perPersonConfusionMatrices[person][workspace])

    return fscores



outer_loop()
print("HERE is the confusionMatrix")
print(confusionMatrix)
with open('confusion.json', 'w') as fp:
    json.dump(confusionMatrix, fp, sort_keys=True, indent=4)
print("\n\n\n\n\n")
print("matrix per Person")
# print(perPersonConfusionMatrices)
with open('perpersonconfusion.json', 'w') as fp2:
    json.dump(perPersonConfusionMatrices, fp2, sort_keys=True, indent=4)
print("\n\n\n\n")
print(json.dumps(perPersonConfusionMatrices, indent=4, sort_keys=True))

# print("\n\n\nPer workspace per person confusion matrix f scores ")
# print(get_f_score_per_Person_confusion(perPersonConfusionMatrices))

#pprint.pprint(perPersonConfusionMatrices)
#gold_totals = calculate_gold_totals()
work_percent = calc_workspace_percentages(workspace_totals)

# print(final_res)
# print("\n\n")
# print(final_res["event_totals"])
print("\n\n")
print("workspace totals -- the real good stuff ")
print(workspace_totals)

print("\nworkspace percentages -- what you really wanted to know")
print(work_percent)

# print("\n\n")
# print(person_totals)

print("\n\nEvent Overall Sums\n")
print(event_sums)
# print("\n\nPeople Workspace Labels")
# for (person, label) in person_label_times:
#     print(person)
#     print(label)
#     print (person, label)
#     print(person_label_times[(person, label)])
#     print(" ")


# print("\n\nGold Standard Labels")
# for label in gold_totals:
#     print(label)
#     print(" ")
#     print(gold_totals[label])
#     print("")


#to extend analysis, can find the gold standard here with one for loop, then can find the differences between
#its results and the rest of the data using absolute value. should be fairly straightforward
