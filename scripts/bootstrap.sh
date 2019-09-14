#!/bin/bash

docker build -t hamelsmu/ml-cicd -f Dockerfile .
docker run -e DASK_SCHEDULER=$DASK_SCHEDULER -it -p 8888:8888 -v $PWD:/data hamelsmu/ml-cicd bash