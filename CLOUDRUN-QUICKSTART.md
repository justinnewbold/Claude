# Google Cloud Run - Quick Start

Deploy your Innovative Game Collection to Google Cloud Run in 3 steps.

## Prerequisites

1. **Google Cloud Account** - Sign up at https://cloud.google.com (free $300 credit)
2. **Google Cloud SDK** - Install from https://cloud.google.com/sdk/install
3. **Docker** - Verify with `docker --version`

## Option 1: Automated Script (Easiest) ⭐

**One command to deploy everything:**

```bash
cd deploy
./deploy-cloudrun.sh
```

The script will:
- ✅ Check prerequisites
- ✅ Create/select Google Cloud project
- ✅ Enable required APIs
- ✅ Build Docker image
- ✅ Deploy to Cloud Run
- ✅ Give you a public URL

**Time: 5-10 minutes**

## Option 2: Manual Deployment

### Step 1: Setup

```bash
# Login to Google Cloud
gcloud auth login

# Create project
gcloud projects create innovative-games-YOURNAME

# Set as active
gcloud config set project innovative-games-YOURNAME

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 2: Build & Push

```bash
# Set project ID
export PROJECT_ID=innovative-games-YOURNAME

# Build image with Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/innovative-games \
  -f deploy/Dockerfile.cloudrun .
```

### Step 3: Deploy

```bash
# Deploy to Cloud Run
gcloud run deploy innovative-games \
  --image gcr.io/$PROJECT_ID/innovative-games \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --port 8080
```

**You'll get a URL like:** `https://innovative-games-xyz123.run.app`

## What You Get

- ✅ **Public URL** - Share with anyone
- ✅ **Auto-scaling** - 0 to 1000+ users automatically
- ✅ **HTTPS included** - SSL certificate automatic
- ✅ **Free tier** - 2 million requests/month free
- ✅ **Global CDN** - Fast worldwide
- ✅ **Zero maintenance** - Google handles everything

## Costs

**Free tier (forever):**
- 2 million requests/month
- 360,000 GB-seconds memory
- 180,000 vCPU-seconds

**After free tier:**
- ~$3-5/month for 10,000 users
- **$0/month if under 2M requests**

**Most likely: FREE** 🎉

## Common Commands

```bash
# View logs
gcloud run services logs tail innovative-games --region us-central1

# Update service
gcloud builds submit --tag gcr.io/$PROJECT_ID/innovative-games
gcloud run deploy innovative-games --region us-central1

# Get URL
gcloud run services describe innovative-games \
  --region us-central1 \
  --format 'value(status.url)'

# Delete service
gcloud run services delete innovative-games --region us-central1
```

## Troubleshooting

**Build fails?**
- Check Docker is running
- Verify you're logged in: `gcloud auth list`
- Check project ID: `gcloud config get-value project`

**Deployment fails?**
- Check APIs are enabled
- Verify billing is enabled (required even for free tier)
- Check quotas: https://console.cloud.google.com/quotas

**Can't access URL?**
- Check service is running: `gcloud run services list`
- Verify `--allow-unauthenticated` flag was used
- Check firewall isn't blocking

## Next Steps

1. **Test all games** - Visit your URL and try each game
2. **Monitor usage** - https://console.cloud.google.com/run
3. **Set up alerts** - Get notified of errors
4. **Custom domain** - Use your own domain name
5. **Share the URL** - Let people play!

## Full Documentation

For comprehensive guide including:
- Detailed explanations
- Custom domains
- Security hardening
- Performance optimization
- Cost optimization

See: [deploy/CLOUDRUN.md](deploy/CLOUDRUN.md)

---

**🚀 Ready to deploy?**

```bash
cd deploy
./deploy-cloudrun.sh
```

**That's it!** Your games will be live in ~5 minutes.
