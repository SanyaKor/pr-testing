#!/usr/bin/env python3
import os, json, urllib.request, urllib.error

repo = os.environ["GITHUB_REPOSITORY"]
ref  = os.environ["GITHUB_REF"]
token = os.environ["GITHUB_TOKEN"]

parts = ref.split("/")
if len(parts) < 3 or not parts[2].isdigit():
    raise SystemExit("Не получилось определить номер PR из GITHUB_REF: " + ref)
pr_number = parts[2]

url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
data = json.dumps({"body": "✅ Взято в работу. Бот отписался."}).encode()

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
        if r.status == 201:
            print("Комментарий добавлен.")
        else:
            print("Неожиданный статус:", r.status, r.read().decode())
except urllib.error.HTTPError as e:
    print("Ошибка API:", e.code, e.read().decode())
