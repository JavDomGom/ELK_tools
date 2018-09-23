#!/bin/bash

KIBANA="http://172.17.0.2:5601" # Set this variable
LOOP=1

while [ $LOOP ]
do
     printf '\nPlease, type which visualization do you want to add: '
     read TYPE

     case $TYPE in
      area|pie) curl -s -XPOST -H "kbn-xsrf: true" -H "Content-Type: application/json" "$KIBANA/api/saved_objects/visualization" -d "{\"attributes\": $(cat templates/$TYPE.json)}"
                exit 0
      ;;
      exit)     printf 'Exiting...\n'
                LOOP=0
                exit 0
      ;;
      *)        printf 'Valid options are: [area|pie]\n' ;;
     esac
done
