# Graph Report - .  (2026-04-15)

## Corpus Check
- Corpus is ~35,900 words - fits in a single context window. You may not need a graph.

## Summary
- 84 nodes · 112 edges · 18 communities detected
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 17 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Execution Engine Core|Execution Engine Core]]
- [[_COMMUNITY_Architecture Rationale|Architecture Rationale]]
- [[_COMMUNITY_API and Deployment Config|API and Deployment Config]]
- [[_COMMUNITY_Frontend UI Screens|Frontend UI Screens]]
- [[_COMMUNITY_Infrastructure and Auth|Infrastructure and Auth]]
- [[_COMMUNITY_Web Server Stack|Web Server Stack]]
- [[_COMMUNITY_Filesystem Statefulness Tests|Filesystem Statefulness Tests]]
- [[_COMMUNITY_User Pod Configuration|User Pod Configuration]]
- [[_COMMUNITY_Interactive IO Features|Interactive IO Features]]
- [[_COMMUNITY_Guess Game Logic|Guess Game Logic]]
- [[_COMMUNITY_Auth Form Fields|Auth Form Fields]]
- [[_COMMUNITY_RAM Statefulness Test 2|RAM Statefulness Test 2]]
- [[_COMMUNITY_Data Science Demo Step 2|Data Science Demo Step 2]]
- [[_COMMUNITY_Filesystem Test Step 1|Filesystem Test Step 1]]
- [[_COMMUNITY_Filesystem Test Step 2|Filesystem Test Step 2]]
- [[_COMMUNITY_Data Science Demo Step 1|Data Science Demo Step 1]]
- [[_COMMUNITY_RAM Statefulness Test 1|RAM Statefulness Test 1]]
- [[_COMMUNITY_Signup Username Field|Signup Username Field]]

## God Nodes (most connected - your core abstractions)
1. `PyRuntime Forge` - 35 edges
2. `Login Form UI` - 7 edges
3. `server.py (Flask + Socket.IO Backend)` - 6 edges
4. `Filesystem Statefulness` - 6 edges
5. `RAM Non-Statefulness` - 6 edges
6. `Command Console UI (Main Page)` - 6 edges
7. `User Pod (Kubernetes Pod per User)` - 5 edges
8. `Jupyter vs PyRuntime Forge Comparison Document` - 5 edges
9. `Signup / Registration Form UI` - 5 edges
10. `close_exec_session()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Filesystem Statefulness` --semantically_similar_to--> `Container Statefulness`  [INFERRED] [semantically similar]
  README.md → docs/jupyter-vs-pyruntime-forge.md
- `Python Kernel Statefulness (Jupyter)` --semantically_similar_to--> `RAM Non-Statefulness`  [INFERRED] [semantically similar]
  docs/jupyter-vs-pyruntime-forge.md → README.md
- `PyRuntime Forge` --references--> `Flask`  [EXTRACTED]
  README.md → requirements.txt
- `PyRuntime Forge` --references--> `PyMongo`  [EXTRACTED]
  README.md → requirements.txt
- `PyRuntime Forge` --references--> `Kubernetes Python Client`  [EXTRACTED]
  README.md → requirements.txt

## Hyperedges (group relationships)
- **Code Execution Pipeline: Socket.IO → Kubernetes Exec → stdout Streaming** — readme_execute_command_event, readme_user_pod, readme_socketio_streaming, readme_execution_model [EXTRACTED 1.00]
- **Statefulness Trade-off: Container-Stateful but Not RAM-Stateful** — readme_filesystem_statefulness, readme_ram_non_statefulness, docs_container_stateful, docs_python_kernel_stateful [EXTRACTED 0.95]
- **User Registration: Flask Endpoint → MongoDB Storage → Kubernetes Deployment** — readme_register_endpoint, readme_mongodb_atlas, readme_kubernetes, readme_user_pod [EXTRACTED 1.00]
- **PyRuntime Forge UI Screen Set** — main_commandconsole, loginpage_loginform, signuppage_signupform [INFERRED 0.95]
- **Authentication UI Pages (Login + Signup)** — loginpage_loginform, signuppage_signupform, shared_authflow [INFERRED 0.90]
- **Consistent Purple Design System Across All Pages** — main_commandconsole, loginpage_loginform, signuppage_signupform, shared_designsystem [INFERRED 0.85]

## Communities

### Community 0 - "Execution Engine Core"
Cohesion: 0.18
Nodes (12): close_exec_session(), emit_command_error(), get_pod_name(), handle_disconnect(), handle_execute_command(), Sanitizes a string to be a valid Kubernetes resource name., Finds a pod based on the 'app=<username>' label., register() (+4 more)

### Community 1 - "Architecture Rationale"
Cohesion: 0.24
Nodes (11): Container Statefulness, Jupyter Notebook, Jupyter vs PyRuntime Forge Comparison Document, Python Kernel Statefulness (Jupyter), Rationale: python -c Is Simple and Reliable, Rationale: Value Without RAM Statefulness, Use Cases (Data Preprocessing, Teaching, Sandboxed Execution), Execution Model (python -c) (+3 more)

