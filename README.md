# PyRuntime Forge

PyRuntime Forge is a web-based application that provides "Jupyter Notebook as a Service." It allows users to register and receive their own personal, isolated coding environment running inside a Kubernetes cluster. Users can log in and execute Python code directly from their browser, with the output streamed back in real-time.

## Features

- **User Registration & Login:** Securely register users and store their details in a MongoDB database.
- **Dynamic Environment Provisioning:** Automatically creates a dedicated Jupyter Notebook container for each new user in a Kubernetes cluster.
- **Isolated Runtimes:** Each user's coding environment is a separate Kubernetes pod, ensuring isolation and security.
- **Remote Code Execution:** Users can execute Python code from a web-based console.
- **Real-time Output:** Command output is streamed back to the user's browser instantly using WebSockets.
- **Modern Frontend:** A clean, responsive user interface with a toggle for login/registration and on-page notifications.

## Technology Stack

- **Backend:** Flask, Flask-SocketIO
- **Database:** MongoDB
- **Orchestration:** Kubernetes
- **Frontend:** HTML5, CSS3, JavaScript (with Socket.IO client)
- **Python Libraries:** `pymongo`, `kubernetes`

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

1.  **Python 3:** Make sure `python3` and `pip` are available in your terminal.
2.  **Docker Desktop:** Required to run a local Kubernetes cluster.
    - [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
3.  **Kubernetes (via Docker Desktop):** Enable the Kubernetes cluster within Docker Desktop's settings.
4.  **Homebrew:** The package manager for macOS (used to install MongoDB).
    - [Install Homebrew](https://brew.sh/)
5.  **MongoDB Community Edition:**
    - Install using Homebrew: `brew install mongodb-community`

## Setup and Installation

Follow these steps to get the application running locally.

1.  **Clone the Repository (if applicable)**
    ```bash
    git clone <your-repository-url>
    cd PyRuntimeForge-main
    ```

2.  **Create and Activate a Python Virtual Environment**
    ```bash
    # Create the environment
    python3 -m venv venv

    # Activate it (on macOS/Linux)
    source venv/bin/activate
    ```

3.  **Install Python Dependencies**
    It's best to create a `requirements.txt` file with all the necessary packages.

    **`requirements.txt`:**
    ```
    flask
    flask-socketio
    pymongo
    kubernetes
    ```

    Then, install them with a single command:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start Required Services**

    - **Start the Kubernetes Cluster:**
      Open Docker Desktop and ensure the Kubernetes cluster is running (the icon in the bottom-left should be green).

    - **Start the MongoDB Service:**
      ```bash
      brew services start mongodb-community
      ```

5.  **Run the Application**
    ```bash
    python3 server.py
    ```
    The application will be available at **http://127.0.0.1:5000**.

## How to Use

1.  Open your web browser and navigate to `http://127.0.0.1:5000`.
2.  Use the **"Create an Account"** form to register a new user.
3.  After successful registration, you will be switched to the login form.
4.  Use the **"Welcome Back!"** form to log in with the same email you used to register.
5.  Upon successful login, the **Command Console** will appear.
6.  Enter any Python code into the text area and click **"Execute"** to see the output.

## Important Commands

Here is a summary of useful commands to manage your local development environment.

#### Kubernetes (`kubectl`)

- **Check cluster status:**
  ```bash
  kubectl cluster-info
  ```
- **List all running deployments:**
  ```bash
  kubectl get deployments
  ```
- **List all running pods (user containers):**
  ```bash
  kubectl get pods
  ```
- **Delete a specific user's deployment:**
  ```bash
  # Replace <username> with the sanitized username
  kubectl delete deployment <username>-deployment
  ```

#### MongoDB (`brew services`)

- **Start the MongoDB server:**
  ```bash
  brew services start mongodb-community
  ```
- **Stop the MongoDB server:**
  ```bash
  brew services stop mongodb-community
  ```
- **Check the status of all Homebrew services:**
  ```bash
  brew services list
  ```

## Security Considerations ⚠️

This project is a proof-of-concept and has **significant security vulnerabilities**. It should **NOT** be deployed to a public-facing production environment without major modifications.

- **Arbitrary Code Execution:** The application allows any user to run any code inside a container on your cluster.
- **No Authentication:** There is no password system; login is based solely on email.
- **No Resource Limits:** A user could easily consume all available CPU and memory by running an infinite loop.
