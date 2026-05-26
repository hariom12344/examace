# 🚀 ExamAce Deployment Guide - Quick Start

**Deployment Target:** GitHub Pages (Frontend) + Render.com (Backend)

---

## 📋 Pre-Deployment Checklist

- [ ] Have a GitHub account
- [ ] Have your code pushed to GitHub
- [ ] Frontend builds without errors
- [ ] Backend runs locally

---

## Step 1: Deploy Frontend to GitHub Pages (5 min)

### 1a. Initialize Git (if not already done)
```bash
cd "c:\Users\VICTUS\Desktop\exam compt\examace"
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

### 1b. Create GitHub Repository
1. Go to https://github.com/new
2. Name: `examace` (or your preferred name)
3. Click "Create repository"
4. Copy the URL

### 1c. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/examace.git
git push -u origin main
```

### 1d. Enable GitHub Pages
1. Go to: GitHub → Your Repo → Settings → Pages
2. Under "Build and deployment":
   - Source: `GitHub Actions`
3. Wait 2-3 minutes for deployment

✅ **Frontend Live at:** `https://YOUR_USERNAME.github.io/examace/`

---

## Step 2: Deploy Backend to Render.com (10 min)

### 2a. Prepare Backend
```bash
cd backend
pip freeze > requirements.txt
# Already exists, just verify!
```

### 2b. Ensure Procfile exists
Check: `backend/Procfile` should contain:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 2c. Push to GitHub
```bash
git add backend/Procfile requirements.txt
git commit -m "Add deployment config"
git push
```

### 2d. Deploy on Render
1. Visit https://render.com
2. Sign up (use GitHub login)
3. Dashboard → Create → Web Service
4. Select repository: `examace`
5. Settings:
   - **Name:** `examace-backend`
   - **Build command:** `pip install -r backend/requirements.txt`
   - **Start command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Region:** Choose nearest
6. Click "Create Web Service"
7. Wait 5 minutes for deployment

✅ **Backend Live at:** `https://examace-backend.onrender.com/` (your URL will differ)

---

## Step 3: Connect Frontend to Backend (5 min)

### 3a. Get Backend URL
1. Go to Render Dashboard
2. Click on your service
3. Copy the URL (e.g., `https://examace-backend-xxxx.onrender.com`)

### 3b. Update Frontend Config
Edit: `frontend/.env.production`
```env
VITE_API_URL=https://examace-backend-xxxx.onrender.com
```

Replace `examace-backend-xxxx` with your actual URL!

### 3c. Commit & Push
```bash
git add frontend/.env.production
git commit -m "Update API URL for production"
git push
```

### 3d. Wait for GitHub Pages Redeploy
- GitHub Actions will auto-deploy
- Check: GitHub → Actions tab
- Wait 2-3 minutes

---

## ✅ Verify Everything Works

### Test 1: Frontend Loads
1. Open: `https://YOUR_USERNAME.github.io/examace/`
2. Should see the login page

### Test 2: Backend API
1. Open: `https://examace-backend-xxxx.onrender.com/api/docs`
2. Should see Swagger API documentation

### Test 3: Full Flow
1. Go to frontend URL
2. Click "Sign Up"
3. Create an account (email, name, password)
4. Should be able to log in
5. Navigate to exams section
6. Should see all your exams

### Test 4: Check Browser Console
1. Open DevTools (F12)
2. Go to Console tab
3. Should NOT see red errors
4. Should see API requests going to your backend URL

---

## 🔍 Troubleshooting

### Issue: Blank Page or 404
**Solution:** 
1. Check browser console (F12) for errors
2. Verify GitHub Pages deployment completed:
   - GitHub → Actions tab → Check workflow status
3. Clear cache: Ctrl+Shift+Delete

### Issue: API Calls Failing  
**Solution:**
1. Check `.env.production` has correct backend URL
2. Verify backend is running on Render
3. Check browser console network tab for 404/500 errors
4. Backend URL should end with `/` or not, be consistent

### Issue: Signup/Login Not Working
**Solution:**
1. Open DevTools (F12) → Network tab
2. Try login
3. Check the request URL - should go to your backend
4. Check response - look for error message
5. Common issue: CORS error → Backend URL might be wrong

### Issue: Render Service Sleeping
**Solution:** Render free tier sleeps after 15 min inactivity
- Click "Resume" in Render dashboard
- Or upgrade to paid tier ($7/month)

---

## 📊 Deployment Checklist

- [ ] Frontend deployed to GitHub Pages
- [ ] Backend deployed to Render.com
- [ ] `.env.production` updated with backend URL
- [ ] API docs working: `https://backend-url/api/docs`
- [ ] Can sign up
- [ ] Can log in
- [ ] Can see exams
- [ ] Can start an exam
- [ ] No console errors

---

## 🎯 Next Steps After Deployment

1. **Share the Link:** `https://YOUR_USERNAME.github.io/examace/`
2. **Monitor Logs:**
   - Frontend: GitHub Actions
   - Backend: Render Dashboard → Logs
3. **Add More Features:** Analytics, Leaderboard, etc.
4. **Scale as Needed:** Upgrade Render tier, add database, etc.

---

## 💡 Pro Tips

1. **Keep backend awake:** Upgrade Render to paid (~$7/mo) or use a cronjob
2. **Use custom domain:** Add CNAME on Render/GitHub Pages
3. **Monitor performance:** Use browser DevTools, Render metrics
4. **Update code:** Push to GitHub → Auto-deploys to both frontend & backend!

---

## 🆘 Still Having Issues?

1. Check GitHub Actions logs
2. Check Render service logs
3. Open browser DevTools (F12)
4. Check API calls in Network tab
5. Read error messages carefully

---

**You're all set! Your ExamAce app is now live!** 🎉
