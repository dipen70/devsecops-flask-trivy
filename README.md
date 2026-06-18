# devsecops-flask-trivy

A hands-on **DevSecOps** demo project that shows how to find and understand security
vulnerabilities in a containerized application using **[Trivy](https://github.com/aquasecurity/trivy)**,
an open-source security scanner from Aqua Security.

The project deliberately ships a small **Flask** web app with *known* vulnerable
dependencies and an insecure container image. The goal is not to build a perfect app —
it is to experience the "Sec" in DevSecOps: scanning, reading a vulnerability report,
and learning how to remediate the issues that a scanner surfaces.

---

## Team Members

| Name |
| --- |
| Dipen Bhattarai |
| Digdarshan Bohara |
| Sachin Acharya |
| Saugat Maharjan |
| Nimran Koirala |
| Sujal Budha Chettri |

---

## What This Project Is About

**DevSecOps** is the practice of integrating security checks *throughout* the software
development lifecycle instead of treating security as a final gate. A key part of that is
**"shifting security left"** — catching problems early, as code is written and built,
rather than after deployment.

This repository is a minimal, intentionally-insecure sandbox to practice exactly that:

- A tiny **Flask API** (`app.py`) with two endpoints.
- A **Dockerfile** that builds the app into a container image.
- A **requirements.txt** pinned to **outdated, vulnerable** package versions.
- **Trivy** used as the scanner to detect:
  - Vulnerable Python dependencies (Software Composition Analysis / SCA).
  - Vulnerabilities in the base OS image and system packages.
  - Misconfigurations in the Dockerfile.

It is built so the scanner will find real CVEs, giving us something concrete to read,
interpret, and fix.

### The Application

A minimal Flask service with two routes:

| Route | Method | Description |
| --- | --- | --- |
| `/` | GET | Returns a simple JSON greeting. |
| `/fetch?url=<url>` | GET | Fetches the given URL server-side and returns its HTTP status code. |

> ⚠️ **Note:** The app is intentionally insecure. `debug=True` is enabled and the
> `/fetch` endpoint takes a user-supplied URL (a classic **SSRF** — Server-Side Request
> Forgery — pattern). These are kept on purpose as talking points, not as good practice.

---

## The Setup

### Project Structure

```
devsecops-flask-trivy/
├── app.py             # Flask application (2 endpoints)
├── requirements.txt   # Intentionally vulnerable dependencies
├── Dockerfile         # Container build definition
├── .gitignore
└── README.md
```

### Dependencies (intentionally outdated)

```
flask==2.1.0
requests==2.27.1
Werkzeug==2.1.1
```

These specific older versions carry publicly known CVEs, which is what makes them useful
for a scanning demo.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Trivy](https://aquasecurity.github.io/trivy/latest/getting-started/installation/)
- (Optional) Python 3.9+ to run the app locally without Docker

### 1. Clone the repository

```bash
git clone <repo-url>
cd devsecops-flask-trivy
```

### 2. Run the app locally (optional)

```bash
pip install -r requirements.txt
python app.py
# App available at http://localhost:5000
```

Test it:

```bash
curl http://localhost:5000/
# {"message": "Hello from DevSecOps Flask App!"}
```

### 3. Build the Docker image

```bash
docker build -t devsecops-flask-trivy .
```

### 4. Run the container

```bash
docker run -p 5000:5000 devsecops-flask-trivy
```

---

## Scanning with Trivy

Trivy is the heart of this project. A few of the most useful scans:

**Scan the dependency file (filesystem / SCA scan):**

```bash
trivy fs .
```

**Scan the built Docker image (OS packages + app dependencies):**

```bash
trivy image devsecops-flask-trivy
```

**Scan the Dockerfile for misconfigurations:**

```bash
trivy config .
```

**Show only HIGH and CRITICAL severity issues:**

```bash
trivy image --severity HIGH,CRITICAL devsecops-flask-trivy
```

Each scan produces a report listing the CVE ID, the affected package, the installed
version, the fixed version, and a severity rating — the exact information needed to plan
a fix.

---

## Key Takeaways

- **Shift security left.** Scanning at build time (or even in the editor) catches
  vulnerabilities long before they reach production, where they are far costlier to fix.
- **Dependencies are a major attack surface.** Most real-world vulnerabilities come from
  third-party packages, not from our own code. Pinning *and updating* versions matters.
- **Container images carry their own risks.** The base image (`python:3.9` here) ships an
  entire OS with its own packages and CVEs. Choosing smaller, current base images (e.g.
  `python:3.x-slim` or distroless) shrinks the attack surface.
- **Reading a scan report is a skill.** Severity, exploitability, and whether a fix is
  available all factor into deciding *what to fix first* — you can't (and shouldn't) chase
  every finding blindly.
- **Automation makes it sustainable.** Trivy can be wired into CI/CD pipelines so every
  commit and image is scanned automatically, making security a continuous habit rather
  than a one-off audit.

---

## Challenges

- **Producing meaningful findings on purpose.** We had to deliberately pick package
  versions old enough to carry known CVEs while still letting the app run, so the scanner
  had real issues to report.
- **Interpreting the volume of results.** A single image scan can return dozens of CVEs.
  Learning to filter by severity (`--severity HIGH,CRITICAL`) and focus on what's
  actually exploitable was a learning curve.
- **Distinguishing app vs. base-image issues.** Many vulnerabilities came from the OS
  layer of the base image rather than our code, which taught us that remediation isn't
  always "update my requirements.txt."
- **Balancing fixing vs. demonstrating.** Because the point of the repo is to *show*
  vulnerabilities, we intentionally left insecure patterns (debug mode, SSRF-prone
  endpoint, old dependencies) in place rather than fixing them away.
- **Environment/tooling setup.** Getting Docker and Trivy installed and working
  consistently across team members' machines took some coordination.

---

## Possible Next Steps / Remediation

If this were a real application, the fixes would include:

- Upgrade `flask`, `requests`, and `Werkzeug` to current, patched versions.
- Switch to a smaller, regularly-updated base image (e.g. `python:3.x-slim`).
- Disable `debug=True` in production.
- Validate and restrict the URL in the `/fetch` endpoint to prevent SSRF.
- Add a Trivy scan step to a CI/CD pipeline that fails the build on HIGH/CRITICAL findings.
