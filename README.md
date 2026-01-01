# 🚚 Smart Logistics Routing Engine

> Production-ready delivery route optimization application with Dijkstra's shortest path algorithm. Zero external API dependencies.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![MIT License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![Code Quality](https://img.shields.io/badge/code-production--ready-success.svg)](#)

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running Application](#running-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Features](#features)

## Overview

Smart Logistics Routing Engine is a production-ready delivery route optimization application using Dijkstra's shortest path algorithm with zero external API dependencies.

### Key Highlights

✅ **NO API Keys Required** - Google Maps, Mapbox, or external services
✅ **100% Open Source** - MIT License
✅ **Production Ready** - Error handling, type hints, validation
✅ **Perfect for India's Small Businesses** - Delivery services, logistics, transportation
✅ **Vibrant UI** - Glasmorphism design, smooth animations
✅ **Fast & Lightweight** - In-memory graph, millisecond responses

## System Architecture

The application uses a layered architecture:

```
FRONTEND: HTML5 + CSS3 + Vanilla JavaScript
    ↕ (HTTP/REST API)
BACKEND: FastAPI + Python
    ├─ REST API Endpoints
    ├─ Pydantic Validation
    ├─ Dijkstra Algorithm
    └─ In-Memory Graph Data
```

## How It Works

Dijkstra's shortest path algorithm finds optimal routes by:
1. Initializing distances (start = 0, others = ∞)
2. Processing nodes in priority queue order
3. Updating neighbor distances when shorter paths found
4. Reconstructing path from end back to start

## Technology Stack

- **Backend**: FastAPI 0.109.0, Uvicorn 0.27.0
- **Validation**: Pydantic 2.5.3
- **Config**: python-dotenv 1.0.0
- **Algorithm**: heapq (built-in)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **License**: MIT

## Installation

### Prerequisites
- Python 3.8+
- pip
- Modern web browser
- Terminal/Command Prompt

### Setup Backend

```bash
git clone https://github.com/kritheeck/smart-logistics-routing-engine.git
cd smart-logistics-routing-engine/backend

python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Setup Frontend

```bash
cd ../frontend
# No installation needed - ready to use
```

## Running Application

### Start Backend Server

```bash
cd backend
python run.py

# Expected: INFO: Uvicorn running on http://0.0.0.0:8000
```

### Serve Frontend

```bash
cd frontend

# Option A: Python server
python -m http.server 3000

# Option B: Direct file
# Open: file:///path/to/smart-logistics-routing-engine/frontend/index.html
```

### Access Application

- Browser: http://localhost:3000
- API Docs: http://localhost:8000/api/docs

## API Documentation

### Calculate Route

**Endpoint**: `POST /api/v1/route`

**Request**:
```json
{
  "start": "Warehouse",
  "end": "CustomerE"
}
```

**Response**:
```json
{
  "path": ["Warehouse", "HubA", "CustomerE"],
  "distance": 8.5,
  "nodes_visited": 5,
  "success": true
}
```

**Available Locations**:
```
Warehouse, HubA, HubB, TransitX, TransitY, TransitZ,
CustomerA, CustomerB, CustomerC, CustomerD, CustomerE, CustomerF, DistrictP
```

### Get Graph Information

**Endpoint**: `GET /api/v1/graph`

**Response**:
```json
{
  "nodes": ["Warehouse", "HubA", "HubB", ...],
  "total_nodes": 13,
  "total_edges": 40
}
```

### Health Check

**Endpoint**: `GET /api/v1/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "Smart Logistics Routing Engine",
  "version": "1.0.0"
}
```

## Project Structure

```
smart-logistics-routing-engine/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── graph.py
│   │   ├── dijkstra.py
│   │   └── routes.py
│   ├── run.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── README.md
├── LICENSE
└── .gitignore
```

## Features

✅ Shortest path calculation with Dijkstra algorithm
✅ Real-time route optimization
✅ Distance metrics display
✅ Error handling and validation
✅ Type hints and Pydantic validation
✅ Responsive UI with glassmorphism design
✅ Loading states with animations
✅ CORS enabled for cross-origin requests
✅ Auto-generated API documentation
✅ Production-ready error handling

## Testing API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Get graph
curl http://localhost:8000/api/v1/graph

# Calculate route
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "Warehouse", "end": "CustomerE"}'
```

## License

MIT License - See LICENSE file for details

## Author

kritheeck - [GitHub](https://github.com/kritheeck)

---

**Made with ❤️ for India's Logistics Industry**
