# 🚀 Single Deployment Guide - Deploy Everything at Once!

## 🎯 **Option 1: Railway (Recommended - Easiest)**

Railway can deploy both frontend and backend in one go!

### **Step 1: Prepare for Railway**
1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository: `badalraj9/DeepWebResearcher`**

### **Step 2: Configure Services**
Railway will automatically detect both services:

#### **Backend Service (Auto-detected)**
- **Source**: `DeepWebResearcher/`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Port**: `8000`

#### **Frontend Service (Auto-detected)**
- **Source**: `ChatBot/`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npx serve -s dist -l 3000`
- **Port**: `3000`

### **Step 3: Add Environment Variables**
In Railway dashboard, add:
```
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
```

### **Step 4: Deploy**
Click **"Deploy"** - Railway will build and deploy both services automatically!

### **Step 5: Get URLs**
- **Backend URL**: `https://your-backend.railway.app`
- **Frontend URL**: `https://your-frontend.railway.app`

---

## 🎯 **Option 2: Render (Alternative)**

### **Step 1: Create Render Account**
1. **Go to [Render.com](https://render.com)**
2. **Sign up with GitHub**

### **Step 2: Create Web Service**
1. **Click "New +" → "Web Service"**
2. **Connect your GitHub repository**
3. **Configure**:
   - **Name**: `deepwebresearcher-backend`
   - **Root Directory**: `DeepWebResearcher`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free

### **Step 3: Create Static Site**
1. **Click "New +" → "Static Site"**
2. **Connect same repository**
3. **Configure**:
   - **Name**: `deepwebresearcher-frontend`
   - **Root Directory**: `ChatBot`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

### **Step 4: Add Environment Variables**
In backend service settings, add:
```
OPENROUTER_API_KEY=your_key
TAVILY_API_KEY=your_key
```

### **Step 5: Deploy Both**
Click **"Create Web Service"** and **"Create Static Site"**

---

## 🎯 **Option 3: Heroku (Classic)**

### **Step 1: Create Heroku App**
```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create your-app-name
```

### **Step 2: Configure Buildpacks**
```bash
# Add Python buildpack for backend
heroku buildpacks:add heroku/python

# Add Node.js buildpack for frontend
heroku buildpacks:add heroku/nodejs
```

### **Step 3: Create Procfile**
Create `Procfile` in root:
```
web: cd DeepWebResearcher && python app.py
```

### **Step 4: Deploy**
```bash
git add .
git commit -m "Heroku deployment"
git push heroku main
```

---

## 🎯 **Option 4: DigitalOcean App Platform**

### **Step 1: Create App**
1. **Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)**
2. **Click "Create App"**
3. **Connect GitHub repository**

### **Step 2: Configure Services**
Add two services:

#### **Backend Service**
- **Source**: `DeepWebResearcher/`
- **Type**: Web Service
- **Build Command**: `pip install -r requirements.txt`
- **Run Command**: `python app.py`

#### **Frontend Service**
- **Source**: `ChatBot/`
- **Type**: Static Site
- **Build Command**: `npm install && npm run build`
- **Output Directory**: `dist`

### **Step 3: Deploy**
Click **"Create Resources"**

---

## 🔧 **Environment Variables Setup**

### **Required Variables**
```
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### **Optional Variables**
```
PORT=8000
NODE_ENV=production
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Build Fails**
   - Check all dependencies in `requirements.txt` and `package.json`
   - Ensure Python version compatibility
   - Verify Node.js version

2. **Services Can't Connect**
   - Check environment variables
   - Verify API keys are valid
   - Check CORS settings

3. **Frontend Can't Reach Backend**
   - Update `VITE_API_URL` in frontend environment
   - Check backend URL is correct
   - Verify backend is running

### **Quick Fixes**

```bash
# Check logs
railway logs
# or
heroku logs --tail

# Restart services
railway service restart
# or
heroku restart
```

---

## 🎉 **Success Indicators**

After deployment, verify:

- ✅ **Frontend loads** at your frontend URL
- ✅ **Backend responds** at `/health` endpoint
- ✅ **Research works** - can start new research
- ✅ **LaTeX Executive Summary** generates correctly
- ✅ **Library saves** and loads properly
- ✅ **No CORS errors** in browser console

---

## 📞 **Quick Commands**

### **Railway (Recommended)**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

### **Render**
```bash
# Deploy via GitHub integration
# Just push to main branch
git push origin main
```

### **Heroku**
```bash
# Deploy to Heroku
git push heroku main
```

---

## 🏆 **Recommended: Railway**

**Why Railway is the best choice:**
- ✅ **Single deployment** for both services
- ✅ **Automatic service detection**
- ✅ **Free tier available**
- ✅ **Easy environment variable management**
- ✅ **Built-in monitoring**
- ✅ **Automatic HTTPS**
- ✅ **GitHub integration**

**Deploy time**: ~5 minutes
**Setup complexity**: Very Easy
**Cost**: Free tier available 