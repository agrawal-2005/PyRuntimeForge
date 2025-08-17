from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from flask_socketio import SocketIO, emit
import re

app = Flask(__name__)
socketio = SocketIO(app)

# MongoDB client
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['cloud']
users_collection = db['users']

# Kubernetes API client
config.load_kube_config()
k8s_apps_v1 = client.AppsV1Api()
k8s_core_v1 = client.CoreV1Api()

def get_pod_name(username, namespace="default"):
    """
    FIXED: Finds a pod based on the 'app=<username>' label.
    """
    try:
        # The label selector must match the label set in the deployment template
        pod_list = k8s_core_v1.list_namespaced_pod(
            namespace=namespace,
            label_selector=f"app={username}" # This was the main bug
        )
        if pod_list.items:
            # Return the name of the first pod found
            return pod_list.items[0].metadata.name
        else:
            print(f"No pod found for username: {username}")
            return None
    except ApiException as e:
        print(f"Error getting pod name for {username}: {e}")
        return None

def handle_execute_command_internal(data):
    command = data['command']
    username = data['container_id']  # This is actually the username
    namespace = "default"

    pod_name = get_pod_name(username, namespace)

    if not pod_name:
        return f"Error: Could not find a running pod for user '{username}'."

    # The container name is the same as the username in the deployment manifest
    container_name = username
    
    # We execute the user's code via Python's -c flag
    command_to_exec = ["python", "-c", command]
    
    try:
        # Use the stream function to execute the command and get output
        exec_response = stream(
            k8s_core_v1.connect_get_namespaced_pod_exec,
            name=pod_name,
            namespace=namespace,
            command=command_to_exec,
            container=container_name,
            stderr=True,
            stdin=False, # No input needed
            stdout=True,
            tty=False,
            _preload_content=False
        )

        output = ""
        while exec_response.is_open():
            exec_response.update(timeout=1)
            if exec_response.peek_stdout():
                output += exec_response.read_stdout()
            if exec_response.peek_stderr():
                output += exec_response.read_stderr()
        
        # Ensure the response is closed
        exec_response.close()

        return output if output else "[No output produced]"

    except ApiException as e:
        return f"Kubernetes API Error: {e.reason}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    
def sanitize_for_k8s(name):
    """Sanitizes a string to be a valid Kubernetes resource name."""
    # Convert to lowercase
    name = name.lower()
    # Replace any character that is not a lowercase letter, number, or hyphen with a hyphen
    name = re.sub('[^a-z0-9-]', '-', name)
    # Ensure it doesn't start or end with a hyphen
    name = name.strip('-')
    return name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    user_data = request.json
    original_username = user_data.get('username')
    email = user_data.get('email')
    namespace = "default"

    # Sanitize the username for use in Kubernetes
    k8s_username = sanitize_for_k8s(original_username)

    deployment_name = f"{k8s_username}-deployment"

    deployment_manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": deployment_name}, # Use sanitized name
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": k8s_username}},
            "template": {
                "metadata": {"labels": {"app": k8s_username}},
                "spec": {
                    "containers": [{
                        "name": k8s_username, # Use sanitized name
                        "image": "jupyter/datascience-notebook:latest",
                        "ports": [{"containerPort": 80}]
                    }]
                }
            }
        }
    }

    # ... (the rest of your try/except block) ...
    # Make sure to use 'deployment_name' in your try/except block
    try:
        k8s_apps_v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)
        # ...
    except ApiException as e:
        if e.status == 404:
            k8s_apps_v1.create_namespaced_deployment(
                body=deployment_manifest,
                namespace=namespace
            )
            # ...

    # When storing in MongoDB, you can store both the original and sanitized names if needed,
    # but for container_id, use the sanitized one.
    if not users_collection.find_one({"email": email}):
        users_collection.insert_one({
            "username": original_username, # Store original for display
            "email": email,
            "container_id": k8s_username # This MUST be the sanitized name
        })

    return jsonify({"message": f"User {original_username} registered successfully."})


@app.route('/login', methods=['POST'])
def login():
    login_data = request.json
    email = login_data.get('email')
    
    user = users_collection.find_one({"email": email})

    if user:
        # The 'container_id' we store is just the username
        return jsonify({"container_id": user['container_id']})
    else:
        return jsonify({"error": "User not found"}), 404

@socketio.on('execute_command')
def handle_execute_command(data):
    output = handle_execute_command_internal(data)
    emit('command_output', {'output': output})

if __name__ == '__main__':
    socketio.run(app, debug=True)