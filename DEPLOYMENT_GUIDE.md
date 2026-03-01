# 🚀 Deployment Guide: Backend on Fly.io + Frontend on Vercel

## Why This Combination is PERFECT

✅ **Fly.io Backend**
- Docker support = FFmpeg available
- 1GB RAM = Enough for AI models
- Persistent storage for models
- Global edge network

✅ **Vercel Frontend**
- Optimized for React/Vite
- Automatic deployments from Git
- Global CDN
- Zero configuration
- Free SSL

## 📋 Prerequisites

### For Fly.io (Backend)
```bash
# Install Fly.io CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login
```

### For Vercel (Frontend)
```bash
# Install Vercel CLI (optional)
npm install -g vercel

# Or use Vercel Dashboard (recommended)
# https://vercel.com
```

---

## 🎯 STEP 1: Deploy Backend to Fly.io

### 1.1 Navigate to Backend Directory
```bash
cd backend
```

### 1.2 Launch Fly.io App
```bash
fly launch --name aivideo-backend --region iad --no-deploy
```

Answer the prompts:
- PostgreSQL database? → **No**
- Redis database? → **No**
- Deploy now? → **No**

### 1.3 Create Persistent Volume (Optional but Recommended)
```bash
fly volumes create aivideo_data --region iad --size 1
```

### 1.4 Deploy Backend
```bash
fly deploy
```

### 1.5 Get Your Backend URL
```bash
fly info
```

Your backend will be at: `https://aivideo-backend.fly.dev`

### 1.6 Test Backend
```bash
# Test health endpoint
curl https://aivideo-backend.fly.dev/

# View logs
fly logs
```

---

## 🎨 STEP 2: Deploy Frontend to Vercel

### Option A: Using Vercel Dashboard (Recommended)

1. **Push Code to GitHub**
   ```bash
   cd ..  # Go to project root
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Go to Vercel Dashboard**
   - Visit https://vercel.com/new
   - Click "Import Project"
   - Select your GitHub repository

3. **Configure Project**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add Environment Variable**
   - Click "Environment Variables"
   - Add:
     - **Name**: `VITE_API_URL`
     - **Value**: `https://aivideo-backend.fly.dev`
   - Apply to: Production, Preview, Development

5. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes
   - Your frontend will be at: `https://your-project.vercel.app`

### Option B: Using Vercel CLI

```bash
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod

# When prompted:
# - Set up and deploy? → Yes
# - Which scope? → Your account
# - Link to existing project? → No
# - Project name? → aivideo-frontend
# - Directory? → ./
# - Override settings? → Yes
# - Build Command? → npm run build
# - Output Directory? → dist
# - Development Command? → npm run dev
```

Then set environment variable:
```bash
vercel env add VITE_API_URL production
# Enter: https://aivideo-backend.fly.dev
```

Redeploy:
```bash
vercel --prod
```

---

## 🔧 STEP 3: Configure CORS

Update `backend/app.py` to allow requests from Vercel:

```python
from flask_cors import CORS

# Update CORS configuration
CORS(app, origins=[
    "http://localhost:5173",  # Local development
    "https://your-project.vercel.app",  # Replace with your Vercel URL
    "https://*.vercel.app",  # Allow all Vercel preview deployments
])
```

Redeploy backend:
```bash
cd backend
fly deploy
```

---

## ✅ Verification Checklist

### Backend (Fly.io)
- [ ] Backend deployed successfully
- [ ] Health check endpoint works: `https://aivideo-backend.fly.dev/`
- [ ] Logs show no errors: `fly logs`
- [ ] FFmpeg is available (check logs during video generation)

### Frontend (Vercel)
- [ ] Frontend deployed successfully
- [ ] Environment variable `VITE_API_URL` is set
- [ ] Can access frontend URL
- [ ] No console errors in browser

### Integration
- [ ] Frontend can connect to backend
- [ ] CORS is configured correctly
- [ ] Text support works
- [ ] Audio recording works
- [ ] Video generation works

---

## 🧪 Testing Your Deployment

### Test Backend Directly
```bash
# Health check
curl https://aivideo-backend.fly.dev/

# Test text support
curl -X POST https://aivideo-backend.fly.dev/text-support \
  -H "Content-Type: application/json" \
  -d '{"text": "I need help with my order"}'

# System info
curl https://aivideo-backend.fly.dev/system-info
```

### Test Frontend
1. Open your Vercel URL in browser
2. Go to Video Help page
3. Record audio or type text
4. Check if AI responds

