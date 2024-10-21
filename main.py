import requests
from requests.auth import HTTPBasicAuth

# Replace these with your Azure DevOps information
organization = "your_organization_name"  # e.g., 'myorganization'
project = "your_project_name"            # e.g., 'myproject'
personal_access_token = "your_pat_token" # e.g., 'xyzxyzxyzxyzxyz'
api_version = "6.0"  # API version

# Azure DevOps Repositories API URL to list repositories
repo_url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version={api_version}"

# Function to get the list of repositories
def get_repositories():
    response = requests.get(repo_url, auth=HTTPBasicAuth('', personal_access_token))
    if response.status_code == 200:
        return response.json()["value"]
    else:
        print(f"Failed to retrieve repositories: {response.status_code} - {response.text}")
        return []

# Function to list files in a repository and return them as an array
def list_files_in_repo(repo_id):
    # URL to fetch files from the repository
    items_url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_id}/items?recursionLevel=Full&api-version={api_version}"
    
    response = requests.get(items_url, auth=HTTPBasicAuth('', personal_access_token))
    
    file_paths = []
    
    if response.status_code == 200:
        items = response.json()["value"]
        for item in items:
            if item['gitObjectType'] == 'blob':  # Only list files (blobs), skip folders (trees)
                file_paths.append(item['path'])
    else:
        print(f"Failed to retrieve files for repository: {response.status_code} - {response.text}")
    
    return file_paths

# Main logic
repositories = get_repositories()
all_files = []

# Loop through each repository, get its files, and add them to the all_files array
if repositories:
    for repo in repositories:
        repo_id = repo['id']
        repo_name = repo['name']
        print(f"Listing files for repository: {repo_name}")
        
        # Get files for the current repository and add them to the all_files list
        files_in_repo = list_files_in_repo(repo_id)
        all_files.extend(files_in_repo)

# Output the combined list of files
print("\nCombined list of files from all repositories:")
print(all_files)
