import os, json, requests

fname = os.getenv('GITHUB_EVENT_PATH')
nwo = os.getenv('GITHUB_REPOSITORY')
token = os.getenv('GITHUB_TOKEN')

assert token, 'Error: you must supply the environment variable GITHUB_TOKEN'

with open(fname, 'r') as f:
    raw_payload = json.load(f)

assert 'action' in raw_payload, 'This action is only designed to work with a repository dispatch event.'

payload = eval(raw_payload['action'])

assert isinstance(payload, dict), f'Expecting payload sent in repository dispatch to be a dict.  Instead received: {payload}'
assert 'sha' in payload, 'key sha not found in payload'
assert 'pr_num' in payload, 'key pr_num not found in payload'
assert 'conclusion' in payload, 'key conclusion not found in payload'

pr_num = payload['pr_num']
conclusion = payload['conclusion']
sha = payload['sha']

print(f'::set-output name=SHA::{sha}')
print(f'::set-output name=ISSUE_NUMBER::{pr_num}')
print(f'::set-output name=CONCLUSION::{conclusion}')