# Deployment Files

This directory contains everything needed to deploy the Innovative Game Collection to the cloud.

## Quick Start (3 options)

### 1️⃣ Automated Script (Easiest)

```bash
./quickstart.sh
```

Follow the prompts to choose your deployment method.

### 2️⃣ One-Line Deploy to Railway

```bash
cd web-terminal && npx @railway/cli login && npx @railway/cli up
```

### 3️⃣ Docker (Local)

```bash
docker-compose up
# Visit http://localhost:5000
```

## Directory Structure

```
deploy/
├── quickstart.sh           # Automated deployment script
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Container image definition
├── railway.json            # Railway.app configuration
├── DEPLOYMENT.md           # Comprehensive deployment guide
└── web-terminal/           # Web-based terminal application
    ├── app.py              # Flask application
    ├── requirements.txt    # Python dependencies
    └── templates/          # HTML templates
        ├── index.html      # Game selection page
        └── terminal.html   # Terminal interface
```

## Deployment Options

### Cloud Platforms (Recommended)

| Platform | Difficulty | Free Tier | Deploy Time |
|----------|-----------|-----------|-------------|
| **Railway.app** ⭐ | Easy | $5/month credit | 2 minutes |
| **Render.com** | Easy | 750 hrs/month | 5 minutes |
| **Heroku** | Easy | 550 hrs/month | 5 minutes |
| **Google Cloud Run** | Medium | 2M requests | 10 minutes |

### Self-Hosted

| Platform | Cost | Setup Time |
|----------|------|------------|
| **DigitalOcean** | $5/month | 15 minutes |
| **AWS EC2** | ~$5/month | 20 minutes |
| **Linode** | $5/month | 15 minutes |

## Features

### Web Terminal
- ✅ Play all games in browser
- ✅ No installation required
- ✅ Beautiful UI with xterm.js
- ✅ Works on mobile devices
- ✅ WebSocket-based real-time terminal

### Docker
- ✅ Consistent environment
- ✅ Easy scaling
- ✅ Simple deployment
- ✅ Portable across platforms

## Tech Stack

- **Backend:** Python + Flask + Flask-SocketIO
- **Frontend:** HTML5 + JavaScript + xterm.js
- **WebSockets:** Socket.IO
- **Container:** Docker + Docker Compose

## Environment Variables

```bash
# Required
SECRET_KEY=your-random-secret-key-here

# Optional
PORT=5000                    # Server port
FLASK_ENV=production        # Environment mode
MAX_TERMINALS=100           # Max concurrent sessions
```

## Security

The deployment includes:
- Session management
- Input sanitization
- HTTPS support (on cloud platforms)
- Rate limiting (configurable)
- Terminal isolation

## Monitoring

### Logs

**Local/Docker:**
```bash
docker logs -f innovative-games
```

**Railway:**
```bash
railway logs
```

### Metrics

All platforms provide:
- Request count
- Response time
- Error rates
- Resource usage

## Troubleshooting

**Port already in use:**
```bash
# Change port in docker-compose.yml or:
docker run -p 8080:5000 innovative-games
```

**Permission denied:**
```bash
chmod +x quickstart.sh
```

**WebSocket connection failed:**
- Check firewall settings
- Ensure WebSocket support on proxy
- Verify CORS settings

## Support

See [DEPLOYMENT.md](../DEPLOYMENT.md) for comprehensive documentation.

## Quick Commands

```bash
# Deploy to Railway
./quickstart.sh

# Run locally with Docker
docker-compose up

# Run locally without Docker
cd web-terminal && pip install -r requirements.txt && python app.py

# Stop Docker
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose up --build
```

---

**Ready to deploy? Run `./quickstart.sh` and choose your platform!** 🚀