---

## 📊 Resource Usage & Costs

### Fly.io Backend (Free Tier)
- **Compute**: 1 shared-cpu-1x VM with 1GB RAM
- **Storage**: 1GB persistent volume
- **Bandwidth**: 100GB/month
- **Cost**: **$0/month** (within free tier)

### Vercel Frontend (Free Tier)
- **Bandwidth**: 100GB/month
- **Build Minutes**: 6,000 minutes/month
- **Deployments**: Unlimited
- **Cost**: **$0/month** (within free tier)

**Total Monthly Cost: $0** 🎉

---

## 🔄 Continuous Deployment

### Backend (Fly.io)
Every time you push to GitHub, manually deploy:
```bash
cd backend
fly deploy
```

Or set up GitHub Actions (see CI/CD section below)

### Frontend (Vercel)
Automatic! Every push to `main` branch triggers deployment.

Preview deployments for pull requests are automatic too.

---

## 🤖 CI/CD Setup (Optional)

### GitHub Actions for Fly.io Backend

Create `.github/workflows/deploy-backend.yml`:

```yaml
name: Deploy Backend to Fly.io

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: superfly/flyctl-actions/setup-flyctl@master
      
      - name: Deploy to Fly.io
        run: flyctl deploy --remote-only
        working-directory: ./backend
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

Get your Fly.io token:
```bash
fly auth token
```

Add it to GitHub:
- Go to repository Settings → Secrets → Actions
- Add secret: `FLY_API_TOKEN`

### Vercel Frontend
Already automatic! No setup needed.

---

## 🐛 Troubleshooting

### Backend Issues

**Build fails:**
```bash
# Check Dockerfile locally
cd backend
docker build -t test .

# If it works, deploy again
fly deploy
```

**App crashes:**
```bash
# Check logs
fly logs

# SSH into machine
fly ssh console

# Check memory
fly vm status
```

**Video generation fails:**
```bash
# SSH into machine
fly ssh console

# Check ffmpeg
ffmpeg -version

# Check dataset
ls -la dataset/
```

### Frontend Issues

**Build fails on Vercel:**
- Check build logs in Vercel dashboard
- Verify `package.json` scripts
- Check Node.js version compatibility

**API connection fails:**
- Verify `VITE_API_URL` environment variable
- Check CORS configuration in backend
- Check browser console for errors

**Environment variable not working:**
- Redeploy after adding env vars
- Check if variable name starts with `VITE_`
- Clear browser cache

---

## 🔒 Security Best Practices

### Backend (Fly.io)
```bash
# Set secrets
fly secrets set FLASK_SECRET_KEY=$(openssl rand -hex 32)

# List secrets
fly secrets list
```

### Frontend (Vercel)
- Never commit `.env` files
- Use Vercel environment variables
- Different values for production/preview/development

### CORS Configuration
Only allow your Vercel domain:
```python
CORS(app, origins=[
    "https://your-project.vercel.app",
    "https://*.vercel.app",  # For preview deployments
])
```

---

## 📈 Monitoring

### Fly.io Backend
```bash
# View metrics
fly dashboard

# Check status
fly status

# View logs (real-time)
fly logs

# Check health
fly checks list
```

### Vercel Frontend
- Go to Vercel Dashboard
- View Analytics
- Check deployment logs
- Monitor performance

---

## 🚀 Quick Commands Reference

### Backend (Fly.io)
```bash
cd backend

# Deploy
fly deploy

# Logs
fly logs

# Status
fly status

# SSH
fly ssh console

# Restart
fly apps restart

# Scale
fly scale memory 2048
```

### Frontend (Vercel)
```bash
cd frontend

# Deploy
vercel --prod

# View deployments
vercel ls

# View logs
vercel logs

# Environment variables
vercel env ls
vercel env add VITE_API_URL production
```

---

## 🎉 Success!

Your application is now live:
- **Backend**: https://aivideo-backend.fly.dev
- **Frontend**: https://your-project.vercel.app

Test the complete flow:
1. Open frontend URL
2. Go to Video Help page
3. Record audio or type message
4. Watch AI generate video response

---

## 📞 Support Resources

- **Fly.io**: https://fly.io/docs
- **Vercel**: https://vercel.com/docs
- **Fly.io Community**: https://community.fly.io
- **Vercel Discord**: https://vercel.com/discord

---

**🎊 Congratulations! Your AI Video Responder is now live!**
