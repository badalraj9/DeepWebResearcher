# DeepWebResearcher Setup Guide

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd deepwebreserch
```

### 2. Backend Setup (Python)
```bash
cd DeepWebResearcher

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp env.example .env

# Edit .env with your API keys
# GROQ_API_KEY=your_groq_api_key_here
# TAVILY_API_KEY=your_tavily_api_key_here

# Initialize database
python -c "from app import init_db; init_db()"

# Start backend server
python app.py
```

### 3. Frontend Setup (React)
```bash
cd ChatBot

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔧 Configuration

### API Keys Required
1. **Groq API Key**: For LLM services
   - Sign up at [groq.com](https://groq.com)
   - Get your API key from dashboard

2. **Tavily API Key**: For web search
   - Sign up at [tavily.com](https://tavily.com)
   - Get your API key from dashboard

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Optional
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🏗️ Architecture

### Backend (Python/Flask)
- **app.py**: Main Flask application with API endpoints
- **draftagent.py**: AI research workflow and content generation
- **research_templates.py**: Advanced research templates
- **gradio_interface.py**: Alternative Gradio interface

### Frontend (React/TypeScript)
- **src/App.tsx**: Main application component
- **src/components/**: UI components
- **src/hooks/**: Custom React hooks
- **src/pages/**: Page components
- **services/api.ts**: API service layer

## 🎯 Features

### Research Capabilities
- ✅ Multi-source research with Tavily
- ✅ AI-powered content generation with Groq
- ✅ Fact-checking and verification
- ✅ Multiple content styles (blog, report, summary)
- ✅ Advanced research templates
- ✅ Real-time progress tracking

### Content Management
- ✅ Draft library with tagging
- ✅ Playlist organization
- ✅ Rich text editor
- ✅ Export capabilities
- ✅ Version control

### User Experience
- ✅ Modern, responsive UI
- ✅ Dark/light theme
- ✅ Real-time updates
- ✅ Error boundaries
- ✅ Performance monitoring

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**
   ```bash
   # Check your .env file exists and has correct keys
   cat DeepWebResearcher/.env
   ```

2. **Database Issues**
   ```bash
   # Reinitialize database
   cd DeepWebResearcher
   python -c "from app import init_db; init_db()"
   ```

3. **Frontend Build Errors**
   ```bash
   cd ChatBot
   npm run lint  # Check for TypeScript errors
   npm run build # Test build process
   ```

4. **Port Conflicts**
   ```bash
   # Backend runs on port 5000
   # Frontend runs on port 5173
   # Check if ports are available
   netstat -an | grep :5000
   netstat -an | grep :5173
   ```

### Performance Optimization
- Use the performance monitoring hooks
- Check browser console for errors
- Monitor API response times
- Use error boundaries for graceful failures

## 📚 API Documentation

### Research Endpoints
- `POST /research/start` - Start new research
- `GET /research/results/<id>` - Get research results

### Library Endpoints
- `GET /library/drafts` - Get all drafts
- `POST /library/save-draft` - Save draft
- `GET /library/playlists` - Get playlists

## 🚀 Deployment

### Production Setup
1. Set `FLASK_ENV=production`
2. Configure proper CORS settings
3. Set up database backups
4. Configure monitoring and logging
5. Set up SSL certificates

### Docker Deployment
```dockerfile
# Example Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

### Development Workflow
1. Create feature branch
2. Make changes
3. Run tests and linting
4. Submit pull request

### Code Standards
- TypeScript strict mode enabled
- ESLint configuration enforced
- Python PEP 8 compliance
- Comprehensive error handling

## 📊 Monitoring

### Performance Metrics
- Page load times
- API response times
- User interactions
- Error tracking

### Error Handling
- Error boundaries in React
- Comprehensive logging
- User-friendly error messages
- Automatic error reporting

## 🔒 Security

### Best Practices
- API keys in environment variables
- CORS configuration
- Input validation
- SQL injection prevention
- XSS protection

### Data Protection
- User data encryption
- Secure API communication
- Regular security audits
- GDPR compliance ready

## 📈 Future Enhancements

### Planned Features
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app
- [ ] API integrations
- [ ] Advanced AI models

### Technical Improvements
- [ ] Microservices architecture
- [ ] GraphQL API
- [ ] Real-time WebSocket support
- [ ] Advanced caching
- [ ] Machine learning optimization

---

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review error logs
3. Check API documentation
4. Create an issue in the repository

**Happy Researching! 🧠🔬** 