# 🚀 DevOps Capstone Project: Enhanced Implementation Plan & System Design

## 📘 Project Overview

This project simulates a real-world production-grade DevOps workflow and will provide hands-on experience with containerization, infrastructure automation, monitoring, CI/CD pipelines, REST APIs, database logging, and web-based user interfaces.

### 🎯 Objective:

Build, deploy, monitor, and manage a containerized microservice architecture with the following components:

- REST-based file exchange between server and client
- Web UI for interaction
- Database integration (MongoDB)
- Logging and monitoring via Grafana
- CI/CD pipeline with GitHub Actions
- Full AWS deployment via Terraform

---

## 🧱 System Design & Architecture

### 🗂️ Repositories

- `server-app` GitHub repository
- `client-app` GitHub repository
  Each repository will contain:
- Dockerfile
- Application code
- Terraform scripts (in `/terraform` directory)
- CI/CD GitHub Actions workflows
- README.md with detailed instructions

### 🧩 Components

| Component      | Description                                                     |
| -------------- | --------------------------------------------------------------- |
| Server App     | Exposes REST API to generate file, checksum, and send to client |
| Client App     | Web UI + API to request and verify file, log result in DB       |
| MongoDB        | Stores file verification history on client side                 |
| Docker         | Containerize all apps and services                              |
| Docker Compose | Used to orchestrate multi-container setups locally              |
| Terraform      | Provision AWS infrastructure: EC2s, networking, firewall        |
| AWS EC2        | One instance for client stack, one for server stack             |
| Grafana        | System + container metrics dashboards (on port 3020)            |
| GitHub Actions | CI/CD workflows to build, push, and deploy images               |
| Docker Hub     | Public image registry for server and client images              |
| Slack          | Notification for successful CI/CD events                        |

### 🌐 Network & Infra Design

- VPC with 2 public subnets (client + server EC2s)
- t2.micro EC2 instances (free tier)
- Security groups:

  - Open port 3020 (Grafana)
  - Custom ports for API communication (e.g., 5000, 5001)
  - SSH, HTTP/HTTPS as needed

### 🛠 Tools & Services

| Purpose          | Tool/Service                        |
| ---------------- | ----------------------------------- |
| Frontend + API   | Flask + Bootstrap (Jinja templates) |
| Database         | MongoDB (NoSQL for metadata)        |
| Containerization | Docker, Docker Compose              |
| Version Control  | Git, GitHub                         |
| IaC              | Terraform                           |
| Cloud Hosting    | AWS EC2 (Ubuntu)                    |
| Monitoring       | Grafana + Node Exporter             |
| CI/CD            | GitHub Actions                      |
| Notifications    | Slack                               |

---

## 📋 Step-by-Step Implementation Plan

### ✅ Phase 1: Application Development & Local Docker Deployment (Completed)

### 🎯 Objectives:

- Develop a RESTful server that generates a file and returns its checksum
- Create a web-based client to trigger the fetch, receive the file, verify checksum, and log results in MongoDB
- Set up local MongoDB using Docker
- Integrate all services using a **single unified `docker-compose.yml`** for seamless orchestration

---

### 🧱 What We Implemented

#### 🔹 Server (Flask App)

- Endpoint `/generate` creates a 1KB file with random text in `/serverdata`
- Calculates SHA256 checksum
- `/file` endpoint sends the generated file to the client
- Uses environment variables from `.env`
- Built with `python:3.10-slim`

#### 🔹 Client (Flask Web UI)

- Homepage (`/`) contains a button to fetch file from server
- `/fetch` endpoint:

  - Calls server's `/generate` and `/file`
  - Saves file to `/clientdata`
  - Computes checksum
  - Logs metadata into MongoDB: `timestamp`, `filename`, `checksum`, `verified`, `status`, `client_ip`

- Uses environment variables from `.env`
- MongoDB is connected via `pymongo`

#### 🔹 MongoDB

- Runs locally as a container with persistent named volume
- No schema creation needed (auto-created via insert)
- DB name: `filelogs`
- Collection: `logs`

#### 🔹 Unified `docker-compose.yml`

- Placed in root directory
- Builds all services (`client`, `server`, `mongo`)
- Shares network, volumes, and env files

---

### 🐞 Problems Faced & Resolutions

