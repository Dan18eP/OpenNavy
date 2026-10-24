# OpenNavy: Product and Engineering Backlog
### The Sovereign Fleet Navigator for Open Source Codebases
**License:** MIT License  
**Tracks:** Best Open-Source AI Project (DigitalOcean / Hacktoberfest 2026) | Best Use of Gemma 4 (Google DeepMind)

---

## 1. Project Vision and Scope
OpenNavy is a local-first, sovereign developer cockpit and multiplayer architectural radar that turns unfamiliar open-source codebases into an interactive nautical chart. It translates GitHub issues and bug screenshots into precise implementation waypoints using Google Gemma 4, while detecting team code collisions over a local area network (LAN) mesh with zero cloud dependency.

---

## 2. Engineering Team and Roles

- **Daniel Echeverría (Lead Architect & Backend Core):**
  - Architecture governance and ADR documentation.
  - Core backend engine: Tree-sitter AST parser, Tarjan SCC dependency graph, and local Google Gemma 4 harness.
  - FastAPI WebSocket Sonar Hub and GitFlow release management.

- **Brandon Carranza (Frontend Engineer & Cockpit Navigator):**
  - Nautical Cockpit interface (React 18, Vite, Tailwind CSS, Lucide icons).
  - Interactive Waypoint Split-View (`DeepCode` AST explorer synced with Gemma 4 waypoints).
  - Cockpit ergonomics, visual design tokens, and user experience.

- **Dylan Gamero (Real-Time & Systems Engineer):**
  - Fleet Sonar radar canvas and real-time multiplayer telemetry visualization.
  - Architectural Collision Radar: proximity alerts based on Tarjan SCC coupling.
  - Shared Blueprint broadcast synchronization and dual-machine LAN validation.

---

## 3. Architecture and Technical Standards

### 3.1 Modular Hexagonal Architecture
As defined in `docs/ARCHITECTURE.md`, OpenNavy strictly enforces a Ports and Adapters pattern with zero circular dependencies between layers:
- **Domain Layer (`backend/app/domain/`):** Pure entities (Repo, AstNode, Waypoint, CrewPeer, CollisionAlert).
- **Application Services (`backend/app/services/`):** Orchestrators (`course_orchestrator`, `sonar_orchestrator`, `ast_service`).
- **Domain Analyzers (`backend/app/analyzers/`):** Universal Tree-sitter parser, Tarjan SCC graph solver.
- **Infrastructure Adapters (`backend/app/infrastructure/`):** Ollama client, file system reader, WebSocket connection manager.
- **API Drivers (`backend/app/api/v1/`):** REST routers (`/repos`, `/course`, `/explorer`) and WebSocket hub (`/sonar`).

### 3.2 Architectural Decision Records (ADRs)
- `docs/adr/0001-record-architecture-decisions.md`: Standardized MADR format for all decisions.
- `docs/adr/0002-modular-hexagonal-architecture.md`: Separation of domain, analyzers, infrastructure, and endpoints.
- `docs/adr/0003-local-first-inference-with-gemma4.md`: Sovereign inference using Ollama with `gemma4:e4b` and `gemma4:e2b`.
- `docs/adr/0004-lan-multiplayer-mesh-with-fastapi-websockets.md`: Peer coordination over LAN WebSocket without cloud dependencies.
- `docs/adr/0005-gitflow-and-conventional-commits.md`: GitFlow workflow with Conventional Commits and strict emoji-free policy.

### 3.3 GitFlow and Collaboration Rules
- **Production Branch (`main`):** Stable, deployable, verified release baseline.
- **Integration Branch (`develop`):** Active team collaboration branch. All features branch from and merge into `develop`.
- **Feature Branches (`feature/<area>-<short-description>`):** Isolated work units (e.g., `feature/course-plotter-ui`, `feature/sonar-radar-canvas`).
- **Commit Messages:** Strict Conventional Commits (`feat(...)`, `fix(...)`, `docs(...)`, `refactor(...)`, `test(...)`, `chore(...)`).
- **Strict Style Policy:** Zero emojis across all commits, documentation, code, and pull requests.

---

## 4. Sprint Roadmaps and User Stories

```
[Sprint 1: Sovereign Foundations] ---> [Sprint 2: Course Plotter] ---> [Sprint 3: Fleet Sonar LAN] ---> [Sprint 4: Freeze & Demo]
          [COMPLETED]                          [COMPLETED]                     [IN PROGRESS]                    [PLANNED]
```

### Sprint 1: Sovereign Foundations and Local AI Engine (Google Gemma 4)
*Objective: Establish clean repository foundations, integrate Tree-sitter AST and Tarjan SCC, and configure local inference with Google Gemma 4.*
*Status: COMPLETED*

- [x] **US-01: MIT License and Clean Repository Layout**
  - Owner: Daniel Echeverría
  - Description: Initialize repository with permissive MIT license and clear directory layout (`backend/`, `frontend/`, `scripts/`, `docs/`).
  - Acceptance Criteria: Root contains official `LICENSE` (MIT) and `.gitignore` preventing sensitive or heavy binary commits.

