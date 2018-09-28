#!/usr/bin/python3

# Dependencies: curl, jq

# Example: python3 kibana_export_import_savedObjects.py -o http://172.17.0.2:5601 -i http://172.17.0.3:5601

import sys, os, argparse, datetime, fileinput, json, urllib.request, subprocess

# Set global variables,
indexPatternCons = 'your_index-pattern*'
exportDir = 'export'


def msg():
    ''' This function returns a message that will be printed in the program's help. '''
    return "\tpython3 {:s} -o http://export_elastic_host:port -i http://import_elastic_host:port | -h".format(sys.argv[0])


# Set the arguments that the program will receive.
parser = argparse.ArgumentParser(description='This program makes an export of Dashboards and Visualizations from Kibana, modifies the data and then imports them into another Kibana.', usage=msg())
parser.add_argument('-o','--output', help='URL with host and port of the Elastic Search from which data will be exported.', required=True)
parser.add_argument('-i','--input', help='URL with host and port of the Elastic Search to which data will be imported.', required=True)
args = vars(parser.parse_args())


def getTimestamp():
	''' This function returns a timestamp for formatting logs. '''
	return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def log(type, msg):
	''' This function returns a timestamp for formatting logs.

	Arguments:
		:type: The message type.
		:msg: The message to be printed.
	'''

    # Set the colors for each case of log level.
	switcher = {
		's': '\033[32m[SUCCESS]\033[0m',
		'i': '\033[34m[INFO]\033[0m',
		'w': '\033[33m[WARNING]\033[0m',
		'e': '\033[31m[ERROR]\033[0m',
	}
	print(getTimestamp(), switcher.get(type), msg)


def exportJSON(type, id):
	''' This function export a savedObject like visualization
        or dashboard in a JSON file.

	Arguments:
		:type: Can be dashboard or visualization.
		:id: visualization or dashboard ID.
	'''
    # Get saved object data in JSON format.
    with urllib.request.urlopen(args['output']+'/api/saved_objects/'+type+'/'+id) as url:
        data = json.loads(url.read())

        # If the export directory does not exist, it is automatically created
        if not os.path.isdir(exportDir):
           os.makedirs(exportDir)

        # If the type directory does not exist into export dir, it is automatically created
        if not os.path.isdir(exportDir+'/'+type):
           os.makedirs(exportDir+'/'+type)

        # Dump data in JSON file.
        with open(exportDir+'/'+type+'/'+id+'.json','w') as f:
            json.dump(data, f)


def getDestinationIndexPatternIdByTitle(searchTitle=indexPatternCons):
    ''' This function search the index-pattern by title and gets the ID.

	Arguments:
		:searchTitle: The index-pattern title (default = indexPatternCons).
	'''
    # Initially the search is marked as false.
    found = False

    # Get all data of all index-patterns that exist in the origin Kibana.
    with urllib.request.urlopen(args['input']+'/api/saved_objects/index-pattern?per_page=10000') as url:
        data = json.loads(url.read().decode())

        # Search through the data items.
        for (k, v) in data.items():

            # If the key is saved_objects.
            if k == 'saved_objects':

                # for each item in value.
                for item in v:

                    # Set index-pattern title.
                    title = item['attributes']['title']

                    # If the origin index-pattern title and destination index-pattern are equal.
                    if searchTitle == title:

                        # The search is marked as True.
                        found = True

                        # Stop search loop.
                        break

                        # Set destination index-pattern ID.
                        id = item['id']

                        # Return destination index-pattern ID.
                        return id

    # If no index-pattern has been found with the name of the search (searchTitle argument) prints an error.
    if not found:
        log('e', 'ERROR: The index-pattern \"'+searchTitle+'\" doesn\'t exist in \"'+args['input']+'\" Elastic Search.')


def replaceVisualizationData(title, id):
    ''' This function replaces visualization data in JSON file.

	Arguments:
		:title: Visualization title.
		:id: visualization ID.
	'''
    indexPatternId = ''
    fileToOpen = exportDir+'/visualization/'+id+'.json'

    # Open visualization JSON file and loads the data in data variable.
    with open(fileToOpen, 'r') as f:
        data = json.loads(
            # Gets only the searchSourceJSON structure.
            json.load(f)['attributes']['kibanaSavedObjectMeta']['searchSourceJSON']
        )

        # For key and value in data.
        for (k, v) in data.items():

            # If item key is equal to index, set indexPatternId variable with item value.
            if k == 'index':
                indexPatternId = v
    f.close()

    # If there is an id of an index-pattern associated with the visualization.
    if indexPatternId:
        for line in fileinput.input([fileToOpen], inplace=True):
            # Change the source ID to the destination ID for an index-pattern with the same title.
            print(line.replace(indexPatternId, getDestinationIndexPatternIdByTitle()), end='')


