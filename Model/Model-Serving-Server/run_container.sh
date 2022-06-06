#!/bin/bash

STOP_RESULT=$(docker ps -aqf "name=^inference-server")
echo $STOP_RESULT
if [ -n "$STOP_RESULT" ]; then
  docker stop $(docker ps -aqf "name=^inference-server")
fi
RM_RESULT=$(docker ps -aqf "name=^inference-server")
echo $RM_RESULT
if [ -n "$RM_RESULT" ]; then
  docker rm $(docker ps -aqf "name=^inference-server")
fi

docker run --name "inference-server" -p 30002:30002 -tid inference-server
