# GitHub Pages Deployment Guide

## 🚀 Quick Start

### Prerequisites
- GitHub account
- Repository with your code
- Node.js 18+

---

## Method 1: Automatic Deployment (GitHub Actions)

### Step 1: Push to GitHub
```bash
cd c:\Users\VICTUS\Desktop\exam compt\examace
git init
git add .
git commit -m "Initial commit - ExamAce frontend"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/examace.git
git push -u origin main
```

### Step 2: Enable GitHub Pages
1. Go to your repository on GitHub
2. Settings → Pages
3. Under "Build and deployment":
   - **Source**: GitHub Actions
   - **Branch**: (auto-selected)
4. Wait for workflow to complete

### Step 3: Access Your App
Your frontend will be live at: **https://YOUR_USERNAME.github.io/examace/**

---

## Method 2: Manual Deployment

### Step 1: Build the Frontend
```bash
cd frontend
npm install
npm run build
```

### Step 2: Create gh-pages Branch
```bash
git checkout --orphan gh-pages
git rm -rf .
echo "# ExamAce Frontend" > README.md
git add .
git commit -m "Initial gh-pages commit"
git push origin gh-pages
```

### Step 3: Deploy Build Output
```bash
npm run build
git checkout gh-pages
cp -r dist/* .
git add .
git commit -m "Deploy frontend build"
git push origin gh-pages
git checkout main
```

---

## ⚙️ Backend Configuration

**Important:** GitHub Pages only hosts static files. Your backend API must be:

### Option A: Deploy Backend Separately
- Deploy backend to Heroku, Railway, Render, or AWS
- Update API endpoint in frontend:

**File:** `frontend/src/services/endpoints.js`
```javascript
// Change from:
const API_BASE = 'http://localhost:8000'

// To:
const API_BASE = 'https://your-backend-url.com'
```

### Option B: Use a Proxy Service
Use CORS proxy or API gateway if needed

### Option C: Deploy Full Stack
Use Docker + Cloud (see DEPLOYMENT.md for alternatives)

---

## 📋 Environment Variables

Create `frontend/.env.production` for production:
```env
VITE_API_URL=https://your-backend-api.com
VITE_BASE_URL=/examace/
```

---

## 🔄 Continuous Deployment

Once set up, any push to `main` branch will:
1. ✅ Trigger GitHub Actions workflow
2. ✅ Build the frontend
3. ✅ Deploy to GitHub Pages automatically
4. ✅ Live at: `https://YOUR_USERNAME.github.io/examace/`

---

## ✅ Verify Deployment

1. Check GitHub Actions tab → Workflow status
2. Visit: `https://YOUR_USERNAME.github.io/examace/`
3. If 404 error: Check "Settings → Pages → Source"

---

## 🛠️ Troubleshooting

### Issue: 404 Error
**Solution:** Make sure base URL in `vite.config.js` matches repository name:
```javascript
base: '/examace/'  // Match repo name
```

### Issue: API calls failing
**Solution:** Update backend URL in `src/services/endpoints.js`:
```javascript
const API_BASE = 'https://your-deployed-backend.com'
```

### Issue: Blank page
**Solution:** Check browser console for errors, verify build output

---

## 📊 Next Steps

1. **Deploy Backend** to Heroku, Railway, or AWS
2. **Update API endpoint** in frontend
3. **Test all features** in production
4. **Monitor performance** and logs

---

## 🎯 Deployment Checklist

- [ ] Push code to GitHub
- [ ] Enable GitHub Pages
- [ ] Wait for workflow to complete
- [ ] Update backend API URL
- [ ] Test login/signup
- [ ] Test exam features
- [ ] Verify redirects work
- [ ] Check console for errors
- [ ] Monitor GitHub Actions logs

---

**Need help?** Check the main README or contact support!
