# Token Tracker - AI Observability Hackathon Project

## DevOps 2025 Ottawa Hackathon

Team Participant Names:
- aniqueali17
- subomiakingbade,  
- Rotimi779, 
- yelfaram

## Project Overview
Token Tracker is a full-stack AI observability application developed during a hackathon by a 4-person team. It simulates LLM-powered chat interactions while tracking key performance and safety metrics in real-time using modern observability tools.

The system monitors:
- **Token usage**
- **Request latency**
- **Toxicity scores**
- **HTTP traces and backend events**

It features a React-based chat frontend, a FastAPI backend, and a Dockerized observability stack using Prometheus, Tempo, and Grafana.

## Why This Project Was Created
This project was built to explore **AI observability concepts** and demonstrate how large language model (LLM) interactions can be monitored for performance, safety, and reliability in real-time.

My primary role focused on:
- **Backend setup and infrastructure**
- **Dockerizing the observability stack (Prometheus, Tempo, Grafana)**
- **Building API metrics and tracing endpoints**
- **Configuring OpenTelemetry integration for FastAPI**

## Project Features
- **Real-Time Monitoring**
  - Tracks token usage, response latency, and toxicity scores per chat message.
- **OpenTelemetry Tracing**
  - Visualizes detailed HTTP traces and model calls.
- **Prometheus Metrics**
  - Exposes custom application metrics (latency, token count, toxicity).
- **Grafana Dashboard**
  - Embedded into the React frontend for live visualization.
- **Dockerized Services**
  - FastAPI backend, Prometheus, Tempo, and Grafana orchestrated via Docker Compose.
- **Frontend Chat Interface**
  - React app for user interaction with the simulated LLM.

## Setup Instructions

### Prerequisites
- Docker
- Node.js (Recommended: v16 or later)

---

### Backend Setup
```bash
# From the backend folder
docker-compose up --build
```

#### Running Services
- *FastAPI API:* `http://localhost:8000/`
- *Prometheus:* `http://localhost:9090/`
- *Grafana:* `http://localhost:3000/`
- *Tempo (tracing):* `http://localhost:3200/`

To stop services:
```bash
docker-compose down --volumes
```

### Frontend Setup
```bash
# install packages
npm install
```
```bash
# run server
npm run dev
```
App will be available at `http://localhost:5173/`

### Grafana Dashboard Setup
1. Navigate to Grafana at `http://localhost:3000/`
2. Login with:
```
Username: admin
Password: admin
```
3. Push data by using the chat feature on the frontend (*/chat* endpoint must be hit first)
4. Refresh Grafana to verify that live data is displayed.
5. Copy the shareable link for your Grafana dashboard and paste into the `GrafanaEmbed.jsx` component
```jsx
<iframe src="{your_dashboard_link}" ... />
```

__NOTE__:
If the Grafana dashboard appears zoomed out or does not show recent data, use the time range selector in the top right of the embedded Grafana frame. Change the time range to “Last 15 minutes”, for example.

### Testing Workflow
1. Start backend services (`docker-compose up`) and the frontend (`npm run dev`).
2. Wait for backend confirmation: *Application startup complete.*
3. Open the React app: `http://localhost:5173/`
4. Send a message via the chat interface
5. Observe:
 - LLM response
 - Token usage
 - Latency
 - Toxicity scores
 - Traces and metrics in Grafana

#### Screenshots
![What You Should See](https://i.imgur.com/ldiXkgB.jpeg)
