# PyRuntime Forge

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/Flask-SocketIO-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask SocketIO">
  <img src="https://img.shields.io/badge/Kubernetes-Docker_Desktop-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB Atlas">
</p>

<p align="center">
  A browser-based Python runtime platform that gives each user an isolated Kubernetes container,
  persistent filesystem state, and interactive stdin support.
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#installation-and-setup">Installation and Setup</a> •
  <a href="#environment-variables">Environment Variables</a> •
  <a href="#api-endpoints">API Endpoints</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#known-limitations">Known Limitations</a>
</p>

---

## Overview

PyRuntime Forge lets users register, log in, and run Python code inside their own Kubernetes pod.

The current execution model is:

```python
command_to_exec = ["python", "-c", command]
```

So the platform is:

- filesystem-stateful
- container-stateful
- not Python-RAM-stateful across separate executions

This means:

- files created in a user's pod remain available between runs
- interactive programs using `input()` now work through the browser UI
- Python variables such as `x = 10` do not survive a new click on `Execute`

---

## Features

- Per-user isolated Python runtime in Kubernetes
- User registration and login backed by MongoDB Atlas
- Python code execution directly from the browser
- Interactive stdin support for `input()`-based programs
- Streaming stdout and stderr output using Socket.IO
- Persistent filesystem inside the user's pod
- File-based data science workflows across multiple executions
- Pre-built user pod image with NumPy, Pandas, scikit-learn, and Matplotlib
- Test-case suite for validating project behavior
- Documentation comparing PyRuntime Forge with Jupyter

---

## Screenshots

### Login And Registration

Users can switch between sign up and login from the same page.

![Login Page](./screenshots/Login_page.png)

![Signup Page](./screenshots/Signup_Page.png)

### Command Console

After login, users can execute Python code and send stdin when the running program calls `input()`.

![Main Console](./screenshots/Main.png)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.9+, Flask, Flask-SocketIO, Eventlet |
| Frontend | HTML, CSS, JavaScript, Socket.IO client |
| Database | MongoDB Atlas |
| Orchestration | Kubernetes on Docker Desktop |
| Runtime Isolation | Per-user Kubernetes Deployment + Pod |
| User Pod Image | `jupyter/datascience-notebook:latest` |
| Custom Pod Base | `python:3.9-slim` with NumPy, Pandas, scikit-learn, Matplotlib (see `Dockerfile`) |
| Execution Model | `python -c "<submitted code>"` inside the user container |
| Configuration | `.env` with `python-dotenv` |
| Test Assets | Ready-to-run Python scripts in `test-cases/` |
| Documentation | Markdown docs in `docs/` |

---

## Project Structure

```text
PyRuntimeForge/
├── docs/
│   └── jupyter-vs-pyruntime-forge.md   # Comparison: PyRuntime Forge vs Jupyter
├── screenshots/
│   ├── Login_page.png
│   ├── Main.png
│   └── Signup_Page.png
├── templates/
│   └── index.html                      # Single-page frontend (auth + code console)
├── test-cases/
│   ├── README.md                       # How to run the test cases
│   ├── data_science_demo_step1.py      # Saves a CSV dataset to the pod
│   ├── data_science_demo_step2.py      # Loads and summarises the saved dataset
│   ├── filesystem_statefulness_step1.py
│   ├── filesystem_statefulness_step2.py
│   ├── interactive_guess_game.py       # Tests interactive stdin support
│   ├── ram_statefulness_step1.py
│   └── ram_statefulness_step2.py
├── .env                                # MongoDB URI (not committed)
├── .gitignore
├── Dockerfile                          # Custom user-pod image (Python 3.9-slim + data science libs)
├── LICENSE
├── README.md
├── requirements.txt                    # Server-side Python dependencies
└── server.py                          # Flask + Socket.IO backend
```

### About the Dockerfile

The `Dockerfile` defines a lightweight custom image for user pods:

