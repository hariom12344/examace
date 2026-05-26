# Backend Deployment Guide

Your frontend will be on GitHub Pages, but you need to deploy the backend API. Here are your options:

---

## 🚀 Quick Option: Render.com (Recommended - FREE)

### Step 1: Prepare Backend
```bash
cd backend
pip freeze > requirements.txt  # Already done
```

### Step 2: Create `Procfile` in backend:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 3: Push to GitHub
```bash
git add backend/Procfile requirements.txt
git commit -m "Add deployment config"
git push origin main
```

### Step 4: Deploy on Render
1. Visit https://render.com
2. Sign up with GitHub
3. Create New → Web Service
4. Select your repository
5. Build command: `pip install -r backend/requirements.txt`
6. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Deploy!

**Your backend URL:** `https://your-app-name.onrender.com`

---

## 🚀 Alternative: Railway.app (Simple)

### Step 1: Create `railway.json`:
```json
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "restartPolicyType": "on_failure",
    "restartPolicyMaxRetries": 5
  }
}
```

### Step 2: Visit https://railway.app
1. Create account (GitHub login)
2. New Project → Deploy from GitHub
3. Select repo
4. Railway auto-detects Python
5. Add environment variables if needed
6. Deploy!

---

## 🐳 Docker Deployment

Create `docker/Dockerfile.backend`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Deploy to:
- **Railway**: Drag & drop Dockerfile
- **Render**: GitHub connected (auto-detects Dockerfile)
- **AWS**: ECR + ECS
- **DigitalOcean**: App Platform

---

## 📝 Update Frontend API URL

Once backend is deployed, update:

**File:** `frontend/src/services/endpoints.js`
```javascript
// Production URL
const API_BASE = process.env.VITE_API_URL || 'https://your-backend.onrender.com'

export default {
  LOGIN: `${API_BASE}/auth/login`,
  SIGNUP: `${API_BASE}/auth/signup`,
  EXAMS: `${API_BASE}/exams`,
  // ... etc
}
```

**File:** `frontend/.env.production`
```env
VITE_API_URL=https://your-backend.onrender.com
```

---

## 🔐 Environment Variables for Backend

Add these on your hosting platform:

```
DATABASE_URL=sqlite:///./examace.db
SECRET_KEY=your-secret-key-here
DEBUG=False
ENVIRONMENT=production
```

---

## ✅ Verification

After deployment:

1. **Test Backend:**
   ```bash
   curl https://your-backend.onrender.com/api/docs
   ```

2. **Test Frontend to Backend:**
   - Open frontend app
   - Go to Login
   - Try signup/login
   - Check browser console

3. **Check Logs:**
   - Render: Dashboard → Logs
   - Railway: Deployments → View Logs

---

## 💰 Cost Comparison

| Platform | Frontend | Backend | Cost |
|----------|----------|---------|------|
| GitHub Pages | Free | Render Free | Free |
| GitHub Pages | Free | Railway | ~$5/mo |
| GitHub Pages | Free | Heroku | $50+/mo |
| GitHub Pages | Free | AWS | Pay per use |

---

## 🎯 Full Stack Deployment Summary

1. **Frontend:** GitHub Pages (Free)
   - URL: `https://USERNAME.github.io/examace/`

2. **Backend:** Render or Railway (Free tier)
   - URL: `https://your-app.onrender.com/`

3. **Update API URL** in frontend
4. **Test everything**
5. **Share with users!**

---

**Recommended:** Use Render.com - simplest, free tier, auto-deploys from GitHub!
