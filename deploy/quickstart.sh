#!/bin/bash

# Innovative Game Collection - Quick Deploy Script
# Automatically detects and deploys to the best available platform

set -e

echo "╔═══════════════════════════════════════════════════╗"
echo "║  INNOVATIVE GAME COLLECTION - QUICK DEPLOY       ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to deploy to Railway
deploy_railway() {
    echo "🚂 Deploying to Railway.app..."

    if ! command_exists railway; then
        echo "Installing Railway CLI..."
        npm install -g @railway/cli
    fi

    cd web-terminal
    railway login
    railway init
    railway up

    echo ""
    echo "✅ Deployed to Railway!"
    echo "🌐 Get your URL with: railway domain"
}

# Function to deploy with Docker
deploy_docker() {
    echo "🐳 Deploying with Docker..."

    if ! command_exists docker; then
        echo "❌ Docker not found. Please install Docker first."
        exit 1
    fi

    cd ..
    docker build -t innovative-games -f deploy/Dockerfile .
    docker run -d -p 5000:5000 --name innovative-games innovative-games

    echo ""
    echo "✅ Running locally with Docker!"
    echo "🌐 Visit: http://localhost:5000"
}

# Function to run locally without Docker
deploy_local() {
    echo "💻 Running locally..."

    if ! command_exists python3; then
        echo "❌ Python 3 not found. Please install Python 3.6+."
        exit 1
    fi

    cd web-terminal

    # Install dependencies
    echo "Installing dependencies..."
    pip3 install -r requirements.txt

    echo ""
    echo "✅ Starting server..."
    echo "🌐 Visit: http://localhost:5000"
    echo ""
    python3 app.py
}

# Main menu
echo "Choose deployment method:"
echo ""
echo "1) Railway.app (Recommended - Easy cloud deployment)"
echo "2) Docker (Local containerized)"
echo "3) Local (Direct Python execution)"
echo "4) Show all deployment options"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        deploy_railway
        ;;
    2)
        deploy_docker
        ;;
    3)
        deploy_local
        ;;
    4)
        echo ""
        echo "📚 All deployment options:"
        echo ""
        echo "Cloud Platforms (Free tiers available):"
        echo "  • Railway.app - Fastest setup"
        echo "  • Render.com - Easy GitHub integration"
        echo "  • Heroku - Classic platform"
        echo "  • Google Cloud Run - Auto-scaling"
        echo "  • AWS ECS/Fargate - Enterprise"
        echo ""
        echo "Self-Hosted:"
        echo "  • DigitalOcean Droplet - $5/month"
        echo "  • Linode VPS - $5/month"
        echo "  • AWS EC2 - Variable pricing"
        echo ""
        echo "Container Platforms:"
        echo "  • Docker Desktop - Local testing"
        echo "  • Kubernetes - Advanced orchestration"
        echo ""
        echo "📖 See DEPLOYMENT.md for detailed instructions"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📖 For more options, see DEPLOYMENT.md"
