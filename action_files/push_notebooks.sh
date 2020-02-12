#!/bin/bash

set -e
# set -ex

git config --global user.name $GITHUB_ACTOR
git remote add github-pages "https://$GITHUB_ACTOR:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git"
git pull github-pages ${GITHUB_REF} --ff-only
git add docs/docs/reports
git commit -m "Update Jupyter Blog Posts" --allow-empty
git push github-pages HEAD:${GITHUB_REF}