def replaceDashboardData(dashboardId):
    ''' This function replaces dashboard data in JSON file.

	Arguments:
		:dashboardId: Dashboard ID.
	'''
    fileToOpen = exportDir+'/dashboard/'+dashboardId+'.json'

    # Open dashboard JSON file and loads the data in data variable.
    with open(fileToOpen, 'r') as f:
        data = json.loads(
            json.load(f)['attributes']['panelsJSON']
        )

        # For each panel in Dashboard.
        for panel in data:

            # If panel is visualization type.
            if panel['type'] == 'visualization':

                # Set origin visualization ID.
                visIdOrigin = panel['id']

                # Search in origin Kibana by origin visualization ID and get all JSON data.
                with urllib.request.urlopen(args['output']+'/api/saved_objects/visualization/'+visIdOrigin) as url:
                    data = json.loads(url.read().decode())

                    # Set origin visualization title.
                    visTitleOrigin = data['attributes']['title']

                # Search in destination Kibana all visualizations JSON data.
                with urllib.request.urlopen(args['input']+'/api/saved_objects/visualization?per_page=10000') as url:
                    data = json.loads(url.read().decode())
                    for (k, v) in data.items():

                        # Search into saved_object key.
                        if k == 'saved_objects':
                            for item in v:

                                # Set destination visualization title.
                                visTitleDestination = item['attributes']['title']

                                # If the visualization title is equal in origin and destination.
                                if visTitleDestination == visTitleOrigin:

                                    # Set destination visualization ID.
                                    visIdDestination = item['id']

                                    # Stop search loop.
                                    break

            # Print INFO log for each visualization founded.
            log('i', '['+visTitleOrigin+'] Origin visualization ID: \"'+visIdOrigin+'\" found. Replaced by destination visualization ID: \"'+visIdDestination+'\".')

            # If both IDs were found.
            if visIdOrigin and visIdDestination:
                for line in fileinput.input([fileToOpen], inplace=True):

                    # Change origin ID to destination ID for a Dashboard with the same title.
                    print(line.replace(visIdOrigin, visIdDestination), end='')
                    
    # Close opened file.
    f.close()

def importSavedObject(type, id):
    ''' This function import a savedObject like visualization
        or dashboard in a JSON file.

	Arguments:
		:type: Can be dashboard or visualization.
		:id: visualization or dashboard ID.
	'''
    fileToImport = exportDir+'/'+type+'/'+id+'.json'

    # At this moment, a call is made to a shell script that is
    # responsible for importing the dashboard or visualization.
    command = '''./import.sh '''+args['input']+" "+fileToImport+" "+type

    # Get the shell script output
    output = subprocess.check_output(command, shell=True)
    #print(output)

def getOriginSavedObjects(savedObjectType):
    ''' This function get a savedObject like visualization
        or dashboard, export it, replace data and finally
        import the JSON file.

	Arguments:
		:savedObjectType: Can be dashboard or visualization.
	'''
    # Search in origin Kibana dashboards or visualizations and get all data in JSON format.
    with urllib.request.urlopen(args['output']+'/api/saved_objects/'+savedObjectType+'?per_page=10000') as url:
        data = json.loads(url.read().decode())

        # For each key and value in data items.
        for (k, v) in data.items():

            # Search into saved_object key.
            if k == 'saved_objects':
                for item in v:

                    # Set destination saved object ID.
                    id = item['id']

                    # Set destination saved object title.
                    title = item['attributes']['title']

                    # Print INFO log for each saved object founded.
                    log('i', savedObjectType+' \"'+title+'\" found. Start export data.')

                    # Export saved object data in JSON file.
                    exportJSON(savedObjectType, id)

                    # Print INFO log for each saved object founded.
                    log('i', 'Start replace data in exported '+savedObjectType+' JSON file ...')

                    # Is saved objects is visualization.
                    if savedObjectType == 'visualization':

                        # Replace data.
                        replaceVisualizationData(title, id)

                    # Is saved objects is visualization.
                    elif savedObjectType == 'dashboard':

                        # replace data.
                        replaceDashboardData(id)

                    # Print INFO log for each saved object founded.
                    log('i', 'Start import '+savedObjectType+' JSON data in '+args['output']+' ...')

                    # Finally import JSON data in destination Kibana.
                    importSavedObject(savedObjectType, id)


# Start the program with a call to the getOriginSavedObjects function.
# The visualizations are first treated and then the dashboards.
# You have to strictly follow that order.
getOriginSavedObjects('visualization')
getOriginSavedObjects('dashboard')
