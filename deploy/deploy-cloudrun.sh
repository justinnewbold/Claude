#!/bin/bash

# Innovative Game Collection - Google Cloud Run Deployment Script
# Automates the deployment process

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  INNOVATIVE GAME COLLECTION - GOOGLE CLOUD RUN DEPLOYMENT   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud SDK not found${NC}"
    echo ""
    echo "Please install it first:"
    echo "  macOS:   brew install --cask google-cloud-sdk"
    echo "  Linux:   curl https://sdk.cloud.google.com | bash"
    echo "  Windows: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✅ Google Cloud SDK found${NC}"

# Check if user is logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${YELLOW}🔐 Logging in to Google Cloud...${NC}"
    gcloud auth login
fi

echo -e "${GREEN}✅ Authenticated${NC}"

# Get or create project
echo ""
echo -e "${BLUE}PROJECT SETUP${NC}"
echo "─────────────────────────────────────────────────────────────"

# List existing projects
echo "Your existing projects:"
gcloud projects list --format="table(projectId,name)" 2>/dev/null || true
echo ""

read -p "Enter PROJECT_ID (or press Enter to create new): " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    # Create new project
    echo ""
    read -p "Enter a unique project name (e.g., innovative-games-john): " PROJECT_NAME

    if [ -z "$PROJECT_NAME" ]; then
        echo -e "${RED}❌ Project name cannot be empty${NC}"
        exit 1
    fi

    PROJECT_ID="$PROJECT_NAME"

    echo -e "${YELLOW}Creating project: $PROJECT_ID${NC}"
    gcloud projects create "$PROJECT_ID" --name="Innovative Games" || {
        echo -e "${RED}❌ Failed to create project. Try a different name.${NC}"
        exit 1
    }

    echo -e "${GREEN}✅ Project created${NC}"
fi

# Set active project
gcloud config set project "$PROJECT_ID"
echo -e "${GREEN}✅ Active project: $PROJECT_ID${NC}"

# Enable APIs
echo ""
echo -e "${BLUE}ENABLING APIs${NC}"
echo "─────────────────────────────────────────────────────────────"

echo "Enabling Cloud Run API..."
gcloud services enable run.googleapis.com --project="$PROJECT_ID"

echo "Enabling Container Registry API..."
gcloud services enable containerregistry.googleapis.com --project="$PROJECT_ID"

echo "Enabling Cloud Build API..."
gcloud services enable cloudbuild.googleapis.com --project="$PROJECT_ID"

echo -e "${GREEN}✅ APIs enabled${NC}"

# Select region
echo ""
echo -e "${BLUE}REGION SELECTION${NC}"
echo "─────────────────────────────────────────────────────────────"
echo "Available regions:"
echo "  1) us-central1     (Iowa, USA)"
echo "  2) us-east1        (South Carolina, USA)"
echo "  3) us-west1        (Oregon, USA)"
echo "  4) europe-west1    (Belgium)"
echo "  5) asia-east1      (Taiwan)"
echo ""
read -p "Select region [1-5] (default: 1): " REGION_CHOICE

case $REGION_CHOICE in
    2) REGION="us-east1" ;;
    3) REGION="us-west1" ;;
    4) REGION="europe-west1" ;;
    5) REGION="asia-east1" ;;
    *) REGION="us-central1" ;;
esac

echo -e "${GREEN}✅ Region: $REGION${NC}"

# Build image
echo ""
echo -e "${BLUE}BUILDING DOCKER IMAGE${NC}"
echo "─────────────────────────────────────────────────────────────"
echo "This will take 2-5 minutes..."
echo ""

cd "$(dirname "$0")/.."

# Check if Dockerfile.cloudrun exists, create if not
if [ ! -f "deploy/Dockerfile.cloudrun" ]; then
    echo "Creating Dockerfile.cloudrun..."
    cat > deploy/Dockerfile.cloudrun <<'DOCKERFILE'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY *.py ./games/
COPY *.md ./games/

COPY deploy/web-terminal/requirements.txt ./
COPY deploy/web-terminal/app.py ./
COPY deploy/web-terminal/templates ./templates/

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8080
EXPOSE 8080

CMD exec python app.py
DOCKERFILE
fi

# Update app.py to use PORT environment variable
if [ ! -f "deploy/web-terminal/app.py.backup" ]; then
    cp deploy/web-terminal/app.py deploy/web-terminal/app.py.backup

    # Add PORT support
    cat > deploy/web-terminal/app.py <<'PYTHON'
#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import pty, os, select, termios, struct, fcntl

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

class Terminal:
    def __init__(self):
        self.fd = None
        self.child_pid = None

    def spawn(self, game_file):
        (child_pid, fd) = pty.fork()
        if child_pid == 0:
            os.execvp('python3', ['python3', f'/app/games/{game_file}'])
        else:
            self.child_pid = child_pid
            self.fd = fd
            self.set_terminal_size(80, 24)
            return fd

    def set_terminal_size(self, cols, rows):
        if self.fd:
            fcntl.ioctl(self.fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))

    def read(self):
        if self.fd:
            try:
                return os.read(self.fd, 10240).decode('utf-8', errors='replace')
            except:
                return None

    def write(self, data):
        if self.fd:
            os.write(self.fd, data.encode())

