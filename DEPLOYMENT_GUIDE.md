# 🚀 DEPLOYMENT GUIDE - SudarshanChakraAI

## 🎯 **RECOMMENDED HOSTING: Vercel + Railway (FREE)**

### **Step 1: Deploy Backend to Railway**

1. **Go to [Railway.app](https://railway.app)**
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"

2. **Connect Your Repository**
   - Select your `SudarshanChakraAI` repository
   - Railway will detect it's a Python project

3. **Configure Backend**
   - Railway will automatically detect `requirements.txt`
   - Set environment variables (if needed):
     ```
     PYTHON_VERSION=3.11.0
     ```

4. **Deploy**
   - Railway will build and deploy automatically
   - Get your backend URL: `https://your-project-name.railway.app`

### **Step 2: Deploy Frontend to Vercel**

1. **Go to [Vercel.com](https://vercel.com)**
   - Sign up with GitHub
   - Click "New Project"
   - Import your repository

2. **Configure Frontend**
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Set Environment Variables**
   - Go to Project Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = `https://your-project-name.railway.app`

4. **Deploy**
   - Vercel will build and deploy automatically
   - Get your frontend URL: `https://your-project-name.vercel.app`

### **Step 3: Connect Custom Domain**

1. **In Vercel Dashboard**
   - Go to Domains
   - Add your domain: `sudarshanchakraai.xyz`
   - Follow DNS configuration instructions

2. **Update DNS Records**
   - Add CNAME record pointing to Vercel
   - Wait for DNS propagation (5-10 minutes)

## 🔧 **ALTERNATIVE HOSTING OPTIONS**

### **Option 1: Render (FREE)**
```bash
# Backend
- Go to render.com
- Create new Web Service
- Connect GitHub repo
- Build Command: pip install -r requirements.txt
- Start Command: python main.py

# Frontend  
- Create new Static Site
- Build Command: npm run build
- Publish Directory: out
```

### **Option 2: Heroku (PAID)**
```bash
# Backend
heroku create sudarshanchakraai-backend
git subtree push --prefix backend heroku main

# Frontend
heroku create sudarshanchakraai-frontend
git subtree push --prefix frontend heroku main
```

### **Option 3: DigitalOcean App Platform**
```bash
# Deploy both frontend and backend
- Create new app
- Connect GitHub repository
- Configure build settings
- Deploy automatically
```

## 🎯 **QUICK DEPLOYMENT (5 MINUTES)**

### **For Hackathon Demo:**

1. **Railway Backend (2 minutes)**
   ```bash
   # Go to railway.app
   # Connect GitHub repo
   # Deploy automatically
   ```

2. **Vercel Frontend (2 minutes)**
   ```bash
   # Go to vercel.com  
   # Import GitHub repo
   # Set environment variable
   # Deploy automatically
   ```

3. **Test (1 minute)**
   ```bash
   # Test repository scanning
   # Verify all features work
   # Ready for demo!
   ```

## 🔧 **TROUBLESHOOTING**

### **Backend Issues:**
- **Port Error**: Railway uses `PORT` environment variable
- **Dependencies**: Check `requirements.txt` is complete
- **Database**: SQLite works fine on Railway

### **Frontend Issues:**
- **API Connection**: Check `NEXT_PUBLIC_API_URL` environment variable
- **Build Errors**: Check Node.js version compatibility
- **CORS**: Backend CORS is already configured

### **Common Fixes:**
```bash
# If backend won't start
- Check Procfile exists
- Verify requirements.txt
- Check Python version in runtime.txt

# If frontend won't build
- Check package.json
- Verify all dependencies
- Check Next.js configuration
```

## 🎯 **PRODUCTION READY FEATURES**

### **Already Included:**
- ✅ **CORS Configuration** - Backend allows frontend domain
- ✅ **Environment Variables** - Configurable API URLs
- ✅ **Health Check Endpoint** - `/health` for monitoring
- ✅ **Error Handling** - Proper HTTP status codes
- ✅ **Security Headers** - Basic security configuration

### **Optional Enhancements:**
```bash
# Add to backend/main.py for production
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## 🚀 **DEPLOYMENT CHECKLIST**

### **Before Deploying:**
- [ ] All code is committed to GitHub
- [ ] `requirements.txt` is up to date
- [ ] `package.json` has correct scripts
- [ ] Environment variables are ready
- [ ] Custom domain is configured (if using)

### **After Deploying:**
- [ ] Backend health check passes
- [ ] Frontend loads without errors
- [ ] Repository scanning works
- [ ] File upload works
- [ ] Advanced features display correctly
- [ ] LLM dashboard functions
- [ ] All tabs in Advanced Features work

### **For Demo:**
- [ ] Test with React repository
- [ ] Verify security score calculation
- [ ] Check compliance report generation
- [ ] Confirm automated fixes display
- [ ] Test threat intelligence features

## 🎯 **FINAL DEPLOYMENT COMMANDS**

### **Railway Backend:**
```bash
# 1. Go to railway.app
# 2. Connect GitHub repo
# 3. Deploy automatically
# 4. Copy backend URL
```

### **Vercel Frontend:**
```bash
# 1. Go to vercel.com
# 2. Import GitHub repo
# 3. Set NEXT_PUBLIC_API_URL
# 4. Deploy automatically
# 5. Add custom domain
```

## 🏆 **DEMO READY!**

Your project will be live at:
- **Frontend**: `https://sudarshanchakraai.xyz`
- **Backend**: `https://your-project-name.railway.app`

**Perfect for hackathon presentation!** 🚀✨

---

**GOOD LUCK WITH YOUR DEPLOYMENT! 🎯**
