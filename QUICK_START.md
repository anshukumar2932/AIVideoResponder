# ⚡ Quick Start: Deploy in 5 Minutes

## Backend → Fly.io | Frontend → Vercel

### 🚀 Step 1: Deploy Backend (2 minutes)

```bash
# Install Fly.io CLI (if not installed)
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Navigate to backend
cd backend

# Deploy (one command!)
fly launch --name aivideo-backend --region iad

# When prompted:
# - PostgreSQL? → No
# - Redis? → No
# - Deploy now? → Yes

# Wait 2-3 minutes for deployment
# Your backend URL: https://aivideo-backend.fly.dev
```

### 🎨 Step 2: Deploy Frontend (3 minutes)

#### Option A: Vercel Dashboard (Easiest)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Vercel"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to https://vercel.com/new
   - Click "Import Git Repository"
   - Select your repo
   - **Root Directory**: `frontend`
   - Click "Deploy"

3. **Add Environment Variable**
   - Go to Project Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://aivideo-backend.fly.dev`
   - Redeploy

#### Option B: Vercel CLI (Faster)

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel --prod

# Set environment variable
vercel env add VITE_API_URL production
# Enter: https://aivideo-backend.fly.dev

# Redeploy
vercel --prod
```

### ✅ Step 3: Update CORS (30 seconds)

Edit `backend/app.py`:
```python
CORS(app, origins=[
    "http://localhost:5173",
    "https://your-project.vercel.app",  # Replace with your Vercel URL
    "https://*.vercel.app",
])
```

Redeploy backend:
```bash
cd backend
fly deploy
```

### 🎉 Done!

- **Backend**: https://aivideo-backend.fly.dev
- **Frontend**: https://your-project.vercel.app

Test it:
1. Open frontend URL
2. Click "Video Help"
3. Record audio or type text
4. Watch AI respond!

---

## 🔧 Useful Commands

### Backend (Fly.io)
```bash
fly logs          # View logs
fly status        # Check status
fly ssh console   # SSH into machine
fly deploy        # Redeploy
```

### Frontend (Vercel)
```bash
vercel --prod     # Deploy
vercel logs       # View logs
vercel ls         # List deployments
```

---

## 🐛 Common Issues

**Backend not responding?**
```bash
fly logs  # Check for errors
```

**Frontend can't connect to backend?**
- Check VITE_API_URL in Vercel environment variables
- Check CORS in backend/app.py
- Redeploy both after changes

**Video generation fails?**
```bash
fly ssh console
ffmpeg -version  # Should show ffmpeg is installed
```

---

## 💰 Cost

**Both are FREE!** 🎉
- Fly.io: Free tier (3 VMs)
- Vercel: Free tier (unlimited deployments)

---

## 📚 Full Documentation

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

---

**Need help?** Check the logs first:
- Backend: `fly logs`
- Frontend: Vercel Dashboard → Deployments → Logs
