# ExamAce API Documentation

## Base URL
```
Development: http://localhost:8000
Production: https://api.examace.com
```

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Auth Endpoints

### 1. User Signup
```
POST /api/auth/signup
Content-Type: application/json

Request Body:
{
  "email": "student@example.com",
  "name": "John Doe",
  "password": "SecurePassword123!",
  "role": "student"
}

Response (200):
{
  "id": 1,
  "email": "student@example.com",
  "name": "John Doe",
  "role": "student",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. User Login
```
POST /api/auth/login
Content-Type: application/json

Request Body:
{
  "email": "student@example.com",
  "password": "SecurePassword123!"
}

Response (200):
{
  "id": 1,
  "email": "student@example.com",
  "name": "John Doe",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 1800
}
```

### 3. Refresh Token
```
POST /api/auth/refresh
Content-Type: application/json

Request Body:
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response (200):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 1800
}
```

### 4. Logout
```
POST /api/auth/logout
Authorization: Bearer <token>

Response (200):
{
  "message": "Logged out successfully"
}
```

---

## Exam Endpoints

### 1. List All Exams
```
GET /api/exams?exam_type=PO&skip=0&limit=10
Authorization: Bearer <token>

Response (200):
{
  "total": 50,
  "skip": 0,
  "limit": 10,
  "exams": [
    {
      "id": 1,
      "title": "IBPS PO Mock Test 1",
      "description": "Full length mock test",
      "duration": 120,
      "total_marks": 200,
      "exam_type": "PO",
      "difficulty": "Medium",
      "sections": 3,
      "is_published": true,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 2. Get Exam Details
```
GET /api/exams/{exam_id}
Authorization: Bearer <token>

Response (200):
{
  "id": 1,
  "title": "IBPS PO Mock Test 1",
  "description": "Full length mock test",
  "duration": 120,
  "total_marks": 200,
  "exam_type": "PO",
  "difficulty": "Medium",
  "sections": [
    {
      "name": "Quantitative Ability",
      "time_limit": 40,
      "questions": 40
    },
    {
      "name": "Reasoning Ability",
      "time_limit": 40,
      "questions": 40
    },
    {
      "name": "English Language",
      "time_limit": 40,
      "questions": 40
    }
  ]
}
```

### 3. Create Exam (Admin Only)
```
POST /api/exams
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "title": "IBPS PO Mock Test 2",
  "description": "Full length mock test",
  "duration": 120,
  "total_marks": 200,
  "exam_type": "PO",
  "difficulty": "Hard",
  "sections": 3
}

Response (201):
{
  "id": 2,
  "title": "IBPS PO Mock Test 2",
  ...
}
```

---

## Question Endpoints

### 1. Get Questions (For Taking Exam)
```
GET /api/questions/exam/{exam_id}
Authorization: Bearer <token>

Response (200):
{
  "exam_id": 1,
  "total_questions": 120,
  "questions": [
    {
      "id": 1,
      "question_text": "What is 5 + 3?",
      "option_a": "8",
      "option_b": "9",
      "option_c": "7",
      "option_d": "6",
      "marks": 1,
      "negative_marks": 0.25,
      "topic": "Arithmetic"
    }
  ]
}
```

### 2. Add Question (Admin Only)
```
POST /api/questions
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "exam_id": 1,
  "question_text": "What is 5 + 3?",
  "option_a": "8",
  "option_b": "9",
  "option_c": "7",
  "option_d": "6",
  "correct_answer": "a",
  "explanation": "5 + 3 = 8",
  "difficulty": "Easy",
  "topic": "Arithmetic",
  "section": "Quantitative",
  "marks": 1,
  "negative_marks": 0.25
}

Response (201):
{
  "id": 1,
  "exam_id": 1,
  ...
}
```

---

## Result Endpoints

### 1. Submit Test
```
POST /api/results/submit
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "exam_id": 1,
  "answers": [
    {
      "question_id": 1,
      "selected_answer": "a",
      "time_spent": 45
    },
    {
      "question_id": 2,
      "selected_answer": null,
      "time_spent": 0
    }
  ],
  "total_time": 3600
}

Response (201):
{
  "id": 1,
  "exam_id": 1,
  "score": 95.5,
  "accuracy": 87.5,
  "speed": 2.0,
  "correct_answers": 105,
  "wrong_answers": 12,
  "unanswered": 3,
  "rank": 45
}
```

### 2. Get Result Details
```
GET /api/results/{result_id}
Authorization: Bearer <token>

Response (200):
{
  "id": 1,
  "exam_id": 1,
  "score": 95.5,
  "accuracy": 87.5,
  "speed": 2.0,
  "correct_answers": 105,
  "wrong_answers": 12,
  "unanswered": 3,
  "rank": 45,
  "submitted_at": "2024-01-15T14:30:00Z",
  "answers": [
    {
      "question_id": 1,
      "question_text": "What is 5 + 3?",
      "selected_answer": "a",
      "correct_answer": "a",
      "is_correct": true,
      "time_spent": 45
    }
  ]
}
```

### 3. Get User Results
```
GET /api/results/user?skip=0&limit=20
Authorization: Bearer <token>

Response (200):
{
  "total": 15,
  "results": [
    {
      "id": 1,
      "exam_id": 1,
      "score": 95.5,
      "accuracy": 87.5,
      "submitted_at": "2024-01-15T14:30:00Z"
    }
  ]
}
```

---

## AI Endpoints

### 1. Doubt Solver
```
POST /api/ai/doubt-solver
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request:
- image: <image file>
- query: "How to solve this step by step?"

Response (200):
{
  "id": 1,
  "question_text": "What is 5 + 3?",
  "steps": [
    "Step 1: We need to add 5 and 3",
    "Step 2: 5 + 3 = 8"
  ],
  "answer": "8",
  "confidence": 0.95
}
```

### 2. Get AI Recommendations
```
GET /api/ai/recommendations
Authorization: Bearer <token>

Response (200):
{
  "weak_topics": [
    {
      "topic": "Quadratic Equations",
      "weak_area": true,
      "accuracy": 35,
      "recommended_questions": 20
    }
  ],
  "strengths": [
    {
      "topic": "Arithmetic",
      "weak_area": false,
      "accuracy": 92,
      "recommended_questions": 5
    }
  ],
  "next_test_difficulty": "Medium",
  "study_plan": [
    "Focus on Quadratic Equations",
    "Practice 20 hard questions",
    "Review formulas"
  ]
}
```

---

## Analytics Endpoints

### 1. Get User Dashboard
```
GET /api/analytics/dashboard
Authorization: Bearer <token>

Response (200):
{
  "total_exams_taken": 15,
  "average_accuracy": 78.5,
  "average_speed": 1.8,
  "current_rank": 145,
  "current_streak": 7,
  "total_xp": 2450,
  "performance_by_exam_type": [
    {
      "exam_type": "PO",
      "accuracy": 82,
      "exams_taken": 5
    }
  ]
}
```

### 2. Get Leaderboard
```
GET /api/analytics/leaderboard?exam_type=PO&period=weekly
Authorization: Bearer <token>

Response (200):
{
  "period": "weekly",
  "exam_type": "PO",
  "leaderboard": [
    {
      "rank": 1,
      "user_name": "Raj Kumar",
      "score": 195,
      "accuracy": 92
    }
  ]
}
```

---

## Error Responses

### 400 - Bad Request
```json
{
  "detail": "Invalid request parameters",
  "error_code": "BAD_REQUEST"
}
```

### 401 - Unauthorized
```json
{
  "detail": "Invalid or expired token",
  "error_code": "UNAUTHORIZED"
}
```

### 403 - Forbidden
```json
{
  "detail": "You don't have permission to access this resource",
  "error_code": "FORBIDDEN"
}
```

### 404 - Not Found
```json
{
  "detail": "Resource not found",
  "error_code": "NOT_FOUND"
}
```

### 500 - Internal Server Error
```json
{
  "detail": "Internal server error",
  "error_code": "INTERNAL_ERROR"
}
```

---

## Rate Limiting

- **Default**: 100 requests per minute
- **Sensitive endpoints**: 10 requests per minute
- **Header**: `X-RateLimit-Remaining`

---

## Pagination

All list endpoints support pagination:
- `skip`: Offset (default: 0)
- `limit`: Number of items (default: 10, max: 100)

---

## Filtering & Sorting

### Example: Filter exams by type and difficulty
```
GET /api/exams?exam_type=PO&difficulty=Hard&sort_by=created_at&order=desc
```

Supported filters:
- `exam_type`: PO, Clerk, CGL, Railway, etc.
- `difficulty`: Easy, Medium, Hard
- `topic`: Arithmetic, Reasoning, English, etc.
