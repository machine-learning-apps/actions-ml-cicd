#!/bin/sh

set -e
cd $(dirname "$0")/..

docker build --no-cache -f docker/nbdev.Dockerfile -t nbdev .