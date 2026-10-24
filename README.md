# OpenNavy

### The Sovereign Fleet Navigator for Open Source Codebases

**License:** MIT License  
**Target Tracks:** Best Open-Source AI Project (DigitalOcean / Hacktoberfest 2026) | Best Use of Gemma 4 (Google DeepMind)

---

## 1. Overview

OpenNavy is a sovereign, local-first developer cockpit and architectural radar engineered to eliminate cognitive friction when onboarding and contributing to complex open-source codebases.

Built for privacy-conscious teams and enterprise environments where compliance prohibits sending source code to third-party cloud APIs, OpenNavy runs entirely on local infrastructure. It pairs universal Abstract Syntax Tree (AST) static analysis with local multimodal intelligence powered by **Google Gemma 4**, allowing developers to translate GitHub issues or bug screenshots into verified code waypoints while detecting architectural collisions over a local network mesh in real time.

---

## 2. Core Capabilities

### 2.1 The Nautical Chart (AST Topography and Reef Warnings)
- **Universal Multi-Language Parsing:** Extracts structural syntax trees across Python, TypeScript, JavaScript, Go, and Java using Tree-sitter.
- **Topological Risk Detection:** Applies Tarjan's Strongly Connected Components (SCC) algorithm to identify cyclical dependencies and highly coupled modules ("Reefs"), alerting developers before introducing risky architectural coupling.

### 2.2 The Course Plotter (Multimodal Issue-to-Waypoints)
- **Gemma 4 Multimodal Reasoning:** Accepts issue descriptions, bug reports, and graphical artifacts (such as UI error screenshots or stack trace captures).
- **Zero-Hallucination Waypoints:** Gemma 4 cross-references its reasoning trace (`<|think|>`) with the local AST graph to generate precise file targets, line ranges, step-by-step implementation tasks, and a ready-to-use pull request draft.

### 2.3 The Fleet Sonar (Zero-Cloud LAN Multiplayer Radar)
- **Local Network Coordination:** Operates a lightweight WebSocket hub enabling co-located developers on the same Wi-Fi or LAN subnet to broadcast navigation state without central cloud accounts.
- **Pre-Merge Collision Detection:** Cross-references active teammate focus against the Tarjan coupling matrix in real time, triggering visual warnings when two developers work on interconnected modules before Git merge conflicts arise.
- **Shared Blueprint Broadcast:** Distributes plotted courses across connected crew members in under 200 milliseconds.

---

## 3. System Architecture

OpenNavy follows a Modular Hexagonal Architecture (Ports and Adapters) to guarantee loose coupling, high testability, and clear separation of concerns.

```
+-------------------------------------------------------------------------+
|                              DRIVERS / API                              |
|   FastAPI REST Routes (/api/v1/repos, /course) | WebSocket Hub (/sonar) |
+------------------------------------+------------------------------------+
                                     |
+------------------------------------v------------------------------------+
|                          APPLICATION SERVICES                           |
|       CourseOrchestrator | SonarOrchestrator | ExplorerService          |
+------------------------------------+------------------------------------+
                                     |
+------------------------------------v------------------------------------+
|                              DOMAIN CORE                                |
|        Entities: Repository, ASTNode, Waypoint, CrewPeer, Alert         |
+------------------------------------+------------------------------------+
                                     |
+------------------------------------v------------------------------------+
|                         ANALYZERS & ADAPTERS                            |
| Tree-sitter Universal AST | Tarjan SCC Solver | Ollama Gemma 4 Adapter  |
+-------------------------------------------------------------------------+
```

Detailed architectural specifications and decisions are documented in:
- [System Architecture](docs/ARCHITECTURE.md)
- [ADR-0001: Record Architecture Decisions](docs/adr/0001-record-architecture-decisions.md)
- [ADR-0002: Modular Hexagonal Architecture](docs/adr/0002-modular-hexagonal-architecture.md)
- [ADR-0003: Local-First Inference with Google Gemma 4](docs/adr/0003-local-first-inference-with-gemma4.md)
- [ADR-0004: LAN Multiplayer Mesh with FastAPI WebSockets](docs/adr/0004-lan-multiplayer-mesh-with-fastapi-websockets.md)
- [ADR-0005: GitFlow Branching Model and Conventional Commits](docs/adr/0005-gitflow-and-conventional-commits.md)

---

## 4. Technology Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn, Tree-sitter, NetworkX.
- **Local AI Engine:** Google Gemma 4 (`gemma4:e4b` primary, `gemma4:e2b` fallback) orchestrated through Ollama.
- **Frontend Cockpit:** React 18, TypeScript, Vite, Tailwind CSS, Lucide icons.
- **Networking & Real-Time:** Native WebSockets (FastAPI WebSocket Hub), optional secure LAN tunnel via Cloudflare tunnel binary.
- **Testing:** Pytest, Pytest-Asyncio.

---

## 5. Getting Started

### 5.1 Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher (with npm)
- Ollama installed and accessible via system PATH

### 5.2 Pulling the Gemma 4 Model
Open a terminal and pull the Gemma 4 model:

```bash
# Primary multimodal model (4-bit quantized, ~6.6 GB)
ollama pull gemma4:e4b

# Lightweight fallback model (optional, ~4.6 GB)
ollama pull gemma4:e2b
```

### 5.3 Backend Setup
1. Navigate to the backend directory and install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
2. Start the FastAPI backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   The interactive API documentation is available at `http://localhost:8000/docs`.

### 5.4 Frontend Setup
1. In a new terminal, navigate to the frontend directory:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
   The OpenNavy Cockpit interface will run at `http://localhost:5173`.

### 5.5 One-Click Server Launcher (Host Machine)
For hackathon demonstrations or local network hosting, execute the unified launcher script:
```powershell
.\scripts\start-server.ps1
```
This script initializes Ollama with persistent model caching and establishes the local network bridge.

---

## 6. Project Roadmap and Backlog

Sprint goals, active user stories, and task allocations are tracked in:
- [Engineering Backlog](BACKLOG.md)
- [Product Specification](docs/OPENNAVY_SPECIFICATION.md)
- [Hackathon Runbook](HACKATHON_RUNBOOK.md)

---

## 7. Engineering Team

- **Daniel Echeverría:** Lead Architect & Backend Core
- **Brandon Carranza:** Frontend Engineer & Cockpit Navigator
- **Dylan Gamero:** Real-Time & Systems Engineer

---

## 8. Contributing & GitFlow Guidelines

Contributions follow the GitFlow workflow:
1. `main` branch contains production-stable release baselines.
2. `develop` branch is the active integration branch.
3. Features are developed on dedicated branches: `feature/<area>-<description>`.
4. Commit messages must strictly follow the Conventional Commits specification:
   - `feat(...)`: New functionality
   - `fix(...)`: Defect correction
   - `docs(...)`: Documentation additions or adjustments
   - `refactor(...)`: Code refactoring without behavior modification
   - `test(...)`: Test additions or test updates
5. Documentation and commit messages must remain completely free of emojis across all contributions.

---

## 9. License

This project is licensed under the terms of the [MIT License](LICENSE).
