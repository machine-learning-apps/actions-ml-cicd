#!/bin/bash

set -e
cd $(dirname "$0")/..

docker-compose up -f docker-compose-gpu.yml --build -d
docker push hamelsmu/ml-cicd-gpu
docker exec -it actions-ml-cicd_gpu_1 bash
#docker run -e DASK_SCHEDULER=$DASK_SCHEDULER -it -p 8888:8888 -v $PWD:/data hamelsmu/ml-cicd bash
