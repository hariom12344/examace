# Authentication System - Testing Guide

## Quick Start

### Backend Setup
```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (already done)
# Edit .env if needed with your database credentials

# Start backend
uvicorn main:app --reload
# Backend running on http://localhost:8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
# Frontend running on http://localhost:5173
```

### Database Setup
```bash
# Create PostgreSQL database
createdb examace

# The app will auto-create tables on startup
# (see Base.metadata.create_all in main.py)
```

---

## Testing Auth Endpoints

### Option 1: Using Postman (Recommended)

Import this Postman collection:

```json
{
  "info": {
    "name": "ExamAce Auth",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Signup",
      "request": {
        "method": "POST",
        "header": [
          {"key": "Content-Type", "value": "application/json"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"student@example.com\",\n  \"name\": \"John Doe\",\n  \"password\": \"Password123\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/auth/signup",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "auth", "signup"]
        }
      }
    },
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "header": [
          {"key": "Content-Type", "value": "application/json"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"student@example.com\",\n  \"password\": \"Password123\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/auth/login",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "auth", "login"]
        }
      }
    },
    {
      "name": "Refresh Token",
      "request": {
        "method": "POST",
        "header": [
          {"key": "Content-Type", "value": "application/json"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"refresh_token\": \"YOUR_REFRESH_TOKEN_HERE\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/auth/refresh",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "auth", "refresh"]
        }
      }
    },
    {
      "name": "Logout",
      "request": {
        "method": "POST",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/auth/logout",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "auth", "logout"]
        }
      }
    }
  ]
}
```

### Option 2: Using cURL

#### Signup
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "name": "John Doe",
    "password": "Password123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "Password123"
  }'
```

#### Refresh Token
```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

### Option 3: Using Frontend UI

1. Navigate to http://localhost:5173
2. Click "Sign Up" button
3. Fill in the signup form:
   - Email: `student@example.com`
   - Name: `John Doe`
   - Password: `Password123`
4. Click "Sign Up"
5. You should be redirected to `/dashboard`
6. Click "Logout" to test logout

---

## Expected Responses

### Signup Response (201 Created)
```json
{
  "id": 1,
  "email": "student@example.com",
  "name": "John Doe",
  "role": "student",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 1800
}
```

### Login Response (200 OK)
```json
{
  "id": 1,
  "email": "student@example.com",
  "name": "John Doe",
  "role": "student",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 1800
}
```

### Error: User Already Exists (400)
```json
{
  "detail": "Email already registered"
}
```

### Error: Invalid Credentials (401)
```json
{
  "detail": "Invalid email or password"
}
```

---

## Frontend Auth Flow Testing

### Test Sequence

1. **Test Signup**
   - Go to http://localhost:5173/signup
   - Fill form with:
     - Email: `test1@example.com`
     - Name: `Test User 1`
     - Password: `TestPass123`
   - Click Sign Up
   - Should redirect to `/dashboard`

2. **Test Login After Logout**
   - Click Logout
   - Should redirect to home page
   - Go to http://localhost:5173/login
   - Enter same credentials
   - Should redirect to `/dashboard`

3. **Test Protected Routes**
   - Try accessing `/dashboard` without login
   - Should redirect to `/login`

4. **Test Token Persistence**
   - Login successfully
   - Open browser DevTools (F12)
   - Go to Application > Local Storage
   - Verify tokens are stored:
     - `accessToken`
     - `refreshToken`
     - `user` (JSON string)

5. **Test Token Refresh**
   - Login successfully
   - Wait 30 minutes (or modify expiry in code)
   - Try making API call
   - Should automatically refresh token

---

## Common Issues & Solutions

### Issue: CORS Error
**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
- Backend CORS is configured in `main.py`
- Ensure frontend URL is in `ALLOWED_ORIGINS` in `config.py`
- Restart backend: `uvicorn main:app --reload`

### Issue: Database Connection Error
**Error**: `could not connect to server: No such file or directory`

**Solution**:
```bash
# Make sure PostgreSQL is running
# macOS: brew services start postgresql
# Windows: Check Services for PostgreSQL
# Ubuntu: sudo service postgresql start

# Create database
createdb examace

# Check .env DATABASE_URL is correct
```

### Issue: "Invalid or expired token"
**Error**: 401 Unauthorized

**Solution**:
- Check token in browser DevTools Local Storage
- Token expires after 30 minutes
- Use refresh endpoint with refresh_token
- Or login again

### Issue: Password too short
**Error**: `Password must be at least 6 characters`

**Solution**:
- Use password with 6+ characters
- Example: `Password123`

---

## Database Verification

Check if users were created:

```bash
psql examace

-- List all users
SELECT id, email, name, role, is_active, created_at FROM users;

-- Count total users
SELECT COUNT(*) FROM users;

-- Exit psql
\q
```

---

## File Structure

Backend Auth Files:
```
backend/
├── main.py              # Router included
├── config.py            # Settings
├── database.py          # DB connection
├── models.py            # User model
├── schemas.py           # Pydantic schemas
├── dependencies.py      # JWT dependencies
├── routers/
│   ├── auth.py         # Auth routes
│   └── __init__.py
└── utils/
    ├── jwt_utils.py    # Token functions
    ├── password_utils.py # Hashing functions
    └── __init__.py
```

Frontend Auth Files:
```
frontend/src/
├── App.jsx              # Router setup
├── services/
│   ├── api.js          # Axios instance
│   └── auth.js         # Auth API calls
├── store/
│   ├── index.js        # Redux store
│   └── authSlice.js    # Auth reducer
├── pages/
│   ├── Home.jsx        # Landing page
│   ├── Login.jsx       # Login form
│   ├── Signup.jsx      # Signup form
│   └── Dashboard.jsx   # Protected page
└── components/
    └── ProtectedRoute.jsx # Route guard
```

---

## Next Steps

After successful auth testing:
1. Build Exam Management APIs
2. Create Test Engine UI
3. Build Result System
4. Add Analytics
5. Integrate AI Features

---

## Troubleshooting Checklist

- [ ] PostgreSQL is running
- [ ] Database `examace` exists
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend running on port 8000 (`uvicorn main:app --reload`)
- [ ] Frontend running on port 5173 (`npm run dev`)
- [ ] CORS enabled in backend
- [ ] `.env` files created in both folders
- [ ] No console errors in browser
- [ ] Tokens storing in LocalStorage

---

## Support

For issues:
1. Check browser Console (F12) for errors
2. Check backend terminal for error logs
3. Verify all files are created
4. Ensure all dependencies are installed
5. Check database connection
