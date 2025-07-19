# 🐍 Railway Python Deployment Fix

## 🔍 **The Problem**
Railway is trying to run `pip install -r requirements.txt` from the wrong directory. The error shows it's looking in the root directory instead of the `DeepWebResearcher` directory.

## ✅ **Solution: Force Python Service Detection**

### **Step 1: Use Railway CLI (Recommended)**

This gives you full control over the deployment:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init

# Add backend service with explicit directory
railway service create backend
railway service connect backend --dir DeepWebResearcher

# Set environment variables for backend
railway variables set OPENROUTER_API_KEY=your_openrouter_key
railway variables set TAVILY_API_KEY=your_tavily_key

# Deploy backend
railway up

# Add frontend service
railway service create frontend
railway service connect frontend --dir ChatBot

# Set environment variable for frontend (replace with your backend URL)
railway variables set VITE_API_URL=https://your-backend-url.railway.app

# Deploy frontend
railway up
```

### **Step 2: Web Interface with Explicit Configuration**

1. **Go to [Railway.app](https://railway.app)**
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository: `badalraj9/DeepWebResearcher`**
5. **IMPORTANT: In the deployment settings:**
   - **Root Directory**: `DeepWebResearcher`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. **Add Environment Variables:**
   ```
   OPENROUTER_API_KEY=your_openrouter_key
   TAVILY_API_KEY=your_tavily_key
   ```
7. **Click "Deploy"**

### **Step 3: Alternative - Create Empty Project**

1. **Create "Empty Project" in Railway**
2. **Add GitHub integration manually**
3. **Configure backend service:**
   - **Source**: GitHub repo
   - **Root Directory**: `DeepWebResearcher`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
4. **Add environment variables**
5. **Deploy**

## 🔧 **Manual Service Creation**

If the above methods don't work:

### **Backend Service:**
```bash
# Create backend service
railway service create backend

# Navigate to backend directory
cd DeepWebResearcher

# Link to Railway
railway link

# Set environment variables
railway variables set OPENROUTER_API_KEY=your_key
railway variables set TAVILY_API_KEY=your_key

# Deploy
railway up
```

### **Frontend Service:**
```bash
# Create frontend service
railway service create frontend

# Navigate to frontend directory
cd ChatBot

# Link to Railway
railway link

# Set environment variable (replace with your backend URL)
railway variables set VITE_API_URL=https://your-backend-url.railway.app

# Deploy
railway up
```

## 📋 **Environment Variables Setup**

### **Backend Service:**
```
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
```

### **Frontend Service:**
```
VITE_API_URL=https://your-backend-url.railway.app
```

## 🚨 **Troubleshooting**

### **If pip install still fails:**
1. **Check the logs** for specific error messages
2. **Verify requirements.txt** is in the DeepWebResearcher directory
3. **Try the CLI approach** instead of web interface
4. **Make sure Python version** is compatible (3.11+)

### **If service detection fails:**
1. **Use explicit root directory** setting
2. **Create services manually** with CLI
3. **Check for runtime.txt and Procfile** in DeepWebResearcher directory

## 📞 **Quick Test Commands**

After deployment:

```bash
# Test backend health
curl https://your-backend.railway.app/health

# Test research endpoint
curl -X POST https://your-backend.railway.app/research/start \
  -H "Content-Type: application/json" \
  -d '{"query":"test","style":5}'
```

## 🎉 **Success Indicators**

- ✅ Backend responds at `/health` endpoint
- ✅ Frontend loads without errors
- ✅ Research functionality works
- ✅ LaTeX Executive Summary generates correctly
- ✅ No pip install errors in logs

## 🏆 **Recommended Approach**

1. **Use Railway CLI** (Step 1) - most reliable
2. **Deploy backend first** and test it
3. **Then deploy frontend** and connect them
4. **Test the LaTeX Executive Summary** feature

This approach will fix the pip install error and get your Python backend deployed correctly! 🐍 