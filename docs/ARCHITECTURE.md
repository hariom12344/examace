# ExamAce Architecture & System Design

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  React SPA (Vite)                                              │
│  - Dashboard                                                    │
│  - Exam Module                                                  │
│  - Analytics                                                    │
│  - Admin Panel                                                  │
└─────────────┬───────────────────────────────────────────────────┘
              │ HTTP/HTTPS + WebSocket
              │
┌─────────────▼───────────────────────────────────────────────────┐
│                    API GATEWAY LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  CORS Middleware                                               │
│  Authentication Middleware                                     │
│  Rate Limiting                                                 │
└─────────────┬───────────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────────┐
│                    BACKEND API LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI Microservices                                         │
│  ├─ Auth Service                                               │
│  ├─ Exam Service                                               │
│  ├─ Question Service                                           │
│  ├─ Result Service                                             │
│  ├─ AI Service                                                 │
│  └─ Analytics Service                                          │
└─────────────┬───────────────────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼──┐  ┌──▼───┐  ┌──▼────┐
│ DB   │  │Cache │  │ OpenAI│
│(PG)  │  │Redis │  │ API   │
└──────┘  └──────┘  └───────┘
```

## Microservices Architecture

### 1. Auth Service
- **Responsibility**: User authentication, authorization, JWT management
- **Key Operations**:
  - User signup/login
  - Token generation & refresh
  - Password reset
  - OAuth integration

### 2. Exam Service
- **Responsibility**: Exam management, test creation, exam publishing
- **Key Operations**:
  - Create/update exams
  - Publish exams
  - List exams by type
  - Get exam details

### 3. Question Service
- **Responsibility**: Question bank management, retrieval, difficulty classification
- **Key Operations**:
  - Add/edit questions
  - Get random questions
  - Filter by topic/difficulty
  - Question statistics

### 4. Result Service
- **Responsibility**: Test submission, scoring, result storage
- **Key Operations**:
  - Submit test
  - Calculate score
  - Store results
  - Generate report

### 5. AI Service
- **Responsibility**: AI-powered features
- **Key Operations**:
  - Performance analysis
  - Weak topic detection
  - Doubt solving
  - Question recommendation
  - AI chatbot

### 6. Analytics Service
- **Responsibility**: User analytics, leaderboards, performance tracking
- **Key Operations**:
  - Calculate accuracy
  - Speed analysis
  - Rank prediction
  - Generate reports

## Data Flow Diagram

### Exam Taking Flow
```
1. User Opens Exam
   ├─ Frontend requests exam questions
   ├─ Backend validates user access
   └─ Returns questions (randomized)

2. User Answers Questions
   ├─ Each answer auto-saved
   ├─ Timer updates real-time
   └─ Review mechanism available

3. User Submits Test
   ├─ Final answer validation
   ├─ Score calculation
   ├─ Results stored in DB
   └─ Performance metrics computed

4. Results Display
   ├─ Score, Accuracy, Speed
   ├─ Topic-wise breakdown
   ├─ Comparison with peers
   └─ AI recommendations generated
```

### AI Recommendation Flow
```
1. User Takes Test
   ├─ Results stored in DB
   └─ Performance metrics calculated

2. Trigger AI Analysis
   ├─ Fetch user's performance history
   ├─ Identify weak topics
   └─ Analyze learning patterns

3. AI Processing
   ├─ OpenAI API call
   ├─ Generate recommendations
   └─ Suggest difficulty level

4. Store Recommendations
   ├─ Save in DB
   └─ Display on dashboard
```

## Database Design Patterns

### Normalization
- 3NF (Third Normal Form) applied
- Reduced redundancy
- Maintained data integrity

### Indexing Strategy
- Indexed on frequently queried columns
- Foreign keys for relationships
- Composite indexes for complex queries

### Example Query Optimization
```sql
-- Without index (slow)
SELECT * FROM results WHERE user_id = 1 AND exam_id = 5;

-- With indexes (fast)
CREATE INDEX idx_results_user_exam ON results(user_id, exam_id);
```

## Caching Strategy

### Redis Caching Layers
```
1. Session Cache (30 min)
   - User authentication tokens
   - Active exam sessions

2. Question Cache (1 day)
   - Frequently accessed questions
   - Question metadata

3. Leaderboard Cache (1 hour)
   - Top 100 users by exam type
   - Daily/weekly rankings

4. Result Cache (7 days)
   - Recent user results
   - Performance metrics
```

## Security Architecture

### Authentication Flow
```
1. User Login
   ├─ Email + Password
   └─ Validate credentials

2. Generate JWT
   ├─ Access Token (30 min)
   ├─ Refresh Token (7 days)
   └─ Store refresh token in Redis

3. API Requests
   ├─ Include JWT in header
   ├─ Validate on backend
   └─ Allow/Reject request

4. Token Refresh
   ├─ Use refresh token
   ├─ Generate new access token
   └─ Update Redis
```

### Data Protection
- Passwords hashed with bcrypt
- HTTPS enforced
- CORS enabled only for trusted origins
- Rate limiting on sensitive endpoints
- Input validation & sanitization

## Scalability Considerations

### Horizontal Scaling
```
Load Balancer
├─ Backend Instance 1
├─ Backend Instance 2
├─ Backend Instance 3
└─ Backend Instance N

Shared Services
├─ PostgreSQL (Primary/Replica)
├─ Redis Cluster
└─ OpenAI API
```

### Database Scaling
- Read replicas for analytics
- Partitioning by date for results
- Archive old data
- Connection pooling with PgBouncer

## Performance Metrics

### Target SLAs
- API Response Time: < 200ms
- Question Loading: < 500ms
- AI Response: < 5 seconds
- Database Query: < 100ms

### Monitoring
- Request/Response times
- Error rates
- Database performance
- Cache hit ratios
- User engagement metrics

## Deployment Strategy

### Development
- Local machine with Docker
- Hot reload for both frontend/backend

### Staging
- Docker Compose on staging server
- Mirror production environment

### Production
- Docker containers on Kubernetes
- Frontend on Vercel
- Backend on Railway
- Database on Supabase
- Redis on Redis Cloud
