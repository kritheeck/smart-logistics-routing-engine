# Deployment Guide

## Deploy to Production (Docker, Heroku, AWS, DigitalOcean)

This guide covers deploying your Smart Logistics Routing Engine to production.

## Deployment Options

1. **Docker (Local Container)** - Containerized locally
2. **Heroku** - Free tier available, easy setup
3. **AWS** - EC2, Elastic Beanstalk
4. **DigitalOcean** - Simple droplets and app platform
5. **Railway** - Modern, fast deployment

## Option 1: Docker Deployment

### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY backend/run.py .
COPY frontend ./frontend
COPY backend/.env .

EXPOSE 8000

CMD ["python", "run.py"]
```

### Create docker-compose.yml

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - RELOAD=False
    volumes:
      - ./backend:/app/app
```

### Build & Run Docker

```bash
# Build image
docker build -t logistics-engine .

# Run container
docker run -p 8000:8000 logistics-engine

# With docker-compose
docker-compose up

# Access
# API: http://localhost:8000
# Docs: http://localhost:8000/api/docs
```

## Option 2: Heroku Deployment

### Prerequisites

```bash
# Install Heroku CLI
# Download from https://devcenter.heroku.com/articles/heroku-cli

heroku login
heroku create logistics-routing-engine
```

### Create Procfile

Create `Procfile` in project root:

```
web: cd backend && python run.py
```

### Create runtime.txt

Create `runtime.txt`:

```
python-3.9.16
```

### Deploy

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit"

# Add Heroku remote
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Access Deployed App

```
https://your-app-name.herokuapp.com/api/docs
```

## Option 3: AWS EC2 Deployment

### Launch EC2 Instance

1. Go to AWS Console
2. Launch Ubuntu 20.04 LTS instance (t2.micro)
3. Configure security group (ports 22, 80, 8000)
4. Create key pair

### Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

### Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/kritheeck/smart-logistics-routing-engine.git
cd smart-logistics-routing-engine

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Install Gunicorn

```bash
pip install gunicorn
```

### Run with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### Setup Systemd Service

Create `/etc/systemd/system/logistics.service`:

```ini
[Unit]
Description=Smart Logistics Routing Engine
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/smart-logistics-routing-engine/backend
Environment="PATH=/home/ubuntu/smart-logistics-routing-engine/backend/venv/bin"
ExecStart=/home/ubuntu/smart-logistics-routing-engine/backend/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl start logistics
sudo systemctl enable logistics
sudo systemctl status logistics
```

### Setup Nginx Reverse Proxy

```bash
sudo apt install nginx -y
```

Create `/etc/nginx/sites-available/default`:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Enable & Restart Nginx

```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## Option 4: DigitalOcean App Platform

### Connect GitHub Repository

1. Go to DigitalOcean Apps
2. Click "Create App"
3. Connect GitHub
4. Select smart-logistics-routing-engine

### Configure app.yaml

Create `app.yaml` in project root:

```yaml
name: smart-logistics-routing-engine
services:
- name: backend
  github:
    repo: kritheeck/smart-logistics-routing-engine
    branch: main
  build_command: cd backend && pip install -r requirements.txt
  run_command: cd backend && python run.py
  envs:
  - key: PORT
    value: "8080"
  - key: HOST
    value: "0.0.0.0"
  http_port: 8080
  health_check:
    http_path: /api/v1/health
```

### Deploy

1. Upload app.yaml to repository
2. Click "Deploy"
3. Wait for build & deployment

## Option 5: Railway.app Deployment

### Quick Deploy

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy
railway up

# View logs
railway logs
```

## Post-Deployment Checklist

- [ ] API responds at `/api/v1/health`
- [ ] Graph endpoint works
- [ ] Routes calculate correctly
- [ ] No CORS errors
- [ ] Environment variables set
- [ ] Database/file permissions correct
- [ ] Logs are being generated
- [ ] SSL/HTTPS configured
- [ ] Domain mapped
- [ ] Monitoring setup

## Performance Optimization

### Enable Compression

```python
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

### Add Caching Headers

```python
from fastapi.responses import JSONResponse

@app.get("/api/v1/graph")
async def get_graph():
    return JSONResponse(
        content=graph_data,
        headers={"Cache-Control": "public, max-age=3600"}
    )
```

### Database Connection Pooling

If using database:

```python
from sqlalchemy.pool import NullPool

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool  # For serverless
)
```

## Monitoring & Logging

### Sentry Integration

```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=0.1
)
```

### CloudWatch (AWS)

```bash
pip install watchtower
```

```python
import logging
import watchtower

logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

## SSL/HTTPS Setup

### Let's Encrypt (Free)

```bash
# On Heroku - automatic
# On AWS EC2:
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

### Auto Renewal

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Cost Comparison

| Platform | Tier | Cost | Notes |
|----------|------|------|-------|
| **Heroku** | Free | $0/mo | Limited; great for testing |
| **Heroku** | Hobby | $7/mo | Single dyno |
| **DigitalOcean** | Starter | $5/mo | 512MB RAM |
| **AWS EC2** | t2.micro | $0-5/mo | Free tier first year |
| **Railway** | Starter | $5/mo | 512MB RAM |

## Scaling Considerations

### Horizontal Scaling

```bash
# Multiple instances behind load balancer
# Use auto-scaling group
# Each instance runs independently
```

### Vertical Scaling

```bash
# Increase server resources
# Upgrade to larger instance type
# Add more CPU/RAM
```

### Database Optimization

```bash
# Cache frequent queries
# Index search columns
# Use read replicas for high load
```

## Troubleshooting Deployment

### Port Already in Use

```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Module Import Errors

```bash
# Check venv activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### Environment Variables Not Set

```bash
# Check variables
env | grep APP

# Set in deployment platform UI
# Or in .env file (not recommended for production)
```

## Final Steps

1. **Document API**: Use generated Swagger at `/api/docs`
2. **Monitor**: Set up uptime monitoring (Pingdom, UptimeRobot)
3. **Backup**: Configure automated backups
4. **Update**: Set up CI/CD pipeline
5. **Security**: Run security scans

---

**Your Smart Logistics Engine is ready for production!** 🚀
