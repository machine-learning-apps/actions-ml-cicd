#!/bin/bash

set -e
cd $(dirname "$0")/..

docker build -t hamelsmu/ml-cicd-gpu -f docker/gpu.Dockerfile .
docker push hamelsmu/ml-cicd-gpu
docker run -e DASK_SCHEDULER=$DASK_SCHEDULER --runtime=nvidia -it -p 8888:8888 -v $PWD:/data hamelsmu/ml-cicd bash