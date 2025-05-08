from flask import Flask, jsonify, request

from datetime import datetime

app = Flask(__name__)


# -----------------
# Endpoint: Agent Card (Discovery Phase)
# -----------------

# Define an HTTP GET route for the well-known agent discovery path.
# According to the A2A spec, clients discover an agent by call `/.well-known/agent.json`.

@app.route('/.well-known/agent.json', methods=['GET'])
def agent_card():
    # Return metadata about this agent in JSON format.
    # This includes the agent's name, description,base URL, version, and capability of the agent's API.
    return jsonify({
        "name": "Tell Time Agent",
        "description": "An agent that tells the current time.",
        "base_url": "http://localhost:5000",
        "version": "1.0.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
        }
    })


# -----------------
# Endpoint: Task Handling (tasks/send)
# -----------------
def printf(param, task_id):
    pass


@app.route('/tasks/send', methods=['POST'])
def handle_task():
    try:
        # Parse the incoming JSON payload into a python dictionary.
        task = request.get_json()
        print(task)

        # Extract the task ID and user message from the task dictionary.
        # The task ID is used to identify the task in the A2A protocol.
        task_id = task.get('id')
        print(task_id)

        # Extract the user message text from the first message part.
        # A2A represents messages as a list of parts, where the first part usually is a text.
        user_message = task["message"]["parts"][0]["text"]
        print(user_message)

        printf("Received task ID: %s", task_id)
        printf("Received user message: %s", user_message)

    except(KeyError, TypeError, IndexError):
        return jsonify({
            "error": "Invalid task format. Expected JSON with 'id' and 'message' keys."
        }), 400

    # -----------------
    # Generate a response to the user message.
    # -----------------

    current_time = datetime.now().strftime("%H:%M:%S")
    reply_text = f"The current time is {current_time}."

    # Return the properly formatted A2A task response.
    # This includes the original message and a new message from the agent.

    return jsonify({
        "id": task_id,
        "status": {"state": "completed"},
        "messages": [
            task["message"],
            {
                "role": "agent",
                "parts": [{"text": reply_text}]
            }
        ]
    })


# -----------------
# Run the flask server.
# -----------------

if __name__ == '__main__':
    # Start the Flask server on port 5000.
    app.run(port=5000)