terminals = {}

@app.route('/')
def index():
    games = [
        {'id': 'echo_chambers', 'name': 'Echo Chambers', 'file': 'echo_chambers.py'},
        {'id': 'code_archaeology', 'name': 'Code Archaeology', 'file': 'code_archaeology.py'},
        {'id': 'infinite_library', 'name': 'The Infinite Library', 'file': 'infinite_library.py'},
        {'id': 'forking_paths', 'name': 'The Garden of Forking Paths', 'file': 'forking_paths.py'},
        {'id': 'last_recursion', 'name': 'The Last Recursion', 'file': 'last_recursion.py'},
        {'id': 'schrodingers_dungeon', 'name': 'Schrödinger\'s Dungeon', 'file': 'schrodingers_dungeon.py'},
        {'id': 'emergence_engine', 'name': 'The Emergence Engine', 'file': 'emergence_engine.py'},
        {'id': 'ship_of_theseus', 'name': 'The Ship of Theseus', 'file': 'ship_of_theseus.py'},
        {'id': 'butterfly_effect', 'name': 'The Butterfly Effect', 'file': 'butterfly_effect.py'},
        {'id': 'syntax_tree_climber', 'name': 'Syntax Tree Climber', 'file': 'syntax_tree_climber.py'},
        {'id': 'entanglement', 'name': 'Entanglement', 'file': 'entanglement.py'},
    ]
    return render_template('index.html', games=games)

@app.route('/play/<game_file>')
def play(game_file):
    return render_template('terminal.html', game_file=game_file)

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@socketio.on('start')
def handle_start(data):
    terminal = Terminal()
    terminal.spawn(data['game_file'])
    terminals[request.sid] = terminal
    socketio.start_background_task(read_output, request.sid)

@socketio.on('input')
def handle_input(data):
    if request.sid in terminals:
        terminals[request.sid].write(data['input'])

@socketio.on('resize')
def handle_resize(data):
    if request.sid in terminals:
        terminals[request.sid].set_terminal_size(data['cols'], data['rows'])

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in terminals:
        terminal = terminals[request.sid]
        try:
            if terminal.child_pid:
                os.kill(terminal.child_pid, 9)
            if terminal.fd:
                os.close(terminal.fd)
        except:
            pass
        del terminals[request.sid]

def read_output(session_id):
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
PYTHON
fi

# Build using Cloud Build
echo "Building with Cloud Build..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/innovative-games \
  --project=$PROJECT_ID \
  -f deploy/Dockerfile.cloudrun \
  . || {
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
}

echo -e "${GREEN}✅ Image built and pushed${NC}"

# Deploy to Cloud Run
echo ""
echo -e "${BLUE}DEPLOYING TO CLOUD RUN${NC}"
echo "─────────────────────────────────────────────────────────────"

# Generate secret key
SECRET_KEY=$(openssl rand -base64 32)

echo "Deploying service..."
gcloud run deploy innovative-games \
  --image gcr.io/$PROJECT_ID/innovative-games \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --port 8080 \
  --timeout 3600 \
  --set-env-vars "SECRET_KEY=$SECRET_KEY" \
  --project=$PROJECT_ID || {
    echo -e "${RED}❌ Deployment failed${NC}"
    exit 1
}

# Get service URL
SERVICE_URL=$(gcloud run services describe innovative-games \
  --platform managed \
  --region $REGION \
  --format 'value(status.url)' \
  --project=$PROJECT_ID)

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo -e "║  ${GREEN}✅ DEPLOYMENT SUCCESSFUL!${NC}                                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${BLUE}Your games are now live at:${NC}"
echo -e "${GREEN}${BOLD}$SERVICE_URL${NC}"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo "  View logs:   gcloud run services logs tail innovative-games --region $REGION"
echo "  Update app:  gcloud builds submit --tag gcr.io/$PROJECT_ID/innovative-games"
echo "  Redeploy:    gcloud run deploy innovative-games --region $REGION"
echo "  Delete:      gcloud run services delete innovative-games --region $REGION"
echo ""
echo -e "${BLUE}Monitoring:${NC}"
echo "  https://console.cloud.google.com/run/detail/$REGION/innovative-games?project=$PROJECT_ID"
echo ""
echo -e "${YELLOW}Share this URL with others to let them play your games!${NC}"
echo ""

# Save deployment info
cat > deploy/deployment-info.txt <<EOF
Deployment Information
======================

Project ID: $PROJECT_ID
Region: $REGION
Service URL: $SERVICE_URL

Deployed: $(date)

Commands:
---------
View logs:
  gcloud run services logs tail innovative-games --region $REGION --project $PROJECT_ID

Update deployment:
  gcloud builds submit --tag gcr.io/$PROJECT_ID/innovative-games
  gcloud run deploy innovative-games --region $REGION --project $PROJECT_ID

Delete service:
  gcloud run services delete innovative-games --region $REGION --project $PROJECT_ID
EOF

echo -e "${GREEN}✅ Deployment info saved to: deploy/deployment-info.txt${NC}"
