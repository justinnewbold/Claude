# Deployment Troubleshooting Guide

## ModuleNotFoundError: No module named 'X'

### Problem
You see an error like:
```
ModuleNotFoundError: No module named 'otter_client'
ModuleNotFoundError: No module named 'data_manager'
```

### Cause
The Docker build is copying Python files from your repository that have dependencies not related to the games.

### Solution

**Option 1: Use the fixed Dockerfile (Recommended)**

```bash
# The Dockerfile.cloudrun is now fixed to only copy game files
cd deploy

# Rebuild with the corrected Dockerfile
gcloud builds submit --tag gcr.io/PROJECT_ID/innovative-games \
  -f Dockerfile.cloudrun \
  ../

# Redeploy
gcloud run deploy innovative-games \
  --image gcr.io/PROJECT_ID/innovative-games \
  --region us-central1
```

**Option 2: Clean build**

```bash
# Remove any conflicting files
cd /home/user/Claude

# Build with .dockerignore (now in place)
gcloud builds submit --tag gcr.io/PROJECT_ID/innovative-games \
  -f deploy/Dockerfile.cloudrun \
  .
```

**Option 3: Local Docker test first**

```bash
# Test locally to see what's being copied
cd /home/user/Claude

docker build -t test-games -f deploy/Dockerfile.cloudrun .

# Check what's in the image
docker run -it test-games ls -la /app
docker run -it test-games ls -la /app/games

# If it looks good, push to Cloud Run
docker tag test-games gcr.io/PROJECT_ID/innovative-games
docker push gcr.io/PROJECT_ID/innovative-games

gcloud run deploy innovative-games \
  --image gcr.io/PROJECT_ID/innovative-games \
  --region us-central1
```

---

## Container fails to start

### Problem
```
ERROR: Container failed to start
```

### Check logs
```bash
gcloud run services logs tail innovative-games --region us-central1
```

### Common causes

**1. Port mismatch**
- Solution: Ensure `PORT=8080` environment variable is set
- Check: `ENV PORT=8080` in Dockerfile

**2. App not listening on correct port**
- Solution: App should use `os.environ.get('PORT', 8080)`
- The Dockerfile.cloudrun already has this fixed

**3. Missing dependencies**
- Check requirements.txt includes:
  - Flask
  - flask-socketio
  - python-socketio
  - eventlet

---

## WebSocket connection fails

### Problem
Terminal doesn't connect or shows "Disconnected"

### Solution 1: Check browser console
Open browser DevTools (F12) and look for errors.

### Solution 2: Verify WebSocket upgrade
Cloud Run supports WebSockets, but check:

```bash
# Ensure service allows WebSocket
gcloud run services describe innovative-games \
  --region us-central1 \
  --format json | grep -i websocket
```

### Solution 3: Update templates/terminal.html

Ensure Socket.IO is configured correctly:

```javascript
const socket = io({
    transports: ['websocket', 'polling'],
    upgrade: true
});
```

---

## 403 Forbidden

### Problem
```
Error: Forbidden
Your client does not have permission
```

### Solution
Service needs to allow unauthenticated access:

```bash
gcloud run services add-iam-policy-binding innovative-games \
  --region us-central1 \
  --member="allUsers" \
  --role="roles/run.invoker"

# Or redeploy with flag:
gcloud run deploy innovative-games \
  --allow-unauthenticated \
  --region us-central1
```

---

## Memory/CPU errors

### Problem
```
Container memory exceeded
```

### Solution
Increase resources:

```bash
gcloud run services update innovative-games \
  --memory 1Gi \
  --cpu 2 \
  --region us-central1
```

---

## Games not found

### Problem
```
Error: /app/games/echo_chambers.py not found
```

### Solution
Check Dockerfile copies games correctly:

```dockerfile
# Should have:
COPY echo_chambers.py ./games/
COPY code_archaeology.py ./games/
# ... etc
```

Test locally:
```bash
docker build -t test -f deploy/Dockerfile.cloudrun .
docker run test ls -la /app/games
```

---

## Timeout errors

### Problem
```
504 Gateway Timeout
```

### Solution
Increase timeout:

```bash
gcloud run services update innovative-games \
  --timeout 3600 \
  --region us-central1
```

---

## Build fails

### Problem
```
ERROR: build step X failed
```

### Solution 1: Check quota
Visit: https://console.cloud.google.com/iam-admin/quotas

### Solution 2: Enable billing
Free tier requires billing account (won't charge unless you exceed limits)

### Solution 3: Build locally
```bash
# Build on your machine instead of Cloud Build
docker build -t gcr.io/PROJECT_ID/innovative-games \
  -f deploy/Dockerfile.cloudrun \
  .

# Configure Docker for GCR
gcloud auth configure-docker

# Push
docker push gcr.io/PROJECT_ID/innovative-games

# Deploy
gcloud run deploy innovative-games \
  --image gcr.io/PROJECT_ID/innovative-games \
  --region us-central1
```

---

## Clean slate deployment

If all else fails, start fresh:

```bash
# 1. Delete existing service
gcloud run services delete innovative-games --region us-central1

# 2. Delete images
gcloud container images delete gcr.io/PROJECT_ID/innovative-games

# 3. Rebuild from scratch
cd /home/user/Claude

gcloud builds submit --tag gcr.io/PROJECT_ID/innovative-games \
  -f deploy/Dockerfile.cloudrun \
  .

# 4. Deploy fresh
gcloud run deploy innovative-games \
  --image gcr.io/PROJECT_ID/innovative-games \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --port 8080
```

---

## Get help

**Check Cloud Run documentation:**
https://cloud.google.com/run/docs

**View service status:**
```bash
gcloud run services describe innovative-games --region us-central1
```

**View recent logs:**
```bash
gcloud run services logs tail innovative-games --region us-central1 --limit 100
```

**Test health endpoint:**
```bash
curl $(gcloud run services describe innovative-games \
  --region us-central1 \
  --format 'value(status.url)')/health
```

Should return: `{"status":"healthy"}`

---

## Quick diagnostic checklist

Run these commands to diagnose issues:

```bash
# 1. Check service exists
gcloud run services list

# 2. Check service details
gcloud run services describe innovative-games --region us-central1

# 3. Check recent logs
gcloud run services logs tail innovative-games --region us-central1

# 4. Check image exists
gcloud container images list --repository=gcr.io/PROJECT_ID

# 5. Test locally
docker pull gcr.io/PROJECT_ID/innovative-games
docker run -p 8080:8080 gcr.io/PROJECT_ID/innovative-games
# Visit http://localhost:8080

# 6. Check billing/quotas
gcloud alpha billing accounts list
gcloud compute project-info describe --project PROJECT_ID
```
