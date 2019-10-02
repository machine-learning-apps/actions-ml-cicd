import os
import requests
import argparse

token = os.getenv('GITHUB_TOKEN')
location = os.getenv('GITHUB_REPOSITORY')
sha = os.getenv('SHA')

assert token, "Must supply input GITHUB_TOKEN"
assert location, "Must supply input GITHUB_REPOSITORY"
assert sha, "Must supply input SHA"

url = f'https://api.github.com/repos/{location}/check-runs'
headers = {'authorization': f'token {token}',
           'accept': 'application/vnd.github.antiope-preview+json'}

parser = argparse.ArgumentParser(description='Interact with the Checks Api.')
parser.add_argument('status', help="either in_progress, or completed")
parser.add_argument('name')
parser.add_argument('title')
parser.add_argument('summary')
parser.add_argument('text')

def trigger_check(cli_args):
    "Create a checkrun using the GitHub REST API."
    status, name, title, summary, text = cli_args.status, cli_args.name, cli_args.title, cli_args.summary, cli_args.text
    
    payload = {
        'name': f'{name}',
        'head_sha': f'{sha}',
        'status': f'{status}',
        'output':{
            'title': f'{title}',
            'summary': f'{summary}',
            'text': f'{text}'
        },
    }
    print(payload)
    response = requests.post(url=url, headers=headers, json=payload)
    assert response.status_code == 201, f"Received status code of {response.status_code}"

if __name__ == '__main__':
    args = parser.parse_args()
    trigger_check(cli_args=args)
