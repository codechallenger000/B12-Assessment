import json
import hmac
import hashlib
import datetime
import sys
import requests

SIGNING_SECRET = b"hello-there-from-b12"
ENDPOINT = "https://b12.io/apply/submission"

payload = {
    "action_run_link": "https://github.com/codechallenger000/B12-Assessment/actions/runs/21640031438",
    "email": "dalinhuang12@gmail.com",
    "name": "Dalin Huang",
    "repository_link": "https://github.com/codechallenger000/B12-Assessment",
    "resume_link": "https://flowcv.com/resume/v8ona0poosq9",
    "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
}

body = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode("utf-8")

digest = hmac.new(SIGNING_SECRET, body, hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={digest}",
}

response = requests.post(ENDPOINT, data=body, headers=headers)

if response.status_code != 200:
    print("Submission failed")
    print(response.status_code, response.text)
    sys.exit(1)

data = response.json()
print(data.get("receipt"))
