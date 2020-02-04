#!/bin/bash

set -e
# set -ex

dirs=( "$@" )
echo "Generating push for $dirs"

# setup ssh: allow key to be used without a prompt and start ssh agent
export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
eval "$(ssh-agent -s)"

# Setup Git credentials if we are planning to change the data in the repo
git config --global user.name "$GITHUB_ACTOR"
git config --global user.email "$USER_EMAIL"
git remote add pages-origin "git@github.com:$GITHUB_REPOSITORY.git"
echo $ACTIONS_DEPLOY_KEY | base64 -d > mykey
chmod 400 mykey
ssh-add mykey

git pull pages ${GITHUB_REF} --ff-only
git add $dirs
git commit -m "Update ds-pages" --allow-empty
git push github HEAD:${GITHUB_REF}