#!/bin/bash

set -e
cd $(dirname "$0")/..

docker build -t hamelsmu/ml-cicd -f docker/Dockerfile .
docker run -e DASK_SCHEDULER=$DASK_SCHEDULER -it -p 8888:8888 -v $PWD:/data hamelsmu/ml-cicd bash
