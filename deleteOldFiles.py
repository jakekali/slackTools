
import requests
from datetime import datetime, timedelta
import json

#Paste your slack Autho token here
token = "Your Token Goes here"
# Starting from how many days ago it should delete
daysAgo = 60


def getOldFileIDs(token,daysAgo):
    date_N_days_ago = datetime.now() - timedelta(days=daysAgo)
    timestamp = date_N_days_ago.timestamp()

    payload = {'token': token, 'count': 100000, 'ts_to':timestamp}
    r = requests.post("https://slack.com/api/files.list", data=payload)

    data = json.loads(r.text)
    files = data['files']
    fileIds = []
    for file in files:
        fileIds.append(file['id'])

    return fileIds


def deleteFile(token,Id):

    payload = {'token': token, 'file': Id}
    r = requests.post("https://slack.com/api/files.delete", data=payload)

    data = json.loads(r.text)
    return data
counter = 0
while True:
    fileIds = getOldFileIDs(token, daysAgo)
    for fileId in fileIds:
        print(deleteFile(token,fileId))
        print(fileId)
        counter = counter + 1
    if getOldFileIDs(token, daysAgo) == []:
        print("All  Finished \n You deleted " + str(counter) + " files")
        break
