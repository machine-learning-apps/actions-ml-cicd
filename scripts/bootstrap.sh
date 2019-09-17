#!/bin/bash

set -e
cd $(dirname "$0")/..

docker build -t hamelsmu/ml-cicd -f docker/Dockerfile .
docker-compose up -d
docker exec -it hamelsmu/ml-cicd bash
#docker run -e DASK_SCHEDULER=$DASK_SCHEDULER -it -p 8888:8888 -v $PWD:/data hamelsmu/ml-cicd bash
