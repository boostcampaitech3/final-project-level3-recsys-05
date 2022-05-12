#!/bin/bash

STOP_RESULT=$(docker ps -aqf "name=^santaboj-backend")
echo STOP_RESULT
if [ -n "$STOP_RESULT"]; then
  docker stop $(docker ps -aqf "name=^santaboj-backend")
fi
RM_RESULT=$(docker ps -aqf "name=^santaboj-backend")
echo RM_RESULT
if [ -n "$RM_RESULT" ]; then
  docker rm $(docker ps -aqf "name=^santaboj-backend")
fi

docker run --name "santaboj-backend" -p 8888:8888 -tid santa-backend