| Problem                                                   | Root Cause                                    | Fix                                                                        |
| --------------------------------------------------------- | --------------------------------------------- | -------------------------------------------------------------------------- |
| `pull access denied for server-app`                       | Docker tried to pull instead of build locally | Used `build:` with `context: ./serverSideApp` instead of `image:`          |
| `Bind for 0.0.0.0:5001 failed: port is already allocated` | Port conflict from already running container  | Stopped old container and used `docker-compose down` before restarting     |
| MongoDB not logging correctly                             | Missing `client_ip` and `filename` fields     | Updated `client.py` to include `flask_request.remote_addr` and `filename`  |
| Confusion between multiple `docker-compose.yml` files     | Split Compose definitions in two directories  | Consolidated into **one root-level unified Compose file** for all services |

---

### 🔁 Reproducible Steps for Local Deployment

You can reproduce this working setup by following these steps:

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-org>/devops-capstone
   cd devops-capstone
   ```

2. **Ensure Folder Structure Looks Like:**

   ```
   devops-capstone/
   ├── docker-compose.yml
   ├── clientSideApp/
   │   ├── app/
   │   ├── Dockerfile
   │   ├── .env
   └── serverSideApp/
       ├── app/
       ├── Dockerfile
       ├── .env
   ```

3. **Review Environment Variables**

   `clientSideApp/.env`:

   ```env
   FLASK_ENV=production
   PORT=5000
   DATA_DIR=/clientdata
   SERVER_HOST=http://server:5001
   MONGO_URI=mongodb://mongo:27017/
   ```

   `serverSideApp/.env`:

   ```env
   FLASK_ENV=production
   PORT=5001
   DATA_DIR=/serverdata
   ```

4. **Build & Run All Services**

   ```bash
   docker-compose up --build -d
   ```

5. **Access the App**

   | Service    | URL                                                              |
   | ---------- | ---------------------------------------------------------------- |
   | Client UI  | [http://localhost:5000](http://localhost:5000)                   |
   | Server API | [http://localhost:5001/generate](http://localhost:5001/generate) |
   | MongoDB    | mongodb://localhost:27017                                        |

6. **Verify MongoDB Logs**

   ```bash
   docker exec -it <mongo-container-id> mongosh
   > use filelogs
   > db.logs.find().pretty()
   ```

7. **Stop Services**

   ```bash
   docker-compose down
   ```

---

## ✅ Phase 2: Infrastructure Provisioning with Terraform Infrastructure Provisioning with Terraform

- [ ] Define modules and scripts in `/terraform` for:

  - VPC + subnets
  - EC2 instances (client + server)
  - Security groups

- [ ] Verify SSH + port access

### ✅ Phase 3: Monitoring Stack

- [ ] Install Grafana + Node Exporter on both EC2s
- [ ] Expose Grafana at port 3020 publicly
- [ ] Dashboards:

  - System Metrics: CPU, memory, disk, processes
  - Docker Metrics (via cAdvisor or node_exporter + Prometheus)

### ✅ Phase 4: CI/CD Pipelines

- [ ] GitHub Actions Workflows:

  - On push to main:

    - Build Docker image
    - Push to Docker Hub
    - SSH into EC2 and pull + restart Docker Compose
    - Send Slack notification

- [ ] Store secrets in GitHub Actions secrets vault
- [ ] Configure EC2 as GitHub self-hosted runner (optional)

### ✅ Phase 5: Documentation

- [ ] Detailed README.md for both repos

  - How to run locally
  - How to deploy on AWS
  - How CI/CD is setup
  - Troubleshooting and port reference

- [ ] Architecture diagrams (draw\.io or Lucidchart)
- [ ] Output Grafana dashboard screenshots

---

## ⏳ Timeline

| Week   | Task                                              |
| ------ | ------------------------------------------------- |
| Week 1 | App logic (client + server) + MongoDB integration |
| Week 2 | Dockerize + Compose files + Local testing         |
| Week 3 | Terraform + AWS provisioning                      |
| Week 4 | Grafana + CI/CD pipelines setup                   |
| Week 5 | Final documentation, testing, submission          |

📌 **Final Submission Date: 09 August 2025 – 11:59PM**

---

Next Step ➡️ Start building the **server REST API container** with `/generate` endpoint and Dockerfile.
