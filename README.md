# VAT ANALYZER (to understand data from user studies run on VAT)

# User study looks like this:

'studyName.tasks.json'

for example: 'studyE.tasks.json'

In this file, there should be a massive JSON object which contains the names of the videos users will be watching (the time limit they have, what info is hidden, etc) and the questions they will be asked (what answer choices they have for the questions, the name of the question, and the actual question).


# Data looks like this:

/parentFolder/studyName/videoName
for example: /Data/studyE/drywall-blue

In each of these folders, there's going to be a 'userid.info.json', 'userid.labels.json', and 'userid.survey.json'. For this reason, it would be preferrable if userid's do not have spaces in them.

# Getting data from the Data


# In the end, sorted data should look like:

1. data from users who 'had-both' (FOR EACH TASK TYPE: 4 questions which are shown as two questions per graph because of differing y axis)
2. data from users who had 'no-data' (FOR EACH TASK TYPE: 4 questions which are shown as two questions per graph because of differing y axis)
3. data from users who had 'no-video'  (FOR EACH TASK TYPE: 4 questions which are shown as two questions per graph because of differing y axis)
4. data from 'post-section surveys' (one graph showing 4 questions for each task type: run, pills, etc)
5. data when you combine task types (ie, both running and pills for has-both, both running and pills for no-data, and both running and pills for no-video)
6. data from the user after they complete a section (where a section is, in some order, 'has-both', 'no-video', 'no-data').
7. there were also a few open-ended questions, so there should also be plain text somewhere too.