### Community 2 - "API and Deployment Config"
Cohesion: 0.22
Nodes (10): Socket.IO command_complete Event, Socket.IO command_output Event, .env Configuration File, Socket.IO execute_command Event, Dockerfile (Flask Server Image / Render), index.html (Single-Page Frontend), PyRuntime Forge, Socket.IO send_stdin Event (+2 more)

### Community 3 - "Frontend UI Screens"
Cohesion: 0.36
Nodes (10): Login Form UI, Register Here Link (Login Page), Command Console UI (Main Page), Execute Button (Python Command Runner), Login Success Notification, PyRuntime Forge Application, User Authentication Flow, Shared UI Design System (Purple Theme) (+2 more)

### Community 4 - "Infrastructure and Auth"
Cohesion: 0.29
Nodes (7): Docker Desktop, Kubernetes, POST /login Endpoint, MongoDB Atlas, No Password Authentication (Known Limitation), POST /register Endpoint, Single Namespace Limitation

### Community 5 - "Web Server Stack"
Cohesion: 0.33
Nodes (6): server.py (Flask + Socket.IO Backend), Eventlet, Flask, Flask-SocketIO, Kubernetes Python Client, PyMongo

### Community 6 - "Filesystem Statefulness Tests"
Cohesion: 0.4
Nodes (5): Filesystem Statefulness, data_science_demo_step1.py, data_science_demo_step2.py, filesystem_statefulness_step1.py, filesystem_statefulness_step2.py

### Community 7 - "User Pod Configuration"
Cohesion: 0.5
Nodes (5): jupyter/datascience-notebook:latest Image, No Resource Limits Limitation, pod.Dockerfile (Custom User Pod Image), Pod Startup Delay Limitation, User Pod (Kubernetes Pod per User)

### Community 8 - "Interactive IO Features"
Cohesion: 0.67
Nodes (3): Interactive stdin Support (input()), Socket.IO Streaming Output, interactive_guess_game.py

### Community 9 - "Guess Game Logic"
Cohesion: 1.0
Nodes (0): 

### Community 10 - "Auth Form Fields"
Cohesion: 1.0
Nodes (2): Email Input Field (Login), Email Input Field (Signup)

### Community 11 - "RAM Statefulness Test 2"
Cohesion: 1.0
Nodes (0): 

### Community 12 - "Data Science Demo Step 2"
Cohesion: 1.0
Nodes (0): 

### Community 13 - "Filesystem Test Step 1"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Filesystem Test Step 2"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Data Science Demo Step 1"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "RAM Statefulness Test 1"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Signup Username Field"
Cohesion: 1.0
Nodes (1): Username Input Field (Signup)

## Knowledge Gaps
- **22 isolated node(s):** `Finds a pod based on the 'app=<username>' label.`, `Sanitizes a string to be a valid Kubernetes resource name.`, `Gunicorn`, `Docker Desktop`, `Socket.IO execute_command Event` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Guess Game Logic`** (2 nodes): `guess_the_number()`, `interactive_guess_game.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Auth Form Fields`** (2 nodes): `Email Input Field (Login)`, `Email Input Field (Signup)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `RAM Statefulness Test 2`** (1 nodes): `ram_statefulness_step2.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Data Science Demo Step 2`** (1 nodes): `data_science_demo_step2.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Filesystem Test Step 1`** (1 nodes): `filesystem_statefulness_step1.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Filesystem Test Step 2`** (1 nodes): `filesystem_statefulness_step2.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Data Science Demo Step 1`** (1 nodes): `data_science_demo_step1.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `RAM Statefulness Test 1`** (1 nodes): `ram_statefulness_step1.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Signup Username Field`** (1 nodes): `Username Input Field (Signup)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PyRuntime Forge` connect `API and Deployment Config` to `Architecture Rationale`, `Infrastructure and Auth`, `Web Server Stack`, `Filesystem Statefulness Tests`, `User Pod Configuration`, `Interactive IO Features`?**
  _High betweenness centrality (0.276) - this node is a cross-community bridge._
- **Why does `RAM Non-Statefulness` connect `Architecture Rationale` to `API and Deployment Config`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `User Pod (Kubernetes Pod per User)` connect `User Pod Configuration` to `API and Deployment Config`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Login Form UI` (e.g. with `Command Console UI (Main Page)` and `Login Success Notification`) actually correct?**
  _`Login Form UI` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `RAM Non-Statefulness` (e.g. with `Execution Model (python -c)` and `Python Kernel Statefulness (Jupyter)`) actually correct?**
  _`RAM Non-Statefulness` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Finds a pod based on the 'app=<username>' label.`, `Sanitizes a string to be a valid Kubernetes resource name.`, `Gunicorn` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._