#!/usr/bin/python3

import os, json, fileinput
from Elastic import Metrics

# Set global variables,
kibana = 'http://172.17.0.2:5601'
exportDir = 'new_export'

def getSavedObject(type, id):
    # Get visualization http_status and content.
    http_status, content = Metrics.getSavedObject(kibana, type, id)

    # Loads content in JSON format.
    data = json.loads(content)

    # If the export directory does not exist, it is automatically created
    if not os.path.isdir(exportDir):
       os.makedirs(exportDir)

    # If the type directory does not exist into export dir, it is automatically created
    if not os.path.isdir(exportDir+'/'+type):
       os.makedirs(exportDir+'/'+type)

    # Dump data in JSON file.
    with open(exportDir+'/'+type+'/'+id+'.json','w') as f:
        json.dump(data, f)
    f.close()

    # Return saved object JSON data
    return data


savedObject = getSavedObject('visualization', '7d7d37c0-a203-11e8-a6df-49c8c0fe61fb')

print(savedObject['attributes']['title'])