```dockerfile
FROM python:3.9-slim
RUN pip install --no-cache-dir numpy pandas scikit-learn matplotlib
```

It is an alternative to `jupyter/datascience-notebook:latest` if you want a smaller image without the full Jupyter stack. To use it, build and push it to a registry, then replace the `image` value in the deployment manifest inside `server.py`.

---

## Installation and Setup

### Prerequisites

Make sure you have:

1. Python 3.9 or newer
2. Docker Desktop installed
3. Kubernetes enabled in Docker Desktop
4. A MongoDB Atlas cluster
5. Your current public IP allowed in Atlas network access

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd PyRuntimeForge
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, Flask-SocketIO, Eventlet, PyMongo, the Kubernetes client, and python-dotenv.

### 4. Verify Kubernetes

```bash
kubectl config current-context
kubectl get nodes
```

Expected context:

```text
docker-desktop
```

### 5. Create `.env`

See the next section for the exact format.

### 6. Run the app

```bash
python server.py
```

Default URL:

```text
http://127.0.0.1:5000
```

### macOS port 5000 note

On some macOS systems, AirPlay / Control Center already uses port `5000`.

If that happens, run:

```bash
python -c "import server; server.socketio.run(server.app, debug=True, port=5001)"
```

Then open:

```text
http://127.0.0.1:5001
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>/<database>?retryWrites=true&w=majority&appName=Cluster0"
```

Current database usage in the code:

- database: `cloud`
- collection: `users`

Example:

```env
MONGODB_URI="mongodb+srv://user:password@cluster0.example.mongodb.net/cloud?retryWrites=true&w=majority&appName=Cluster0"
```

---

## API Endpoints

### HTTP Endpoints

#### `GET /`

Loads the frontend UI.

#### `POST /register`

Registers a user, stores that user in MongoDB Atlas, and creates a per-user Kubernetes deployment.

Example request:

```json
{
  "username": "alice",
  "email": "alice@example.com"
}
```

Example response:

```json
{
  "message": "User alice registered successfully."
}
```

#### `POST /login`

Looks up the user by email and returns the sanitized container identifier.

Example request:

```json
{
  "email": "alice@example.com"
}
```

Example response:

```json
{
  "container_id": "alice"
}
```

### Socket.IO Events

#### Frontend -> Backend

- `execute_command`
  Starts Python execution inside the user's pod.
- `send_stdin`
  Sends one input line to the running process.

#### Backend -> Frontend

- `command_started`
  Signals that execution has started.
- `command_output`
  Streams stdout and stderr back to the browser.
- `command_complete`
  Signals that execution has finished.

---

## How It Works

### Simple Execution Flow

```mermaid
flowchart TD
    A["User opens PyRuntime Forge"] --> B["Register or Login"]
    B --> C["Flask server validates user"]
    C --> D["MongoDB Atlas stores / fetches user"]
    C --> E["Kubernetes creates or finds user pod"]
    E --> F["User submits Python code from browser"]
    F --> G["Backend opens exec session in the user's pod"]
    G --> H["python -c runs the submitted code"]
    H --> I["stdout / stderr streamed back through Socket.IO"]
    I --> J["UI renders output in the console"]

    H --> K{"Program uses input()?"}
    K -- Yes --> L["User types in stdin box"]
    L --> M["Frontend emits send_stdin"]
    M --> H
    K -- No --> I
```

