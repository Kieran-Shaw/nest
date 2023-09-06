import requests

URL = 'http://127.0.0.1:8080/onboarding'
HEADERS = {'Content-Type': 'application/json'}

# payload
payload = {
  "client_id": "recHfhIo25QoLVVYq",
  "service_plan_id": "recHNBvsvd17FtiZW",
  "client_name": "Kieran Sample",
  "group_size_id": "rectTqaBjnJ0AHMgx",
  "conditionals_id": [
    "recwFKWQUB8KxDoIp"
  ]
}

response = requests.post(URL, headers=HEADERS, json=payload)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")