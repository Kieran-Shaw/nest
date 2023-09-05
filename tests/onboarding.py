import requests

URL = 'http://127.0.0.1:8080/onboarding'
HEADERS = {'Content-Type': 'application/json'}

# payload
payload = {
  "client_id": "rec3XMI5ahwaSucPG",
  "service_plan_id": "recaOgS9lAfvifcKo",
  "client_name": "Sample Client"
}

response = requests.post(URL, headers=HEADERS, json=payload)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")