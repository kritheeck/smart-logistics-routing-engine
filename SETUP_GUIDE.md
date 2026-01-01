# Clone & Setup Guide

## Complete Installation Instructions

This guide will walk you through cloning, setting up, and running the Smart Logistics Routing Engine on your local machine.

## Prerequisites

- **Git** - Version control
- **Python 3.8+** - Latest stable version
- **pip** - Python package manager (comes with Python)
- **Modern Web Browser** - Chrome, Firefox, Safari, or Edge
- **Terminal/Command Prompt** - For running commands

### Check Prerequisites

```bash
# Check Python version
python --version
# Expected: Python 3.8.0 or higher

# Check pip version
pip --version
# Expected: pip X.X.X

# Check Git
git --version
# Expected: git version X.XX.X
```

## Step 1: Clone the Repository

### Using HTTPS (Recommended for beginners)

```bash
# Navigate to where you want the project
cd Desktop
# or
cd Documents

# Clone the repository
git clone https://github.com/kritheeck/smart-logistics-routing-engine.git

# Enter the project directory
cd smart-logistics-routing-engine

# List contents
ls -la
```

### Using SSH (For GitHub configured users)

```bash
git clone git@github.com:kritheeck/smart-logistics-routing-engine.git
cd smart-logistics-routing-engine
```

### Verify Cloned Files

You should see:
```
backend/              # Backend FastAPI code
frontend/             # Frontend HTML/CSS/JS
README.md            # Main documentation
LICENSE              # MIT License
.gitignore           # Git ignore rules
```

## Step 2: Setup Backend (FastAPI Server)

### 2.1 Navigate to Backend Directory

```bash
cd backend
ls -la
```

You should see:
```
app/                 # Application code
run.py              # Entry point
requirements.txt    # Dependencies
.env                # Environment config
```

### 2.2 Create Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 2.3 Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

You should see:
```
fastapi                       0.109.0
uvicorn                       0.27.0
pydantic                      2.5.3
python-dotenv                 1.0.0
```

### 2.4 Verify Environment Configuration

```bash
# View .env file
cat .env
# On Windows:
type .env
```

Expected output:
```
APP_NAME=Smart Logistics Routing Engine
APP_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
RELOAD=True
DEBUG=True
```

### 2.5 Start Backend Server

```bash
python run.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **Backend is running!** Don't close this terminal.

## Step 3: Setup Frontend (Web Interface)

### 3.1 Open New Terminal/Command Prompt

Keep the backend terminal open, open a **new terminal window**.

### 3.2 Navigate to Frontend

```bash
# From project root
cd frontend
ls -la
```

You should see:
```
index.html          # Main HTML file
style.css           # Styling
app.js              # JavaScript logic
```

### 3.3 Start Frontend Server

#### Option A: Python Built-in Server (Recommended)

```bash
python -m http.server 3000
```

Expected output:
```
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```

#### Option B: Node.js http-server (If installed)

```bash
npx http-server -p 3000
```

#### Option C: Direct File (No server needed)

Simply open `frontend/index.html` in your browser:
```
file:///path/to/smart-logistics-routing-engine/frontend/index.html
```

✅ **Frontend server is running!**

## Step 4: Access the Application

### Open Your Browser

1. If using Python server: **http://localhost:3000**
2. If using direct file: **file:///path/to/frontend/index.html**
3. API Docs: **http://localhost:8000/api/docs**

### You Should See

- Header with "Smart Logistics Routing"
- Two dropdown menus (Start Location, End Location)
- Calculate Route button
- Results section

## Step 5: Verify Everything Works

### Test 1: Try a Route in the UI

1. Open the web interface
2. Select **Start Location**: Warehouse
3. Select **End Location**: CustomerE
4. Click **Calculate Route**
5. You should see the route path and distance

### Test 2: Check API Health

Open a **third terminal** and run:

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Smart Logistics Routing Engine",
  "version": "1.0.0"
}
```

### Test 3: Calculate Route via API

```bash
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "Warehouse", "end": "CustomerE"}'
```

Expected response:
```json
{
  "path": ["Warehouse", "HubA", "CustomerE"],
  "distance": 8.5,
  "nodes_visited": 5,
  "success": true
}
```

## Troubleshooting

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Change port number
python -m http.server 8080  # Use port 8080 instead
```

### Module Not Found Error

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall requirements
pip install -r requirements.txt
```

### Python Version Issue

**Error**: `Python 3.8+ required`

**Solution**:
```bash
# Check your Python version
python --version

# If outdated, download from python.org
# Then update PATH or use python3
python3 --version
python3 -m venv venv
```

### CORS Errors in Browser

**Solution**: Backend CORS is enabled by default. Ensure:
1. Backend running on `http://localhost:8000`
2. Frontend running on `http://localhost:3000`
3. Both on same machine or CORS configured

### Nothing Works

Try starting fresh:
```bash
# Kill all servers (Ctrl+C)
# Close all terminals
# Re-open fresh terminal

# Backend:
cd backend
source venv/bin/activate  # or venv\Scripts\activate
python run.py

# Frontend (new terminal):
cd frontend
python -m http.server 3000
```

## Project Directory Structure

```
smart-logistics-routing-engine/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── graph.py
│   │   │   └── service.py
│   │   └── __pycache__/
│   ├── run.py
│   ├── requirements.txt
│   ├── .env
│   └── venv/  (created after setup)
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── README.md
├── SETUP_GUIDE.md (this file)
├── LICENSE
├── .gitignore
└── .git/
```

## Next Steps

1. **Testing** - See TESTING_GUIDE.md
2. **Customization** - See CUSTOMIZATION_GUIDE.md
3. **Deployment** - See DEPLOYMENT_GUIDE.md
4. **Contributing** - Submit PRs on GitHub

## Common Commands Reference

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Deactivate virtual environment
deactivate

# Install new package
pip install package_name

# Upgrade pip
pip install --upgrade pip

# Freeze current dependencies
pip freeze > requirements.txt

# Start backend
python run.py

# Start frontend
python -m http.server 3000

# Kill a process on Windows
taskkill /F /PID <process_id>

# Kill a process on Mac/Linux
kill -9 <process_id>
```

## Support & Help

- **GitHub Issues**: https://github.com/kritheeck/smart-logistics-routing-engine/issues
- **API Docs**: http://localhost:8000/api/docs (when running)
- **README**: See main README.md

---

**Congratulations! You've successfully set up Smart Logistics Routing Engine!** 🌟
