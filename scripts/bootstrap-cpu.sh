#!/bin/bash

set -e
cd $(dirname "$0")/..

docker-compose -f docker-compose.cpu.yml up --build  -d
docker push hamelsmu/ml-cicd
docker exec -it actions-ml-cicd_cpu_1 bash

#docker run -e DASK_SCHEDULER=$DASK_SCHEDULER -it -p 7654:7654 -v $PWD:/data hamelsmu/ml-cicd bash
