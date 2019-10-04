import os, json, requests

nwo = os.getenv('GITHUB_REPOSITORY')
sha = os.getenv('SHA')
token = os.getenv('GITHUB_TOKEN')
conclusion = os.getenv('WORKFLOW_CONCLUSION')

assert sha, 'Error: you must supply the environment variable SHA'
assert conclusion, 'Error: you must supply the environment variable WORKFLOW_CONCLUSION'
assert token, 'Error: you must supply the environment variable GITHUB_TOKEN'

url = f'https://api.github.com/repos/{nwo}/check-runs'
headers = {'authorization': f'token {token}',
           'accept': 'application/vnd.github.antiope-preview+json'}

data = {
    'name': 'Argo-Workflow',
    'head_sha': f'{sha}',
    'conclusion': f'{conclusion}',
}

response = requests.post(url=url, headers=headers, json=data)

assert response.status_code == 201, f'Error: Check run API returned status code of {response.status_code}'