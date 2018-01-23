import json

FILE = 'perpersonconfusion.json'

with open(FILE, 'r') as fp:
    myFile = json.load(fp)

if myFile:
    with open(FILE, 'w') as fp2:
        json.dump(myFile, fp2, sort_keys=True, indent=4)
