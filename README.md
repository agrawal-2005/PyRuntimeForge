# PyRuntimeForge

**PyRuntimeForge** is a dynamic Flask-based web application that provisions personalized Kubernetes-based runtime environments for users. It allows users to train or deploy projects seamlessly in isolated, containerized Jupyter environments.

## 🚀 Features

- 🔐 **User Authentication**  
  Secure user registration and login system with MongoDB for managing user sessions.

- ⚙️ **Dynamic Environment Provisioning**  
  Automatically provisions unique Jupyter container environments per user using Kubernetes.

- 🧪 **Isolated Execution**  
  Each user interacts with a dedicated container identified via a unique container ID.

- 🔄 **Real-time Communication**  
  WebSocket-based communication using Flask-SocketIO to execute commands in real time inside the user’s container.

## 🛠️ Tech Stack

- **Backend:** Flask, Flask-SocketIO  
- **Container Orchestration:** Kubernetes  
- **Database:** MongoDB  
- **Others:** Docker, Jupyter Notebook

## 📦 Setup & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/PyRuntimeForge.git
   cd PyRuntimeForge

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
  

3. **Configure environment variables** (MongoDB URI, Kubernetes config, etc.)

4. **Run the Flask app**

   ```bash
   python app.py

> Ensure Kubernetes cluster is running and configured correctly.

## 🧠 Inspiration

This project was built to support dynamic runtime environments for users needing isolated compute sessions—ideal for ML training, educational environments, or multi-user notebooks.

## 📄 License
This project is licensed under the [MIT License](./LICENSE).
