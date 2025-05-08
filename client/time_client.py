import requests

import uuid

# ---------------
# Step1 - Discover the Agent
# ---------------

# Define the base URL where the agent server is running.
BASE_URL = "http://localhost:5000"

# Use HTTP GET to discover the agent's cards from the well-known path (or endpoint).
response = requests.get(f"{BASE_URL}/.well-known/agent.json")

if response.status_code != 200:
    raise Exception("Failed to discover agent. Check if the server is running.")

# Parse the agent's card from the response JSON.
agent_card = response.json()
print(f"Agent Name: {agent_card['name']} - Agenrt Description: {agent_card['description']}")

# ---------------
# Step2 - Prepare a task payload for the Agent
# ---------------

task_id = str(uuid.uuid4())  # Generate a unique task ID.
# Construct a A2A task payload.
task_payload = {
    "id": task_id,
    "message": {
        "parts": [
            {
                "text": "What time is it?",
            }
        ]
    }
}

# ---------------
# Step3 - Send a Task to the Agent
# ---------------

# Use HTTP POST to send the task payload to the agent's task handling endpoint(/tasks/send).
response = requests.post(f"{BASE_URL}/tasks/send", json=task_payload)

if response.status_code != 200:
    raise Exception(f"Task Failed. {response.status_code}: {response.text}")

data = response.json()
print(f"Task ID: {data['id']} - Task Status: {data['status']}")

# Extract the agent's response from the JSON payload.
messages = data.get("messages", {})

if messages:
    # Extract the text part of the first message.
    reply_text = messages[-1]["parts"][0]["text"]
    print(f"Agent's Reply: {reply_text}")
else:
    print("No messages found in the agent's response.")