### End-To-End Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Browser UI
    participant S as Flask + Socket.IO Server
    participant DB as MongoDB Atlas
    participant K as Kubernetes API
    participant P as User Pod

    U->>UI: Open app
    UI->>S: GET /
    S-->>UI: Render page

    U->>UI: Register
    UI->>S: POST /register
    S->>DB: Insert user
    S->>K: Create deployment
    K-->>S: Deployment created
    S-->>UI: Registration success

    U->>UI: Login
    UI->>S: POST /login
    S->>DB: Find user
    DB-->>S: Return container_id
    S-->>UI: Login success

    U->>UI: Submit Python code
    UI->>S: execute_command
    S->>K: Find pod by label
    K-->>S: Pod name
    S->>P: exec python -c "submitted code"
    P-->>S: stdout/stderr
    S-->>UI: command_output

    alt input() is called
        U->>UI: Type reply in stdin box
        UI->>S: send_stdin
        S->>P: write to stdin
        P-->>S: more output
        S-->>UI: command_output
    end

    P-->>S: process exits
    S-->>UI: command_complete
```

### Stateful vs Non-Stateful Behavior

PyRuntime Forge remembers:

- files saved in the container
- datasets downloaded inside the pod
- generated CSV files, plots, and outputs written to disk

PyRuntime Forge does not remember:

- Python variables between separate `Execute` clicks
- in-memory pandas dataframes between separate runs
- imported modules in RAM between separate runs

Example:

Execution 1:

```python
x = 12345
print("Stored x =", x)
```

Execution 2:

```python
print(x)
```

Result:

```text
NameError: name 'x' is not defined
```

This is expected because every execution starts a fresh Python process.

---

## Known Limitations

- **No password authentication.** Registration requires only a username and email. This is intentional for a demo/sandbox environment; do not use this in production without adding proper password hashing and session management.
- **No RAM statefulness.** Each `Execute` click runs `python -c`, which starts a fresh interpreter. Python variables and imported modules are not preserved between clicks. Use file I/O to pass data between executions.
- **Pod startup delay.** When a user registers for the first time, Kubernetes must pull the container image. The first execution may fail or stall until the pod reaches the `Running` state. Check pod status with `kubectl get pods`.
- **Single namespace.** All user pods are deployed to the `default` namespace. Usernames must be unique and are sanitized to valid Kubernetes resource names (lowercase alphanumeric and hyphens only).
- **No resource limits.** The deployment manifest does not set CPU or memory limits on user pods. In a production deployment, resource quotas should be configured.

---

## Useful Commands

### Kubernetes status

```bash
kubectl cluster-info
kubectl get nodes
```

### Deployments and pods

```bash
kubectl get deployments
kubectl get pods
kubectl get pods -o wide
```

### Inspect a pod

```bash
kubectl describe pod <pod-name>
```

### Open a shell in a pod

```bash
kubectl exec -it <pod-name> -- /bin/bash
```

If `bash` is unavailable:

```bash
kubectl exec -it <pod-name> -- /bin/sh
```

### Delete a user runtime

```bash
kubectl delete deployment <username>-deployment
```

---

## Documentation and Test Cases

Additional documentation:

- [docs/jupyter-vs-pyruntime-forge.md](./docs/jupyter-vs-pyruntime-forge.md)

Runnable test cases:

- [test-cases/README.md](./test-cases/README.md)
- [test-cases/filesystem_statefulness_step1.py](./test-cases/filesystem_statefulness_step1.py)
- [test-cases/filesystem_statefulness_step2.py](./test-cases/filesystem_statefulness_step2.py)
- [test-cases/ram_statefulness_step1.py](./test-cases/ram_statefulness_step1.py)
- [test-cases/ram_statefulness_step2.py](./test-cases/ram_statefulness_step2.py)
- [test-cases/interactive_guess_game.py](./test-cases/interactive_guess_game.py)
- [test-cases/data_science_demo_step1.py](./test-cases/data_science_demo_step1.py)
- [test-cases/data_science_demo_step2.py](./test-cases/data_science_demo_step2.py)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Prashant Agrawal**

[![GitHub](https://img.shields.io/badge/GitHub-agrawal--2005-181717?style=flat-square&logo=github)](https://github.com/agrawal-2005)

---

<div align="center">

⭐ **If you find this project useful, please give it a star!** ⭐

</div>
