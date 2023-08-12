import requests

URL = 'http://127.0.0.1:5000/create'
HEADERS = {'Content-Type': 'application/json'}

# payload
payload = {
  "data": {
    "client_name": "Keystone Dental",
    "record_id": "recPZkIVNjfHqx9rF",
    "client_id": "rec53LXywLsdHrzq8",
    "group_size": "recHwNU36PY43ta0F",
    "funding_tag": "Fully Insured",
    "conditionals": [],
    "renewal_date": "2024-01-01",
    "bor_date": "2022-12-06",
    "ale_status": "Applicable Large Group Employer",
    "ftes": 126
  }
}

response = requests.post(URL, headers=HEADERS, json=payload)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")