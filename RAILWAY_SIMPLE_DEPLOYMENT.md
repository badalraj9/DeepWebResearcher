# 🚀 Simple Railway Deployment - No Nixpacks Issues

## 🎯 **The Problem**
Railway's Nixpacks is having trouble with multi-service builds. Let's deploy each service separately.

## ✅ **Solution: Deploy Services One by One**

### **Step 1: Deploy Backend (Python)**

1. **Go to [Railway.app](https://railway.app)**
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository: `badalraj9/DeepWebResearcher`**
5. **In the deployment settings:**
   - **Root Directory**: `DeepWebResearcher`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. **Add Environment Variables:**
   ```
   OPENROUTER_API_KEY=your_openrouter_key
   TAVILY_API_KEY=your_tavily_key
   ```
7. **Click "Deploy"**
8. **Wait for deployment to complete**
9. **Copy the backend URL** (e.g., `https://your-backend.railway.app`)

### **Step 2: Deploy Frontend (React)**

1. **In the same Railway project, click "New Service"**
2. **Select "GitHub Repo"**
3. **Choose the same repository: `badalraj9/DeepWebResearcher`**
4. **In the deployment settings:**
   - **Root Directory**: `ChatBot`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npx serve -s dist -l 3000`
5. **Add Environment Variable:**
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```
6. **Click "Deploy"**

### **Step 3: Test Your Deployment**

1. **Test Backend**: Visit `https://your-backend.railway.app/health`
2. **Test Frontend**: Visit your frontend URL
3. **Test Research**: Try creating a new research with LaTeX Executive Summary

## 🎯 **Alternative: Use Render (More Reliable)**

If Railway continues to have issues, Render is often more reliable:

### **Backend on Render**
1. **Go to [Render.com](https://render.com)**
2. **Create new "Web Service"**
3. **Connect GitHub repository**
4. **Configure:**
   - **Root Directory**: `DeepWebResearcher`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free
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

If the web interface doesn't work:

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

## 🚨 **If You Still Get Nixpacks Errors**

1. **Try Render** instead - it's more reliable for multi-service apps
2. **Deploy backend only first** to test the API
3. **Check the logs** for specific error messages
4. **Use the CLI approach** instead of web interface

## 📞 **Quick Test Commands**

After deployment, test these endpoints:

```bash
# Test backend health
curl https://your-backend.railway.app/health

# Test research endpoint
curl -X POST https://your-backend.railway.app/research/start \
  -H "Content-Type: application/json" \
  -d '{"query":"test","style":5}'
```

## 🏆 **Recommended Approach**

1. **Start with Render** - it's more reliable for this type of project
2. **Deploy backend first** and test it
3. **Then deploy frontend** and connect them
4. **Test the LaTeX Executive Summary** feature

This approach avoids all Nixpacks issues and gives you a working deployment! 🎉 