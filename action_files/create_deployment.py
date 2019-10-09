import requests
import os

branch_name = os.getenv("BRANCH_NAME")
run_id = os.getenv("RUN_ID")
app_token = os.getenv("TOKEN")
repo = os.getenv("GITHUB_REPOSITORY")

assert branch_name, "Environment variable BRANCH_NAME must be supplied."
assert run_id, "Environment variable RUN_ID must be supplied."
assert app_token, "Environment variable APP_TOKEN must be supplied."
assert repo, "System Environment variable GITHUB_REPOSITORY not found."

data = {"ref": branch_name, "payload":{"wandb_run_id":run_id}}
headers = {"Authorization": f"token {app_token}"}
url = f"https://api.github.com/repos/{repo}/deployments"

response = requests.post(url=url, headers=headers, json=data)
assert response, f"Error: attempt to create deployment failed, received {response.status_code}"

# if you get a 202 this means that it needs to merge master into the current branch
if response.status_code == 202:
    response = requests.post(url=url, headers=headers, json=data)
    assert response, f"Error: attempt to create deployment failed, received {response.status_code}"

print(f'Successfully created deployment for run_id: {run_id}')
print(response.content)
