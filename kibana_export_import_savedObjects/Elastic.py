import json, requests
from requests.exceptions import ConnectionError, RequestException

class Metrics:

    def getMetrics(elastic, indexPattern, numberMetrics, country):
        URL = elastic+'/'+indexPattern+'/_search?pretty&size='+numberMetrics

        headers = {
            'Content-Type': 'application/json'
        }
        query = {
          "query": {
            "match": {"meta.country": country}
          },
          "sort": {"@timestamp": "desc"}
        }
        try:
            response = requests.get(URL, json=query, headers=headers)
            return response.status_code, to_json(response.content)
        except ConnectionError as ex:
            print("Connection Error: {}".format(ex))
            exit(0)
        except RequestException as e:
            print("Request exception: {}".format(e))
            exit(1)


    def getSavedObject(kibana, type, id):
        URL = kibana+'/api/saved_objects/'+type+'/'+id

        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(URL, headers=headers)
            return response.status_code, to_json(response.content)
        except ConnectionError as ex:
            print("Connection Error: {}".format(ex))
            exit(0)
        except RequestException as e:
            print("Request exception: {}".format(e))
            exit(1)


def to_json(content):
    ''' Method to convert response.content from bytes to JSON.
    Arguments:
		:content: Response content.
    '''
    return json.dumps(json.loads(content.decode('utf8')), indent=4)
