# 🚀 Deployment Guide for DeepWebResearcher

## 📋 Overview

This project consists of two main components:
1. **Frontend**: React + TypeScript (ChatBot/)
2. **Backend**: Python FastAPI (DeepWebResearcher/)

Due to Vercel's limitations with Python backends, we need to deploy them separately.

## 🎯 Option 1: Frontend on Vercel + Backend on Railway/Render (Recommended)

### Frontend Deployment (Vercel)

1. **Navigate to ChatBot directory**:
   ```bash
   cd ChatBot
   ```

2. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new
   - Set build command: `npm run build`
   - Set output directory: `dist`
   - Set install command: `npm install`

### Backend Deployment (Railway/Render)

#### Railway (Recommended)
1. **Go to [Railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Select the DeepWebResearcher directory**
4. **Add environment variables**:
   ```
   OPENROUTER_API_KEY=your_openrouter_key
   TAVILY_API_KEY=your_tavily_key
   ```
5. **Deploy**

#### Render (Alternative)
1. **Go to [Render.com](https://render.com)**
2. **Create new Web Service**
3. **Connect GitHub repository**
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. **Add environment variables**
6. **Deploy**

### Update Frontend API URL

After backend deployment, update the API URL in your frontend:

1. **In Vercel dashboard**, go to your project settings
2. **Add environment variable**:
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```
3. **Redeploy the frontend**

## 🎯 Option 2: Full Stack on Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Create new project**
3. **Add two services**:
   - **Frontend Service**: Point to ChatBot directory
   - **Backend Service**: Point to DeepWebResearcher directory
4. **Configure environment variables**
5. **Deploy both services**

## 🎯 Option 3: Full Stack on Render

1. **Go to [Render.com](https://render.com)**
2. **Create two services**:
   - **Static Site** for frontend (ChatBot/)
   - **Web Service** for backend (DeepWebResearcher/)
3. **Configure build and start commands**
4. **Add environment variables**
5. **Deploy**

## 🔧 Environment Variables

### Frontend (.env)
```env
VITE_API_URL=https://your-backend-url.com
```

### Backend (.env)
```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 🚨 Common Vercel Errors & Solutions

### BODY_NOT_A_STRING_FROM_FUNCTION
- **Cause**: Backend function returning non-string response
- **Solution**: Deploy backend separately, frontend only on Vercel

### FUNCTION_INVOCATION_FAILED
- **Cause**: Python backend not supported on Vercel
- **Solution**: Use Railway/Render for backend

### DEPLOYMENT_BLOCKED
- **Cause**: Large files or unsupported dependencies
- **Solution**: Check .gitignore, remove node_modules

## 📁 Project Structure for Deployment

```
deepwebreserch/
├── ChatBot/                 # Frontend (Vercel)
│   ├── src/
│   ├── package.json
│   ├── vercel.json
│   └── ...
└── DeepWebResearcher/       # Backend (Railway/Render)
    ├── app.py
    ├── requirements.txt
    └── ...
```

## 🔗 Quick Deploy Commands

### Frontend (Vercel)
```bash
cd ChatBot
vercel --prod
```

### Backend (Railway)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

## 📞 Support

If you encounter issues:
1. Check the deployment platform's logs
2. Verify environment variables
3. Ensure all dependencies are in package.json/requirements.txt
4. Check API endpoints are accessible

## 🎉 Success Indicators

- ✅ Frontend loads without errors
- ✅ Backend API responds to health checks
- ✅ Research functionality works
- ✅ LaTeX Executive Summary generates correctly
- ✅ Library saves and loads properly 