from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from kubernetes import client, config
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# MongoDB client
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['cloud']  
users_collection = db['users']

# Kubernetes API client
from kubernetes.stream import stream
from kubernetes import client, config

# Kubernetes API client
config.load_kube_config()
k8s_apps_v1 = client.AppsV1Api()
k8s_core_v1 = client.CoreV1Api()

def get_pod_name(deployment_name, namespace="default"):
    try:
        # Retrieve the pod associated with the deployment
        print(deployment_name)
        pod_list = k8s_core_v1.list_namespaced_pod(namespace=namespace, label_selector=f"app={deployment_name}")

        # Assuming there's only one pod associated with the deployment
        if pod_list.items:
            return pod_list.items[0].metadata.name
        else:
            return None
    except Exception as e:
        print(f"Error getting pod name: {e}")
        return None

def handle_execute_command1(data):
    command = data['command']
    container_id = data['container_id']  # Extract container ID from user's data
    print(container_id)
    # Specify the namespace where the container resides
    namespace = "default"
    
    # Get the pod name based on the container ID
    pod_name = get_pod_name(container_id, namespace)
    
    if not pod_name:
        return "Pod not found"
    
    # Specify the container name within the pod
    container_name = container_id
    print(pod_name)
    # Command to be executed in the container
    command_to_exec = ["python", "-c", command]
    print(command_to_exec);
    try:
        # Call the Kubernetes API to execute the command
        exec_response = stream(
            k8s_core_v1.connect_get_namespaced_pod_exec,
            name=pod_name,
            namespace=namespace,
            command=command_to_exec,
            container=container_name,
            stderr=True,
            stdin=True,
            stdout=True,
            tty=False
        )
        
        # Extract the output of the command
        print("PRINTING EXEC REPSONSE")
        print(exec_response)
        # command_output = exec_response.output.decode('utf-8')
        return exec_response
    except Exception as e:
        # Handle any exceptions
        return str(e)


# # Usage example:
# data = {
#     "command": "ls -l",
#     "container_id": "my-container"
# }
# output = handle_execute_command(data)
# print(output)


@app.route('/')
def index():
    # Serve the HTML page
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # Extract user registration data from request
    user_data = request.json
    username = user_data.get('username')
    email = user_data.get('email')

    # Create a Kubernetes deployment for the user
    deployment_manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": f"{username}-deployment"
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": username
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": username
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": username,
                            "image": "jupyter/datascience-notebook:latest",
                            "ports": [
                                {
                                    "containerPort": 80
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    # Create the deployment
    k8s_apps_v1.create_namespaced_deployment(body=deployment_manifest, namespace="default")

    # Store user data in MongoDB
    user_document = {
        "username": username,
        "email": email,
        "container_id": f"{username}"  # Assuming container ID is the same as deployment name
    }
    users_collection.insert_one(user_document)
    return user_data

@app.route('/login', methods=['POST'])
def login():
    # Extract login data from request
    login_data = request.json
    email = login_data.get('email')
    print(login_data)
    
    # Query MongoDB to find the user with the given email
    user = users_collection.find_one({"email": email})

    if user:
        container_id = user['container_id']
        # Here you can implement logic to handle container access
        # For example, you can return the container ID and the user can access the container
        return jsonify({"container_id": container_id})
    else:
        return "User not found", 404

@socketio.on('execute_command')
def handle_execute_command(data):
    output = handle_execute_command1(data)   
    emit('command_output', {'output': output})

if __name__ == '__main__':
    socketio.run(app, debug=True)
