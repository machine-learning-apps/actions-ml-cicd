#!/bin/bash
docker run -it -p 8887:8887 -p 4040:4040 -v $PWD:/home/jovyan/mlops nbdev /bin/sh