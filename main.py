import requests
import statistics

issues = [
    "CAMEL-180",
    "CAMEL-321",
    "CAMEL-1818",
    "CAMEL-3214",
    "CAMEL-18065"
]

repo = "apache/camel"

total_commits = 0
files_changed_list = []
dmm_values = []

for issue in issues:
    url = f"https://api.github.com/search/commits?q={issue}+repo:{repo}"
    
    headers = {
        "Accept": "application/vnd.github.cloak-preview"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    commits = data.get("items", [])
    total_commits += len(commits)

    for commit in commits:
        sha = commit["sha"]

        commit_url = f"https://api.github.com/repos/{repo}/commits/{sha}"
        commit_data = requests.get(commit_url).json()

        files = commit_data.get("files", [])
        files_changed_list.append(len(files))

        additions = commit_data["stats"]["additions"]
        deletions = commit_data["stats"]["deletions"]

        dmm = additions + deletions
        dmm_values.append(dmm)

avg_files_changed = statistics.mean(files_changed_list) if files_changed_list else 0
avg_dmm = statistics.mean(dmm_values) if dmm_values else 0

print("Total commits changed:", total_commits)
print("Average files changed:", round(avg_files_changed, 2))
print("Average DMM metrics:", round(avg_dmm, 2))