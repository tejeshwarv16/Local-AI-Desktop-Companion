# test_client.py
import requests
import json

# The URL of our Flask server's /chat endpoint
url = "http://127.0.0.1:5000/chat"

# The data we want to send, in JSON format
payload = {"message": "Why is the sky blue?"}

# The headers to specify that we're sending JSON
headers = {"Content-Type": "application/json"}

print("Sending message to the AI...")

try:
    # Send the POST request
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the AI's response
        ai_response = response.json()
        print("\nAI Response:")
        print(ai_response.get('response', 'No response found.'))
    else:
        print(f"\nError: Received status code {response.status_code}")
        print(f"Response body: {response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"\nConnection Error: Could not connect to the server at {url}.")
    print("Please make sure your 'app.py' server is running.")