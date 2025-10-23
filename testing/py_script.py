#!/usr/bin/env python3
import os, json, urllib.request, urllib.error

repo  = os.environ["REPO"]
pr    = os.environ["PR_NUMBER"]
token = os.environ["GITHUB_TOKEN"]

parts = ref.split("/")

if len(parts) < 3 or not parts[2].isdigit():
    raise SystemExit("Could not determine PR number from GITHUB_REF: " + ref)

pr_number = parts[2]

url  = f"https://api.github.com/repos/{repo}/issues/{pr}/comments"
data = json.dumps({"body": "✅ This Pull Request has been taken in progress by the external bot."}).encode()

req = urllib.request.Request(
    url, data=data, method="POST",
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "ci-external-scripts"
    }
)

try:
    with urllib.request.urlopen(req) as r:
        print("Status:", r.status)
        print("Comment posted.") if r.status == 201 else print("Unexpected response.")
except urllib.error.HTTPError as e:
    print("API error:", e.code, e.read().decode())
    raise SystemExit(1)
