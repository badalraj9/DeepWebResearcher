# DeepWeb Researcher - Deployment Guide

This guide will help you deploy the DeepWeb Researcher application to production or development environments.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- API keys for the services you want to use:
  - OpenAI API Key (optional)
  - Tavily API Key (optional)
  - OpenRouter API Key (optional)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd deepwebreserch
```

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```bash
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Security
JWT_SECRET_KEY=your_secure_jwt_secret_key_here

# Optional: OpenRouter Configuration
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

### 3. Deploy

#### Production Deployment

```bash
# Make the deployment script executable
chmod +x deploy.sh

# Deploy to production
./deploy.sh deploy
```

#### Development Deployment

```bash
# Deploy for development
./deploy.sh dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/health

## 📋 Manual Deployment

### Using Docker Compose

#### Production

```bash
# Build and start services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Development

```bash
# Build and start development services
docker-compose -f docker-compose.dev.yml up -d --build

# View development logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop development services
docker-compose -f docker-compose.dev.yml down
```

### Manual Frontend Deployment

```bash
cd ChatBot

# Install dependencies
npm install

# Build for production
npm run build:prod

# Start production server
npm start
```

### Manual Backend Deployment

```bash
cd DeepWebResearcher

# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn (production)
gunicorn --config gunicorn.conf.py app_with_auth:app

# Run with Flask (development)
python app_with_auth.py
```

## 🔧 Configuration

### Frontend Configuration

The frontend uses Vite and can be configured through environment variables:

```bash
# ChatBot/.env
VITE_API_URL=http://localhost:5001
VITE_APP_NAME=DeepWeb Researcher
VITE_APP_VERSION=1.0.0
VITE_DEV_MODE=false
VITE_ENABLE_LOGGING=false
```

### Backend Configuration

The backend uses Flask and can be configured through environment variables:

```bash
# Environment variables for backend
FLASK_ENV=production
FLASK_APP=app_with_auth.py
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
OPENROUTER_API_KEY=your-openrouter-key
```

## 🌐 Production Deployment

### Using a Reverse Proxy (Nginx)

For production, you can use the included Nginx configuration:

```bash
# Start with Nginx reverse proxy
docker-compose --profile production up -d
```

### SSL/HTTPS Setup

1. Place your SSL certificates in `./nginx/ssl/`
2. Update the Nginx configuration in `ChatBot/nginx.conf`
3. Uncomment SSL lines in the configuration

### Environment-Specific Deployments

#### AWS EC2

```bash
# Install Docker on EC2
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy
./deploy.sh deploy
```

#### Google Cloud Platform

```bash
# Install Docker on GCP
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy
./deploy.sh deploy
```

#### DigitalOcean

```bash
# Install Docker on DigitalOcean
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy
./deploy.sh deploy
```

## 🔍 Monitoring and Logs

### View Logs

```bash
# Production logs
./deploy.sh logs

# Development logs
./deploy.sh logs-dev

# Specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Health Checks

The application includes health check endpoints:

- Backend: `http://localhost:5001/health`
- Frontend: `http://localhost:3000/health`

### Monitoring

You can monitor the application using:

```bash
# Check container status
docker-compose ps

# Check resource usage
docker stats

# Check logs
docker-compose logs --tail=100
```

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :3000
sudo lsof -i :5001

# Kill the process or change ports in docker-compose.yml
```

#### Permission Issues

```bash
# Fix Docker permissions
sudo chmod 666 /var/run/docker.sock

# Or add user to docker group
sudo usermod -aG docker $USER
```

#### Build Failures

```bash
# Clean and rebuild
docker-compose down
docker system prune -f
docker-compose build --no-cache
```

#### Database Issues

```bash
# Reset database (WARNING: This will delete all data)
rm DeepWebResearcher/research_database.sqlite
docker-compose restart backend
```

### Debug Mode

For debugging, you can run services in debug mode:

```bash
# Frontend debug
cd ChatBot
npm run dev

# Backend debug
cd DeepWebResearcher
python app_with_auth.py
```

## 🔒 Security Considerations

### Production Security Checklist

- [ ] Change default JWT secret key
- [ ] Use HTTPS in production
- [ ] Set up proper firewall rules
- [ ] Regularly update dependencies
- [ ] Monitor logs for suspicious activity
- [ ] Use strong API keys
- [ ] Implement rate limiting
- [ ] Set up backup strategy

### Environment Variables Security

```bash
# Generate secure JWT secret
openssl rand -hex 32

# Use environment-specific .env files
.env.production
.env.staging
.env.development
```

## 📊 Performance Optimization

### Frontend Optimization

- Enable gzip compression in Nginx
- Use CDN for static assets
- Implement lazy loading
- Optimize bundle size

### Backend Optimization

- Use multiple Gunicorn workers
- Implement caching
- Optimize database queries
- Use connection pooling

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and deploy
./deploy.sh deploy
```

### Backup Strategy

```bash
# Backup database
cp DeepWebResearcher/research_database.sqlite backup_$(date +%Y%m%d_%H%M%S).sqlite

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d_%H%M%S).tar.gz logs/
```

### Rollback Strategy

```bash
# Rollback to previous version
git checkout <previous-commit>
./deploy.sh deploy
```

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review logs for error messages
3. Check GitHub issues
4. Create a new issue with detailed information

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 