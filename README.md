# DeepWeb Researcher

An advanced AI-powered research platform that combines web search, AI analysis, and content generation capabilities.

## 🚀 Features

- **Multi-Modal Research**: Web search, AI analysis, and content generation
- **Authentication System**: User registration, login, and guest mode
- **Content Library**: Save and manage research results
- **Advanced Editor**: Rich text editing with LaTeX export
- **Real-time Processing**: Background research with status tracking
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python Flask + SQLite
- **AI Integration**: OpenAI, Tavily, OpenRouter APIs
- **Authentication**: JWT-based authentication
- **Deployment**: Docker + Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose
- API keys (optional):
  - OpenAI API Key
  - Tavily API Key
  - OpenRouter API Key

## 🚀 Quick Deployment

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
```

### 3. Deploy

```bash
# Make deployment script executable
chmod +x deploy.sh

# Deploy to production
./deploy.sh deploy

# Or deploy for development
./deploy.sh dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/health

## 🛠️ Development

### Frontend Development

```bash
cd ChatBot

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build:prod
```

### Backend Development

```bash
cd DeepWebResearcher

# Install dependencies
pip install -r requirements.txt

# Run development server
python app_with_auth.py

# Run with Gunicorn (production)
gunicorn --config gunicorn.conf.py app_with_auth:app
```

## 📁 Project Structure

```
deepwebreserch/
├── ChatBot/                 # Frontend React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   ├── hooks/          # Custom hooks
│   │   └── services/       # API services
│   ├── Dockerfile          # Frontend Docker configuration
│   └── nginx.conf          # Nginx configuration
├── DeepWebResearcher/       # Backend Python application
│   ├── app_with_auth.py    # Main Flask application
│   ├── auth_routes.py      # Authentication routes
│   ├── research_api.py     # Research API implementation
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend Docker configuration
├── docker-compose.yml      # Production Docker Compose
├── docker-compose.dev.yml  # Development Docker Compose
├── deploy.sh              # Deployment script
└── DEPLOYMENT.md          # Detailed deployment guide
```

## 🔧 Configuration

### Environment Variables

#### Frontend (ChatBot/.env)
```bash
VITE_API_URL=http://localhost:5001
VITE_APP_NAME=DeepWeb Researcher
VITE_APP_VERSION=1.0.0
VITE_DEV_MODE=false
VITE_ENABLE_LOGGING=false
```

#### Backend
```bash
FLASK_ENV=production
FLASK_APP=app_with_auth.py
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
OPENROUTER_API_KEY=your-openrouter-key
```

## 🌐 Production Deployment

### Using Docker Compose

```bash
# Production deployment
docker-compose up -d --build

# Development deployment
docker-compose -f docker-compose.dev.yml up -d --build
```

### Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🔍 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/guest` - Create guest session

### Research
- `POST /research/start` - Start research
- `GET /research/status/<id>` - Get research status
- `GET /research/results/<id>` - Get research results

### Library
- `GET /library/drafts` - Get all drafts
- `GET /library/drafts/<id>` - Get specific draft
- `POST /library/save-draft` - Save draft
- `POST /library/save-copy` - Save draft copy

### Health
- `GET /health` - Health check endpoint

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation
- Rate limiting (configurable)

## 📊 Monitoring

### Health Checks
- Backend: `http://localhost:5001/health`
- Frontend: `http://localhost:3000/health`

### Logs
```bash
# View logs
./deploy.sh logs

# View development logs
./deploy.sh logs-dev
```

## 🛠️ Troubleshooting

### Common Issues

1. **Port already in use**: Change ports in docker-compose.yml
2. **Permission issues**: Fix Docker permissions
3. **Build failures**: Clean and rebuild containers
4. **API key issues**: Check environment variables

### Debug Mode

```bash
# Frontend debug
cd ChatBot && npm run dev

# Backend debug
cd DeepWebResearcher && python app_with_auth.py
```

## 📈 Performance

### Frontend Optimizations
- Code splitting with Vite
- Lazy loading of components
- Optimized bundle size
- Gzip compression

### Backend Optimizations
- Gunicorn with multiple workers
- Database connection pooling
- Caching strategies
- Async processing

## 🔄 Updates

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and deploy
./deploy.sh deploy
```

### Backup and Rollback

```bash
# Backup database
cp DeepWebResearcher/research_database.sqlite backup.sqlite

# Rollback
git checkout <previous-commit>
./deploy.sh deploy
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For issues and questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review the [deployment guide](DEPLOYMENT.md)
3. Create a GitHub issue

## 🎯 Roadmap

- [ ] Enhanced AI models integration
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced export formats 