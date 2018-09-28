# Import/Export saved objects from Elastic Search
This program is a simple Python script that connects to an origin Kibana and exports a saved object or all, depending on how it is executed.

## Package contents

| Directory/File | Description |
| --- | --- |
| `kibana_export_import_savedObjects.py` | Main Python program. |
| `import.sh` | Script that will be invoked exclusively to make the import of saved objects from the main Python program. |
| `README.md` | This guide. |

## Prerequisites

In order to deploy this service, you need:

* Python 3.
* Curl.
* Jq.

## How it works
This script receives some arguments:


	-o	Output URL with host and port of the origin Kibana, for example:
          http://172.17.0.2:5601

	-i	Input URL with host and port of the destination Kibana, for example:
          http://172.17.0.3:5601

## Example of execution
```
python3 kibana_export_import_savedObjects.py -o http://172.17.0.2:5601 -i http://172.17.0.3:5601
```
In the first execution, an `export` directory and a subdirectory with the name of the saved object (`dashboard` or `visualization`) that will be exported from origin Kibana, where each dashboard and visualization will be stored with the format `savedObjectID.json`. Then some changes are made to the JSON files exported from some visualizations, and finally they are imported into a destination Kibana.
