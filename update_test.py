import requests

URL = 'http://127.0.0.1:8080/update'
HEADERS = {'Content-Type': 'application/json'}

# payload
payload = {
    "key": "value"
}

response = requests.post(URL, headers=HEADERS, json=payload)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")