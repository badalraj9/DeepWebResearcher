#!/bin/bash

# DeepWeb Researcher Deployment Script
# This script helps deploy the application to production

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check environment variables
check_env() {
    print_status "Checking environment variables..."
    
    if [ -z "$OPENAI_API_KEY" ]; then
        print_warning "OPENAI_API_KEY is not set"
    else
        print_success "OPENAI_API_KEY is set"
    fi
    
    if [ -z "$TAVILY_API_KEY" ]; then
        print_warning "TAVILY_API_KEY is not set"
    else
        print_success "TAVILY_API_KEY is set"
    fi
    
    if [ -z "$OPENROUTER_API_KEY" ]; then
        print_warning "OPENROUTER_API_KEY is not set"
    else
        print_success "OPENROUTER_API_KEY is set"
    fi
    
    if [ -z "$JWT_SECRET_KEY" ]; then
        print_warning "JWT_SECRET_KEY is not set, using default"
        export JWT_SECRET_KEY="your-secret-key-change-in-production"
    else
        print_success "JWT_SECRET_KEY is set"
    fi
}

# Build and deploy
deploy() {
    print_status "Starting deployment..."
    
    # Stop existing containers
    print_status "Stopping existing containers..."
    docker-compose down --remove-orphans
    
    # Build images
    print_status "Building Docker images..."
    docker-compose build --no-cache
    
    # Start services
    print_status "Starting services..."
    docker-compose up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 30
    
    # Check health
    print_status "Checking service health..."
    
    # Check backend health
    if curl -f http://localhost:5001/health > /dev/null 2>&1; then
        print_success "Backend is healthy"
    else
        print_error "Backend health check failed"
        exit 1
    fi
    
    # Check frontend health
    if curl -f http://localhost:3000/health > /dev/null 2>&1; then
        print_success "Frontend is healthy"
    else
        print_warning "Frontend health check failed (this might be normal for development)"
    fi
    
    print_success "Deployment completed successfully!"
    print_status "Frontend: http://localhost:3000"
    print_status "Backend API: http://localhost:5001"
    print_status "Health Check: http://localhost:5001/health"
}

# Development deployment
deploy_dev() {
    print_status "Starting development deployment..."
    
    # Stop existing containers
    print_status "Stopping existing containers..."
    docker-compose -f docker-compose.dev.yml down --remove-orphans
    
    # Build images
    print_status "Building Docker images..."
    docker-compose -f docker-compose.dev.yml build --no-cache
    
    # Start services
    print_status "Starting development services..."
    docker-compose -f docker-compose.dev.yml up -d
    
    print_success "Development deployment completed!"
    print_status "Frontend: http://localhost:3000"
    print_status "Backend API: http://localhost:5001"
}

# Show logs
logs() {
    print_status "Showing logs..."
    docker-compose logs -f
}

# Show development logs
logs_dev() {
    print_status "Showing development logs..."
    docker-compose -f docker-compose.dev.yml logs -f
}

# Stop services
stop() {
    print_status "Stopping services..."
    docker-compose down
    print_success "Services stopped"
}

# Stop development services
stop_dev() {
    print_status "Stopping development services..."
    docker-compose -f docker-compose.dev.yml down
    print_success "Development services stopped"
}

# Clean up
clean() {
    print_status "Cleaning up..."
    docker-compose down --volumes --remove-orphans
    docker system prune -f
    print_success "Cleanup completed"
}

# Show help
show_help() {
    echo "DeepWeb Researcher Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy      Deploy to production"
    echo "  dev         Deploy for development"
    echo "  logs        Show production logs"
    echo "  logs-dev    Show development logs"
    echo "  stop        Stop production services"
    echo "  stop-dev    Stop development services"
    echo "  clean       Clean up containers and volumes"
    echo "  help        Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  OPENAI_API_KEY      OpenAI API key"
    echo "  TAVILY_API_KEY      Tavily API key"
    echo "  OPENROUTER_API_KEY  OpenRouter API key"
    echo "  JWT_SECRET_KEY      JWT secret key (optional)"
}

# Main script
case "${1:-help}" in
    deploy)
        check_docker
        check_env
        deploy
        ;;
    dev)
        check_docker
        check_env
        deploy_dev
        ;;
    logs)
        logs
        ;;
    logs-dev)
        logs_dev
        ;;
    stop)
        stop
        ;;
    stop-dev)
        stop_dev
        ;;
    clean)
        clean
        ;;
    help|*)
        show_help
        ;;
esac 