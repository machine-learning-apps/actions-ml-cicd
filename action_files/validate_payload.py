#!/usr/bin/env python

import json
import os

fname = os.getenv('GITHUB_EVENT_PATH')

# so you can set this in a WITH statement
test_trigger_label_name = os.getenv('TRIGGER_LABEL_NAME')

# set a default if not supplied
if test_trigger_label_name is None:
    test_trigger_label_name = 'argo/run-test-suite'

with open(fname, 'r') as f:
    val = json.load(f)

assert 'pull_request' in val, 'Error: this action is designed to operate on a payload for which a root node is `pull_request`.'
    
labels = val['pull_request']['labels']
sha = val['pull_request']['head']['sha']
label_names = [label['name'] for label in labels if labels and 'name' in label]
print(label_names)

print('::set-output name=TRIGGERED::{}'.format(test_trigger_label_name in label_names))
print('::set-output name=ISSUE_NUMBER::{}'.format(val['number']))
print('::set-output name=HEAD_SHA::{}'.format(sha))