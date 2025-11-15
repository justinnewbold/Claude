# GOOGLE CLOUD RUN - STEP-BY-STEP DEPLOYMENT GUIDE

Complete guide to deploy the Innovative Game Collection to Google Cloud Run.

---

## Prerequisites

### 1. Google Cloud Account

**Sign up for Google Cloud:**
- Go to https://cloud.google.com
- Click "Get started for free"
- **Free tier includes:**
  - $300 credit for 90 days
  - 2 million requests/month forever (after trial)
  - No credit card required for trial

### 2. Install Google Cloud CLI

**On macOS:**
```bash
# Using Homebrew
brew install --cask google-cloud-sdk
```

**On Linux:**
```bash
# Download and install
curl https://sdk.cloud.google.com | bash

# Restart shell
exec -l $SHELL

# Initialize
gcloud init
```

**On Windows:**
- Download installer: https://cloud.google.com/sdk/docs/install
- Run `GoogleCloudSDKInstaller.exe`
- Follow installation wizard

### 3. Install Docker

**Verify Docker is installed:**
```bash
docker --version
# Should show: Docker version 20.x.x or higher
```

**If not installed:**
- macOS: https://docs.docker.com/desktop/mac/install/
- Linux: `sudo apt-get install docker.io`
- Windows: https://docs.docker.com/desktop/windows/install/

---

## Step 1: Set Up Google Cloud Project

### Create a New Project

```bash
# Login to Google Cloud
gcloud auth login
# Opens browser for authentication

# Create new project (choose unique PROJECT_ID)
gcloud projects create innovative-games-YOURNAME --name="Innovative Games"

# Set as active project
gcloud config set project innovative-games-YOURNAME

# Verify
gcloud config get-value project
```

**Replace `YOURNAME` with something unique** (e.g., `innovative-games-john123`)

### Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build API (optional, for faster builds)
gcloud services enable cloudbuild.googleapis.com
```

**This takes 1-2 minutes.**

---

## Step 2: Prepare Your Code

### Navigate to Project

```bash
cd /home/user/Claude
```

### Fix Docker Configuration

Update the Dockerfile to work with Cloud Run:

```bash
cat > deploy/Dockerfile.cloudrun <<'EOF'
# Use Python 3.11 slim for smaller image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy game files
COPY *.py ./games/
COPY *.md ./games/