- [x] **US-02: Universal AST Parsing and Dependency Topography**
  - Owner: Daniel Echeverría
  - Description: Integrate Tree-sitter multi-language parser (Python, TypeScript, JavaScript, Go, Java) and Tarjan's Strongly Connected Components (SCC) algorithm.
  - Acceptance Criteria: Backend correctly compiles AST and identifies cyclic dependencies between modules in under 1 second.

- [x] **US-03: Sovereign Gemma 4 Engine Integration**
  - Owner: Daniel Echeverría
  - Description: Connect FastAPI backend to local Ollama inference server running `gemma4:e4b` (primary) with fallback to `gemma4:e2b`.
  - Acceptance Criteria: Local endpoint `/v1/chat/completions` responds in streaming mode with native `<|think|>` reasoning without external internet access.

- [x] **US-04: Repository Ingestion and Exploration Endpoints**
  - Owner: Daniel Echeverría
  - Description: Endpoints to ingest local/remote repositories and expose file trees with line-by-line inspection.
  - Acceptance Criteria: `/api/v1/repos` and `/api/v1/explorer/file` return structured AST nodes and code snippets.

---

### Sprint 2: The Course Plotter (Multimodal Issue-to-Waypoints)
*Objective: Transform issues, bounties, or error screenshots into actionable code waypoints with zero hallucinations.*
*Status: COMPLETED*

- [x] **US-05: Multimodal Course Plotter Endpoint (`/api/v1/course/plot`)**
  - Owner: Daniel Echeverría
  - Description: Backend endpoint accepting issue descriptions (text) or visual artifacts (bug screenshots / stack trace images).
  - Acceptance Criteria: Uses Gemma 4 Vision + Tree-sitter to return structured JSON containing:
    1. Thought Process: Gemma 4's architectural reasoning stream.
    2. Waypoints: Exact file paths and line ranges to modify.
    3. Reef Warnings: Coupled modules and cyclic risks flagged by Tarjan.
    4. Action Steps: Step-by-step implementation checklist.
    5. PR Template: Markdown draft ready for GitHub/GitLab.

- [x] **US-06: Interactive Waypoint Split-View (Cockpit UI)**
  - Owner: Brandon Carranza
  - Description: Connect frontend Course Plotter to DeepCode split-view pane.
  - Acceptance Criteria:
    1. Render input for GitHub issue URL, prompt text, and screenshot upload.
    2. Display Gemma 4 thought trace stream in collapsible panel.
    3. Clicking any generated waypoint automatically opens the source file and smoothly scrolls to the highlighted lines in the AST viewer.
    4. Render Reef Warnings as highlighted navigational beacons.

---

### Sprint 3: The Fleet Sonar (LAN Multiplayer and Collision Radar)
*Objective: Coordinate co-located developer teams on the same local network with zero external cloud infrastructure.*
*Status: COMPLETED*

- [x] **US-07: FastAPI WebSocket Sonar Hub (`/ws/sonar`)**
  - Owner: Daniel Echeverría
  - Description: Lightweight WebSocket event bus broadcasting peer presence and navigation events across the LAN.
  - Acceptance Criteria: Multiple concurrent clients connect via `ws://<HOST_IP>:8000/api/v1/sonar/ws/sonar` without user accounts.

- [x] **US-08: Architectural Collision Radar (Pre-Merge Conflict Detection)**
  - Owner: Dylan Gamero
  - Description: Cross-reference peer navigation against Tarjan's dependency matrix in real time on the frontend.
  - Acceptance Criteria:
    1. Interactive Sonar canvas showing active crew members in the codebase.
    2. If two peers inspect or modify strongly coupled modules, both receive an immediate `COLLISION_ALERT` visual banner.
    3. Display distance/proximity metrics between active files.

- [x] **US-09: Shared Blueprint Broadcast**
  - Owner: Dylan Gamero / Daniel Echeverría
  - Description: When a developer plots a course with Gemma 4, the plan is broadcast to all active crew members on the network.
  - Acceptance Criteria: All connected laptops receive the `SHARED_BLUEPRINT` event within 200ms over LAN.

---

### Sprint 4: Cockpit Polish, Verification and Live Demo Freeze
*Objective: Finalize the nautical interface, execute dual-laptop live tests, and prepare the submission package.*
*Status: PLANNED*

- [ ] **US-10: Nautical Cockpit UI Branding and Ergonomics**
  - Owner: Brandon Carranza
  - Description: Finalize OpenNavy visual styling (The Nautical Chart, Course Plotter, Fleet Sonar) using consistent nautical theme tokens.
  - Acceptance Criteria: Clean UI with Abyss Navy palette, Lucide icons, responsive layout, and zero legacy branding.

- [ ] **US-11: Feature Freeze and Double-Screen LAN Verification**
  - Owner: Daniel Echeverría, Brandon Carranza, Dylan Gamero
  - Description: Strict code freeze. Validate live demo on two laptops connected over local Wi-Fi without external internet access.
  - Acceptance Criteria: Course Plotter resolves test issue in under 10 seconds; Fleet Sonar raises collision alert on peer machine reliably.

- [ ] **US-12: Screencast Backup and MLH Submission Package**
  - Owner: Daniel Echeverría
  - Description: Record a 60-second backup demo video and assemble the MLH submission package (Devpost/GitHub README, architecture diagram).
  - Acceptance Criteria: Complete submission artifacts with working demo links and video backup.
