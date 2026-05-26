# Database Schema Documentation

## Overview
ExamAce uses PostgreSQL as the primary database. The schema is designed for:
- Efficient querying
- Data integrity
- Scalability
- Analytics

## Core Tables

### Users Table
Stores user information and authentication details.

```sql
Table: users
- id (SERIAL PRIMARY KEY)
- email (VARCHAR UNIQUE NOT NULL)
- name (VARCHAR NOT NULL)
- password_hash (VARCHAR NOT NULL)
- role (VARCHAR) - student, admin, instructor
- phone (VARCHAR)
- profile_image (VARCHAR)
- bio (TEXT)
- city (VARCHAR)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### Exams Table
Stores exam information.

```sql
Table: exams
- id (SERIAL PRIMARY KEY)
- title (VARCHAR NOT NULL)
- description (TEXT)
- duration (INTEGER) - in minutes
- total_marks (INTEGER)
- exam_type (VARCHAR) - PO, Clerk, CGL, Railway, etc.
- difficulty (VARCHAR) - Easy, Medium, Hard
- sections (INTEGER) - Number of sections
- is_published (BOOLEAN)
- created_by (INTEGER FK → users.id)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### Questions Table
Stores all questions with their metadata.

```sql
Table: questions
- id (SERIAL PRIMARY KEY)
- exam_id (INTEGER FK → exams.id)
- question_text (TEXT NOT NULL)
- option_a (VARCHAR)
- option_b (VARCHAR)
- option_c (VARCHAR)
- option_d (VARCHAR)
- correct_answer (VARCHAR) - a, b, c, or d
- explanation (TEXT)
- difficulty (VARCHAR)
- topic (VARCHAR)
- section (VARCHAR)
- marks (INTEGER)
- negative_marks (DECIMAL)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
```

### Results Table
Stores test results for analytics.

```sql
Table: results
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER FK → users.id)
- exam_id (INTEGER FK → exams.id)
- score (DECIMAL)
- accuracy (DECIMAL) - Percentage
- speed (DECIMAL) - Questions per minute
- correct_answers (INTEGER)
- wrong_answers (INTEGER)
- unanswered (INTEGER)
- time_taken (INTEGER) - in seconds
- rank (INTEGER)
- is_submitted (BOOLEAN)
- started_at (TIMESTAMP)
- submitted_at (TIMESTAMP)
- created_at (TIMESTAMP)
```

### User Answers Table
Tracks each answer for detailed analysis.

```sql
Table: user_answers
- id (SERIAL PRIMARY KEY)
- result_id (INTEGER FK → results.id)
- question_id (INTEGER FK → questions.id)
- selected_answer (VARCHAR) - a, b, c, d, or null
- is_correct (BOOLEAN)
- time_spent (INTEGER) - seconds
- is_reviewed (BOOLEAN)
- created_at (TIMESTAMP)
```

### User Performance Table
Analytics and performance tracking.

```sql
Table: user_performance
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER FK → users.id)
- exam_type (VARCHAR)
- topic (VARCHAR)
- total_questions (INTEGER)
- correct_answers (INTEGER)
- accuracy (DECIMAL)
- average_speed (DECIMAL)
- level_attempted (VARCHAR)
- last_attempted (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### Gamification Table
Tracks achievements and rewards.

```sql
Table: gamification
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER UNIQUE FK → users.id)
- total_xp (INTEGER)
- current_streak (INTEGER)
- max_streak (INTEGER)
- badges (TEXT) - JSON format
- total_exams_taken (INTEGER)
- rank_in_leaderboard (INTEGER)
- updated_at (TIMESTAMP)
```

### Leaderboard Table
Daily rankings.

```sql
Table: leaderboard
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER FK → users.id)
- date (DATE)
- score (DECIMAL)
- rank (INTEGER)
- exam_type (VARCHAR)
```

### AI Recommendations Table
Stores AI-generated recommendations.

```sql
Table: ai_recommendations
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER FK → users.id)
- topic (VARCHAR)
- weak_area (BOOLEAN)
- difficulty_level (VARCHAR)
- recommended_questions (INTEGER)
- recommendation_text (TEXT)
- created_at (TIMESTAMP)
```

### Doubt Solver Sessions Table
Stores doubt solving interactions.

```sql
Table: doubt_solver_sessions
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER FK → users.id)
- question_id (INTEGER FK → questions.id)
- image_url (VARCHAR)
- query_text (TEXT)
- ai_response (TEXT)
- confidence_score (DECIMAL)
- is_helpful (BOOLEAN)
- created_at (TIMESTAMP)
```

## Relationships

```
users (1) ──→ (N) exams [created_by]
users (1) ──→ (N) results [user_id]
users (1) ──→ (N) user_performance [user_id]
users (1) ──→ (1) gamification [user_id]
users (1) ──→ (N) ai_recommendations [user_id]
users (1) ──→ (N) doubt_solver_sessions [user_id]

exams (1) ──→ (N) questions [exam_id]
exams (1) ──→ (N) results [exam_id]

questions (1) ──→ (N) user_answers [question_id]

results (1) ──→ (N) user_answers [result_id]
```

## Indexes

For performance optimization:

```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_exams_exam_type ON exams(exam_type);
CREATE INDEX idx_questions_exam_id ON questions(exam_id);
CREATE INDEX idx_questions_topic ON questions(topic);
CREATE INDEX idx_results_user_id ON results(user_id);
CREATE INDEX idx_results_exam_id ON results(exam_id);
CREATE INDEX idx_results_submitted_at ON results(submitted_at);
CREATE INDEX idx_user_answers_result_id ON user_answers(result_id);
CREATE INDEX idx_performance_user_id ON user_performance(user_id);
CREATE INDEX idx_performance_topic ON user_performance(topic);
CREATE INDEX idx_leaderboard_date_rank ON leaderboard(date, rank);
CREATE INDEX idx_doubt_sessions_user_id ON doubt_solver_sessions(user_id);
```

## Query Examples

### Get user's exam history
```sql
SELECT r.id, e.title, r.score, r.accuracy, r.submitted_at
FROM results r
JOIN exams e ON r.exam_id = e.id
WHERE r.user_id = $1
ORDER BY r.submitted_at DESC;
```

### Get weekly leaderboard
```sql
SELECT l.rank, u.name, l.score, l.exam_type
FROM leaderboard l
JOIN users u ON l.user_id = u.id
WHERE l.date = CURRENT_DATE
AND l.exam_type = $1
ORDER BY l.rank
LIMIT 100;
```

### Get user's weak topics
```sql
SELECT topic, accuracy, last_attempted
FROM user_performance
WHERE user_id = $1
AND accuracy < 60
ORDER BY accuracy ASC;
```

### Calculate exam statistics
```sql
SELECT
  e.title,
  COUNT(r.id) as total_attempts,
  AVG(r.accuracy) as avg_accuracy,
  AVG(r.score) as avg_score
FROM exams e
LEFT JOIN results r ON e.id = r.exam_id
WHERE e.exam_type = $1
GROUP BY e.id, e.title;
```
