# 🚨 Railway Nixpacks Build Fix

## 🔍 **The Problem**
Railway's Nixpacks is having trouble detecting the correct build configuration because it's looking at the root directory which contains multiple services.

## ✅ **Solution: Deploy Services Separately**

### **Step 1: Deploy Backend First**

1. **Go to [Railway.app](https://railway.app)**
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository: `badalraj9/DeepWebResearcher`**
5. **In the configuration:**
   - **Root Directory**: `DeepWebResearcher`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. **Add Environment Variables:**
   ```
   OPENROUTER_API_KEY=your_openrouter_key
   TAVILY_API_KEY=your_tavily_key
   ```
7. **Click "Deploy"**

### **Step 2: Deploy Frontend**

1. **In the same Railway project, click "New Service"**
2. **Select "GitHub Repo"**
3. **Choose the same repository: `badalraj9/DeepWebResearcher`**
4. **In the configuration:**
   - **Root Directory**: `ChatBot`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npx serve -s dist -l 3000`
5. **Click "Deploy"**

### **Step 3: Connect Services**

1. **Get your backend URL** (e.g., `https://your-backend.railway.app`)
2. **In the frontend service settings, add environment variable:**
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```
3. **Redeploy the frontend service**

## 🎯 **Alternative: Use Render (Easier)**

If Railway continues to have issues, Render is often more reliable for multi-service deployments:

### **Backend on Render**
1. **Go to [Render.com](https://render.com)**
2. **Create new "Web Service"**
3. **Connect GitHub repository**
4. **Configure:**
   - **Root Directory**: `DeepWebResearcher`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. **Add environment variables**
6. **Deploy**

### **Frontend on Render**
1. **Create new "Static Site"**
2. **Connect same repository**
3. **Configure:**
   - **Root Directory**: `ChatBot`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. **Deploy**

## 🔧 **Manual Railway CLI Deployment**

If the web interface doesn't work, use the CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Create project
railway init

# Add backend service
railway service create backend
railway service connect backend --dir DeepWebResearcher

# Add frontend service
railway service create frontend
railway service connect frontend --dir ChatBot

# Deploy both
railway up
```

## 🚨 **Quick Fix: Deploy Backend Only First**

If you want to test quickly:

1. **Deploy only the backend** using the steps above
2. **Test the API** at `https://your-backend.railway.app/health`
3. **Then add the frontend** as a separate service

## 📋 **Environment Variables Checklist**

### **Backend Service:**
```
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
```

### **Frontend Service:**
```
VITE_API_URL=https://your-backend-url.railway.app
```

## 🎉 **Success Indicators**

- ✅ Backend responds at `/health` endpoint
- ✅ Frontend loads without errors
- ✅ Research functionality works
- ✅ LaTeX Executive Summary generates correctly
- ✅ No CORS errors in browser console

## 📞 **If Still Having Issues**

1. **Check Railway logs** for specific error messages
2. **Try Render** as an alternative (often more reliable)
3. **Deploy services one at a time** to isolate issues
4. **Check environment variables** are set correctly 