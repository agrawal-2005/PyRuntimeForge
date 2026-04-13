import os
import base64
import tempfile
import threading

from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")
active_exec_sessions = {}
active_exec_sessions_lock = threading.Lock()

# MongoDB client
mongo_client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
db = mongo_client['cloud']
users_collection = db['users']

# Kubernetes API client
# On Render (production): kubeconfig is stored as a base64-encoded env variable.
# Locally: falls back to ~/.kube/config as usual.
# Wrapped in try/except so a missing or malformed kubeconfig does not
# crash the app at startup — errors will surface only when k8s is called.
k8s_apps_v1 = None
k8s_core_v1 = None

try:
    kubeconfig_b64 = os.getenv("KUBECONFIG_BASE64")
    if kubeconfig_b64:
        kubeconfig_yaml = base64.b64decode(kubeconfig_b64).decode("utf-8")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(kubeconfig_yaml)
            _kubeconfig_path = tmp.name
        config.load_kube_config(config_file=_kubeconfig_path)
    else:
        config.load_kube_config()

    k8s_apps_v1 = client.AppsV1Api()
    k8s_core_v1 = client.CoreV1Api()
    print("Kubernetes client initialized successfully.")
except Exception as e:
    print(f"WARNING: Kubernetes client could not be initialized: {e}")
    print("Pod creation and execution will not work until KUBECONFIG_BASE64 is set correctly.")

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


def remove_exec_session(client_sid, exec_response=None):
    with active_exec_sessions_lock:
        session = active_exec_sessions.get(client_sid)
        if session is None:
            return None

        if exec_response is not None and session["exec_response"] is not exec_response:
            return None

        return active_exec_sessions.pop(client_sid)


def close_exec_session(client_sid):
    session = remove_exec_session(client_sid)
    if session is None:
        return

    exec_response = session["exec_response"]

    try:
        exec_response.write_stdin("\x03")
    except Exception:
        pass

    try:
        exec_response.close()
    except Exception:
        pass


def emit_command_error(client_sid, message):
    socketio.emit('command_output', {'output': f"{message}\n"}, to=client_sid)
    socketio.emit('command_complete', to=client_sid)


def stream_command_output(client_sid, exec_response):
    try:
        while exec_response.is_open():
            exec_response.update(timeout=1)

            if exec_response.peek_stdout():
                socketio.emit(
                    'command_output',
                    {'output': exec_response.read_stdout()},
                    to=client_sid
                )

            if exec_response.peek_stderr():
                socketio.emit(
                    'command_output',
                    {'output': exec_response.read_stderr()},
                    to=client_sid
                )
    except Exception as e:
        socketio.emit(
            'command_output',
            {'output': f"\nAn unexpected error occurred: {str(e)}\n"},
            to=client_sid
        )
    finally:
        try:
            exec_response.close()
        except Exception:
            pass

        remove_exec_session(client_sid, exec_response)
        socketio.emit('command_complete', to=client_sid)


def start_exec_session(data, client_sid):
    if k8s_core_v1 is None:
        emit_command_error(client_sid, "Error: Kubernetes is not configured on this server.")
        return

    command = data['command']
    username = data['container_id']  # This is actually the username
    namespace = "default"

    pod_name = get_pod_name(username, namespace)

    if not pod_name:
        emit_command_error(client_sid, f"Error: Could not find a running pod for user '{username}'.")
        return

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
            stdin=True,
            stdout=True,
            tty=False,
            _preload_content=False
        )

        with active_exec_sessions_lock:
            active_exec_sessions[client_sid] = {
                "exec_response": exec_response,
            }

        socketio.emit('command_started', to=client_sid)
        socketio.start_background_task(stream_command_output, client_sid, exec_response)

    except ApiException as e:
        emit_command_error(client_sid, f"Kubernetes API Error: {e.reason}")
    except Exception as e:
        emit_command_error(client_sid, f"An unexpected error occurred: {str(e)}")
    
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
    if k8s_apps_v1 is None:
        return jsonify({"error": "Kubernetes is not configured on this server."}), 503

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
    client_sid = request.sid
    close_exec_session(client_sid)
    start_exec_session(data, client_sid)


@socketio.on('send_stdin')
def handle_send_stdin(data):
    client_sid = request.sid

    with active_exec_sessions_lock:
        session = active_exec_sessions.get(client_sid)

    if session is None:
        emit('command_output', {'output': "No running command is available for input.\n"})
        emit('command_complete')  # Reset the frontend "Running..." state
        return

    user_input = data.get('input', '')

    try:
        session["exec_response"].write_stdin(f"{user_input}\n")
    except Exception as e:
        emit('command_output', {'output': f"Failed to send input: {str(e)}\n"})


@socketio.on('disconnect')
def handle_disconnect():
    close_exec_session(request.sid)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") != "production"
    socketio.run(app, host="0.0.0.0", port=port, debug=debug)
