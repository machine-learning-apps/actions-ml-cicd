#!/bin/sh
set -e
cd $(dirname "$0")/..

if [ ! -d "nbdev" ]; then
    git clone https://github.com/fastai/nbdev.git
    pip install -e nbdev
    cp nbdev/settings.ini .
fi

# find docs/_notebooks -type f -delete

python action_files/nb2docs.py