# Copy web terminal app
COPY deploy/web-terminal/requirements.txt ./
COPY deploy/web-terminal/app.py ./
COPY deploy/web-terminal/templates ./templates/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run expects port from environment variable
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Run the application
CMD exec python app.py
EOF
```

### Update Flask App for Cloud Run

Cloud Run needs the app to listen on the PORT environment variable:

```bash
cat > deploy/web-terminal/app_cloudrun.py <<'EOF'
#!/usr/bin/env python3
"""
Web-based terminal for Innovative Game Collection - Cloud Run version
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import pty
import os
import subprocess
import select
import termios
import struct
import fcntl

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
socketio = SocketIO(app, cors_allowed_origins="*")

class Terminal:
    """Manages a pseudo-terminal for running games"""

    def __init__(self):
        self.fd = None
        self.child_pid = None

    def spawn(self, game_file):
        """Spawn a game in a pseudo-terminal"""
        (child_pid, fd) = pty.fork()

        if child_pid == 0:
            # Child process - run the game
            game_path = f'/app/games/{game_file}'
            os.execvp('python3', ['python3', game_path])
        else:
            # Parent process - store the terminal
            self.child_pid = child_pid
            self.fd = fd
            self.set_terminal_size(80, 24)
            return fd

    def set_terminal_size(self, cols, rows):
        """Set the terminal size"""
        if self.fd:
            winsize = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def read(self):
        """Read output from terminal"""
        if self.fd:
            try:
                return os.read(self.fd, 10240).decode('utf-8', errors='replace')
            except:
                return None
        return None

    def write(self, data):
        """Write input to terminal"""
        if self.fd:
            os.write(self.fd, data.encode())


# Store active terminals
terminals = {}

@app.route('/')
def index():
    """Show game selection page"""
    games = [
        {'id': 'echo_chambers', 'name': 'Echo Chambers', 'file': 'echo_chambers.py', 'icon': '🌌'},
        {'id': 'code_archaeology', 'name': 'Code Archaeology', 'file': 'code_archaeology.py', 'icon': '💾'},
        {'id': 'infinite_library', 'name': 'The Infinite Library', 'file': 'infinite_library.py', 'icon': '📚'},
        {'id': 'forking_paths', 'name': 'The Garden of Forking Paths', 'file': 'forking_paths.py', 'icon': '🌳'},
        {'id': 'last_recursion', 'name': 'The Last Recursion', 'file': 'last_recursion.py', 'icon': '🔄'},
        {'id': 'schrodingers_dungeon', 'name': 'Schrödinger\'s Dungeon', 'file': 'schrodingers_dungeon.py', 'icon': '🐱'},
        {'id': 'emergence_engine', 'name': 'The Emergence Engine', 'file': 'emergence_engine.py', 'icon': '🧬'},
        {'id': 'ship_of_theseus', 'name': 'The Ship of Theseus', 'file': 'ship_of_theseus.py', 'icon': '🚢'},
        {'id': 'butterfly_effect', 'name': 'The Butterfly Effect', 'file': 'butterfly_effect.py', 'icon': '🦋'},
        {'id': 'syntax_tree_climber', 'name': 'Syntax Tree Climber', 'file': 'syntax_tree_climber.py', 'icon': '🌳'},
        {'id': 'entanglement', 'name': 'Entanglement', 'file': 'entanglement.py', 'icon': '🔗'},
    ]
    return render_template('index.html', games=games)

@app.route('/play/<game_file>')
def play(game_file):
    """Show terminal page for a specific game"""
    return render_template('terminal.html', game_file=game_file)

@app.route('/health')
def health():
    """Health check endpoint for Cloud Run"""
    return {'status': 'healthy'}, 200

@socketio.on('start')
def handle_start(data):
    """Start a game session"""
    game_file = data['game_file']
    session_id = request.sid

    terminal = Terminal()
    fd = terminal.spawn(game_file)
    terminals[session_id] = terminal

    # Start reading output
    socketio.start_background_task(read_output, session_id)

@socketio.on('input')
def handle_input(data):
    """Handle input from web terminal"""
    session_id = request.sid
    if session_id in terminals:
        terminals[session_id].write(data['input'])

@socketio.on('resize')
def handle_resize(data):
    """Handle terminal resize"""
    session_id = request.sid
    if session_id in terminals:
        terminals[session_id].set_terminal_size(data['cols'], data['rows'])

@socketio.on('disconnect')
def handle_disconnect():
    """Clean up terminal on disconnect"""
    session_id = request.sid
    if session_id in terminals:
        terminal = terminals[session_id]
        if terminal.child_pid:
            try:
                os.kill(terminal.child_pid, 9)
            except:
                pass
        if terminal.fd:
            os.close(terminal.fd)
        del terminals[session_id]

def read_output(session_id):
    """Background task to read terminal output"""
    while session_id in terminals:
        terminal = terminals[session_id]
        if terminal.fd:
            try:
                ready, _, _ = select.select([terminal.fd], [], [], 0.1)
                if ready:
                    output = terminal.read()
                    if output:
                        socketio.emit('output', {'output': output}, room=session_id)
                    else:
                        break
            except:
                break

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
EOF
```

---

## Step 3: Build Docker Image

### Set Environment Variables

```bash
# Set your project ID
export PROJECT_ID=innovative-games-YOURNAME

# Verify
echo $PROJECT_ID
```

### Build the Image

```bash
# Build for Cloud Run (using Cloud Build - faster)
gcloud builds submit --tag gcr.io/$PROJECT_ID/innovative-games \
  --project=$PROJECT_ID \
  -f deploy/Dockerfile.cloudrun \
  .
```

**This takes 2-5 minutes.** You'll see:

```
Creating temporary tarball archive...
Uploading tarball...
BUILD
Starting Step #0
Step #0: Pulling image: gcr.io/...
...
Step #5: Successfully tagged gcr.io/innovative-games-yourname/innovative-games
DONE
```

**Alternative: Build locally and push**

If Cloud Build fails, build locally:

```bash
# Build locally
docker build -t gcr.io/$PROJECT_ID/innovative-games \
  -f deploy/Dockerfile.cloudrun \
  .

# Configure Docker to use Google Container Registry
gcloud auth configure-docker

# Push to registry
docker push gcr.io/$PROJECT_ID/innovative-games
```

---

## Step 4: Deploy to Cloud Run

### Deploy the Service

```bash
gcloud run deploy innovative-games \
  --image gcr.io/$PROJECT_ID/innovative-games \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --port 8080 \
  --set-env-vars "SECRET_KEY=$(openssl rand -base64 32)" \
  --project=$PROJECT_ID
```

**Explanation of flags:**

| Flag | What It Does |
|------|-------------|
| `--image` | Which Docker image to deploy |
| `--platform managed` | Use fully managed Cloud Run |
| `--region us-central1` | Deploy to US region (change if needed) |
| `--allow-unauthenticated` | Anyone can access (public) |
| `--memory 512Mi` | 512 MB RAM per container |
| `--cpu 1` | 1 CPU per container |
| `--max-instances 10` | Max 10 concurrent containers |
| `--port 8080` | Container listens on port 8080 |
| `--set-env-vars` | Set secret key |

**Deployment takes 1-2 minutes.**

You'll see:
```
Deploying container to Cloud Run service [innovative-games] in project [innovative-games-yourname] region [us-central1]
✓ Deploying new service... Done.
  ✓ Creating Revision...
  ✓ Routing traffic...
Done.
Service [innovative-games] revision [innovative-games-00001-abc] has been deployed and is serving 100 percent of traffic.
Service URL: https://innovative-games-xyz123.run.app
```

**🎉 Your URL is the Service URL!**

---

## Step 5: Test Your Deployment

### Visit Your Site

```bash
# Get your URL
gcloud run services describe innovative-games \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

Copy the URL and open in your browser!

**You should see:**
- Game selection page
- Click a game
- Terminal opens
- Game runs in browser!

### Test Health Check

```bash
# Check if service is healthy
curl $(gcloud run services describe innovative-games \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')/health
```

Should return: `{"status":"healthy"}`

---

## Step 6: Configure Custom Domain (Optional)

### Add Your Domain

If you own a domain (e.g., `games.yourdomain.com`):

```bash
# Map domain to Cloud Run
gcloud run domain-mappings create \
  --service innovative-games \
  --domain games.yourdomain.com \
  --region us-central1
```

**Follow DNS instructions shown, then:**

1. Add DNS records at your domain registrar
2. Wait 10-15 minutes for propagation
3. Visit `https://games.yourdomain.com`

**SSL certificate is automatic!**

---

## Monitoring & Management

### View Logs

```bash
# Stream logs in real-time
gcloud run services logs tail innovative-games \
  --region us-central1
```

### View Metrics

```bash
# Open Cloud Console
gcloud run services describe innovative-games \
  --region us-central1 \
  --format 'value(status.url)' | \
  sed 's|https://|https://console.cloud.google.com/run/detail/us-central1/innovative-games?project='$PROJECT_ID'|'
```

Or visit: https://console.cloud.google.com/run

**You'll see:**
- Request count
- Response time
- Error rate
- Container instances
- CPU/Memory usage

### Update the Service

Made changes? Redeploy:

```bash
# Rebuild image
gcloud builds submit --tag gcr.io/$PROJECT_ID/innovative-games

# Deploy (Cloud Run auto-detects new image)
gcloud run deploy innovative-games \
  --image gcr.io/$PROJECT_ID/innovative-games \
  --region us-central1
```

**Zero downtime deployment!** Cloud Run gradually shifts traffic.

---

## Cost Estimation

### Free Tier (Forever)

Cloud Run free tier includes:
- **2 million requests/month**
- **360,000 GB-seconds** of memory
- **180,000 vCPU-seconds**

### Example Costs (After Free Tier)

**Scenario: 10,000 users/month**

Assuming each user:
- Plays 1 game
- Session lasts 5 minutes
- Uses 512 MB RAM, 1 CPU

```
Requests: 10,000 (FREE - under 2M limit)
Memory:   10,000 sessions × 5 min × 512 MB = ~$1.20
CPU:      10,000 sessions × 5 min × 1 vCPU = ~$2.40
Total:    ~$3.60/month
```

**Most likely: $0/month** (free tier covers most usage)

### View Your Bill

```bash
# Open billing dashboard
echo "https://console.cloud.google.com/billing?project=$PROJECT_ID"
```

---

## Scaling Configuration

### Adjust Resources

**More memory (for complex games):**
```bash
gcloud run services update innovative-games \
  --memory 1Gi \
  --region us-central1
```

**More CPU:**
```bash
gcloud run services update innovative-games \
  --cpu 2 \
  --region us-central1
```

**More concurrent containers:**
```bash
gcloud run services update innovative-games \
  --max-instances 100 \
  --region us-central1
```

### Auto-Scaling Settings

**Minimum instances (always warm):**
```bash
gcloud run services update innovative-games \
  --min-instances 1 \
  --region us-central1
```

⚠️ **Note:** Min instances = always running = always paying (but faster for users)

**Concurrency (requests per container):**
```bash
gcloud run services update innovative-games \
  --concurrency 80 \
  --region us-central1
```

Default is 80 concurrent requests per container.

---

## Troubleshooting

### Container Fails to Start

**Check logs:**
```bash
gcloud run services logs tail innovative-games --region us-central1
```

**Common issues:**

1. **Port mismatch:**
   - Ensure `PORT=8080` in Dockerfile
   - Ensure app listens on `PORT` environment variable

2. **Missing dependencies:**
   - Check `requirements.txt` includes all packages
   - Rebuild image

3. **File paths wrong:**
   - Games should be in `/app/games/`
   - Templates in `/app/templates/`

### Timeout Errors

Cloud Run timeout is 60 minutes by default. Increase if needed:

```bash
gcloud run services update innovative-games \
  --timeout 3600 \
  --region us-central1
```

### Memory Issues

If containers crash (OOM - Out of Memory):

```bash
gcloud run services update innovative-games \
  --memory 1Gi \
  --region us-central1
```

### WebSocket Not Working

Ensure your client connects to WSS (not WS) on the Cloud Run URL.

Update `templates/terminal.html` if needed:
```javascript
const socket = io({
    transports: ['websocket'],
    upgrade: false
});
```

---

## Security Best Practices

### 1. Set Secret Key

```bash
# Generate strong secret
SECRET_KEY=$(openssl rand -base64 32)

# Update service
gcloud run services update innovative-games \
  --set-env-vars "SECRET_KEY=$SECRET_KEY" \
  --region us-central1
```

### 2. Restrict Access (Optional)

Make the service private:

```bash
gcloud run services update innovative-games \
  --no-allow-unauthenticated \
  --region us-central1
```

Then add authentication (OAuth, etc.)

### 3. Rate Limiting

Add Cloud Armor for DDoS protection:

```bash
# Enable Cloud Armor
gcloud compute security-policies create game-protection \
  --description "Rate limiting for games"

# Add rate limit rule
gcloud compute security-policies rules create 1000 \
  --security-policy game-protection \
  --expression "true" \
  --action "rate-based-ban" \
  --rate-limit-threshold-count 100 \
  --rate-limit-threshold-interval-sec 60
```

---

## Cleanup (Delete Everything)

### Delete Cloud Run Service

```bash
gcloud run services delete innovative-games \
  --region us-central1
```

### Delete Container Images

```bash
gcloud container images delete gcr.io/$PROJECT_ID/innovative-games
```

### Delete Project (Everything)

```bash
gcloud projects delete $PROJECT_ID
```

⚠️ **This deletes EVERYTHING in the project permanently!**

---

## Quick Reference

### Common Commands

```bash
# Deploy/Update
gcloud run deploy innovative-games \
  --image gcr.io/$PROJECT_ID/innovative-games \
  --region us-central1

# View logs
gcloud run services logs tail innovative-games --region us-central1

# Get URL
gcloud run services describe innovative-games \
  --region us-central1 \
  --format 'value(status.url)'

# View service details
gcloud run services describe innovative-games --region us-central1

# List all services
gcloud run services list

# Delete service
gcloud run services delete innovative-games --region us-central1
```

### Environment Variables

```bash
# View current env vars
gcloud run services describe innovative-games \
  --region us-central1 \
  --format 'value(spec.template.spec.containers[0].env)'

# Update env var
gcloud run services update innovative-games \
  --set-env-vars "NEW_VAR=value" \
  --region us-central1

# Remove env var
gcloud run services update innovative-games \
  --remove-env-vars "VAR_NAME" \
  --region us-central1
```

---

## Next Steps

1. ✅ **Test all games** - Make sure every game works
2. ✅ **Share URL** - Give the URL to friends!
3. ✅ **Monitor usage** - Watch Cloud Console metrics
4. ✅ **Set up alerts** - Get notified of errors
5. ✅ **Add custom domain** - Use your own domain
6. ✅ **Optimize costs** - Adjust resources based on usage

---

## Support Resources

- **Cloud Run Docs:** https://cloud.google.com/run/docs
- **Pricing Calculator:** https://cloud.google.com/products/calculator
- **Community:** https://stackoverflow.com/questions/tagged/google-cloud-run
- **Status:** https://status.cloud.google.com

---

**🎉 Congratulations! Your games are now deployed to the cloud!**

Share your URL and let people play!
