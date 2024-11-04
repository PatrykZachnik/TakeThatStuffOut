import subprocess
import json

# Set organization, project, and PAT (Personal Access Token)
organization = "{organization}"
project = "{project}"
pat = "{PAT}"

# Set Azure DevOps login using subprocess
login_command = [
    "az", "devops", "login", "--organization", f"https://dev.azure.com/{organization}"
]

# Pass the PAT to the az devops login command
process = subprocess.Popen(login_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate(input=f"{pat}\n".encode())

if process.returncode != 0:
    print("Failed to log in to Azure DevOps:", stderr.decode())
else:
    print("Successfully logged in to Azure DevOps")

# List repositories in the project
list_repos_command = [
    "az", "repos", "list", "--project", project, "--organization", f"https://dev.azure.com/{organization}"
]

try:
    result = subprocess.run(list_repos_command, capture_output=True, text=True, check=True)
    repos = json.loads(result.stdout)
    
    # Print each repository's remote URL
    for repo in repos:
        print(f"Clone repository: {repo['remoteUrl']}")

except subprocess.CalledProcessError as e:
    print("Error listing repositories:", e.stderr)
