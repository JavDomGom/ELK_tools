#!/bin/bash

# This script receives three arguments:
# $ 1 is the URL of the Kibana where the dashboards and visualizations will be imported.
# $ 2 is the absolute path of the JSON that will be imported.
# $ 3 is the Saved Object type: dashboard or visualization.

KIBANA="$1"
TMP="$2_import_format"
TYPE="$3"

# With jq only the JSON data structure of attributes is obtained and it is dumped into a temporary file.
cat $2 | jq '.attributes' > $TMP

# The Kibana API is called for import.
curl -s -XPOST -H "kbn-xsrf: true" -H "Content-Type: application/json" "$KIBANA/api/saved_objects/$TYPE" -d "{\"attributes\": $(cat $TMP)}"

# Remove temp file.
[ -f $TMP ] && rm -f $TMP
