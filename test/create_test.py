import requests

URL = 'http://127.0.0.1:8080/create'
HEADERS = {'Content-Type': 'application/json'}

# payload
payload = {
  "service_plan_id": "recdnv3mtLnwp7QhP",
  "client_id": "rec3XMI5ahwaSucPG",
  "client_name": "Sample Client",
  "group_size_id": "reck9MsWaYbOr1i3b",
  "conditionals_id": []
}

response = requests.post(URL, headers=HEADERS, json=payload)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")