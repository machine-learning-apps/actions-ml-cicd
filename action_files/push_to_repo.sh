#!/bin/bash

set -e
# set -ex

git config --global user.name $GITHUB_ACTOR
git remote add github-pages "https://$GITHUB_ACTOR:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git"
git pull github-pages ${GITHUB_REF} --ff-only
git add docs/docs/model_card.md docs/_data/model_events.csv docs/docs/data_dictionary.md
git commit -m "Update Jupyter Blog Posts" --allow-empty
git push github-pages HEAD:${GITHUB_REF}
