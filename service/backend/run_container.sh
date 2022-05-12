#!/bin/bash

STOP_RESULT=$(docker ps -aqf "name=^santaboj-backend")
if [ "$STOP_RESULT" != ""]; then
  docker stop $(docker ps -aqf "name=^santaboj-backend")
fi
RM_RESULT=$(docker ps -aqf "name=^santaboj-backend")
if [ "$RM_RESULT" != ""]; then
  docker rm $(docker ps -aqf "name=^santaboj-backend")
fi

docker run --name "santaboj-backend" -p 8888:8888 -tid santa-backend