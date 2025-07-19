# 🚨 Railway Nixpacks Fix - Force Deployment

## 🔍 **The Problem**
Railway is trying to build the entire repository as one service, but we need to deploy backend and frontend separately.

## ✅ **Solution: Force Separate Service Deployment**

### **Method 1: Railway CLI (Recommended)**

This bypasses the web interface issues:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init

# Add backend service
railway service create backend
railway service connect backend --dir DeepWebResearcher

# Add frontend service  
railway service create frontend
railway service connect frontend --dir ChatBot

# Deploy both services
railway up
```

### **Method 2: Web Interface with Manual Configuration**

1. **Go to [Railway.app](https://railway.app)**
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository: `badalraj9/DeepWebResearcher`**
5. **IMPORTANT: In the settings, set:**
   - **Root Directory**: `DeepWebResearcher` (for backend)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. **Add Environment Variables:**
   ```
   OPENROUTER_API_KEY=your_openrouter_key
   TAVILY_API_KEY=your_tavily_key
   ```
7. **Deploy this as your backend service**

### **Method 3: Create Two Separate Projects**

#### **Backend Project:**
1. **Create new Railway project**
2. **Connect GitHub repo**
3. **Set Root Directory**: `DeepWebResearcher`
4. **Deploy**

#### **Frontend Project:**
1. **Create another Railway project**
2. **Connect same GitHub repo**
3. **Set Root Directory**: `ChatBot`
4. **Add environment variable**: `VITE_API_URL=https://your-backend-url.railway.app`
5. **Deploy**

## 🔧 **Manual Service Creation**

If the above methods don't work, create services manually:

### **Step 1: Create Backend Service**
```bash
# Create backend service
railway service create backend
cd DeepWebResearcher
railway link
railway up
```

### **Step 2: Create Frontend Service**
```bash
# Create frontend service
railway service create frontend
cd ChatBot
railway link
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

## 🎯 **Alternative: Use Railway's "Empty Project" Approach**

1. **Create "Empty Project" in Railway**
2. **Add GitHub integration manually**
3. **Configure each service individually**
4. **Set root directories for each service**

## 🚨 **If Still Getting Nixpacks Errors**

### **Quick Fix: Deploy Backend Only First**
1. **Deploy only the backend** using Method 2 or 3
2. **Test the API** at `https://your-backend.railway.app/health`
3. **Then add frontend** as a separate service

### **Use Railway CLI (Most Reliable)**
The CLI approach bypasses the web interface issues and gives you full control over service configuration.

## 📞 **Troubleshooting Commands**

```bash
# Check Railway status
railway status

# View logs
railway logs

# Restart service
railway service restart

# Check environment variables
railway variables
```

## 🎉 **Success Indicators**

- ✅ Backend responds at `/health` endpoint
- ✅ Frontend loads without errors
- ✅ Research functionality works
- ✅ LaTeX Executive Summary generates correctly
- ✅ No CORS errors in browser console

## 🏆 **Recommended Approach**

1. **Use Railway CLI** (Method 1) - most reliable
2. **Deploy backend first** and test it
3. **Then deploy frontend** and connect them
4. **Test the LaTeX Executive Summary** feature

This approach will work around the Nixpacks detection issues! 🎉 