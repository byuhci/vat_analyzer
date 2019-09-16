# VAT ANALYZER (to understand data from user studies run on VAT)

# User study looks like this:

'studyName.tasks.json'

for example: 'studyE.tasks.json'

In this file, there should be a massive JSON object which contains the names of the videos users will be watching (the time limit they have, what info is hidden, etc) and the questions they will be asked (what answer choices they have for the questions, the name of the question, and the actual question).

# You're also gonna need a gold standard
(but you've already done that, so I think you know how to do it, so I'm not going to write out directions for that)


# Data looks like this:

/parentFolder/studyName/videoName

for example: /Data/studyE/drywall-blue

In each of these folders, there's going to be a 'userid.info.json', 'userid.labels.json', and 'userid.survey.json'. For this reason, it would be preferrable if userid's do not have spaces in them.


# In the end, sorted data should look like:

1. data from users who 'had-both' (FOR EACH TASK TYPE: 4 questions which are shown as two questions per graph because of differing y axis)
2. data from users who had 'no-data' (FOR EACH TASK TYPE: 4 questions which are shown as two questions per graph because of differing y axis)
3. data from users who had 'no-video'  (FOR EACH TASK TYPE: 4 questions which are shown as two questions per graph because of differing y axis)
4. data from 'post-section surveys' (one graph showing 4 questions for each task type: run, pills, etc)
5. data when you combine task types (ie, both running and pills for has-both, both running and pills for no-data, and both running and pills for no-video)
6. data from the user after they complete a section (where a section is, in some order, 'has-both', 'no-video', 'no-data').
7. there were also a few open-ended questions, so there should also be plain text somewhere too.
8. You're also going to want to know who won the user studies, so they can get their rewards.
9. We also gathered 'observed data'. This was things like: how often users scrubbed the video, skipped, peeked, resized, jumped in the video, paused/played the video, etc.
10. As far as statistics go, we used mann whitney as our non-parametric test.
11. We also looked at Wilcoxon, one sample t-tests, and tried normalizing our data. Box and whisker graphs.


# Getting data from the Data

1-6. These are all calculated by running 'subjectiveAnswers.py'.

7. I'm pretty sure that I actually wrote a script to take all the plain text out of JSON files into respective .txt files. I'll take a look for this again.

8. In order to calculate the winners of user studies:
a. You're going to need to make a 'perPersonFScores.json' file.
b. set the constant 'file_with_FScores' to that file location/name.

9. In order to parse the 'observed data', you're going to need to talk to Lawrence: he gave me a file which I named:  'fromLawrenceJumpScrubs_withHiddenValue_withFeb.csv' (you can take a look at the CSV in this folder to know that you need from Lawrence). Once you have that, take a look at observedAnswers.py (in the observedAnswers folder). You'll need to correct the file location/name. Also note, I currently have the code set to output the csv into the folder: 'comparingVideoToolUsageToDataWithFeb/' + str(lenDataOrVideo) + nameOfDataOrVideo + 'WithFeb.csv'

10. 'mannWhitney_friedman_scripts.py' (make sure to run _both_ combo() and main(), you'll need to ctrl-f for the variable 'stackedData.csv' and make sure you set that to the correct variable). We might have also used 'friedman_scripts.py' (look at 'adjusted_scale_subjectiveData.csv').

11. Wilcoxon, one sample t-tests, normalizing our data, and box and whisker graphs are all talked about in 'subjectiveAnswersHiddenValRunOrPillActualQuestions'
