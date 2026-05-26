-- ExamAce Database Schema
-- PostgreSQL Schema for Competitive Exam Platform

-- Users Table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'student', -- student, admin, instructor
  phone VARCHAR(20),
  profile_image VARCHAR(255),
  bio TEXT,
  city VARCHAR(100),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exams Table
CREATE TABLE exams (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  duration INTEGER NOT NULL, -- in minutes
  total_marks INTEGER NOT NULL,
  exam_type VARCHAR(50) NOT NULL, -- PO, Clerk, CGL, Railway, etc.
  difficulty VARCHAR(20) DEFAULT 'Medium', -- Easy, Medium, Hard
  sections INTEGER DEFAULT 3, -- Number of sections
  is_published BOOLEAN DEFAULT FALSE,
  created_by INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions Table
CREATE TABLE questions (
  id SERIAL PRIMARY KEY,
  exam_id INTEGER NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
  question_text TEXT NOT NULL,
  option_a VARCHAR(500) NOT NULL,
  option_b VARCHAR(500) NOT NULL,
  option_c VARCHAR(500) NOT NULL,
  option_d VARCHAR(500) NOT NULL,
  correct_answer VARCHAR(1) NOT NULL CHECK (correct_answer IN ('a', 'b', 'c', 'd')),
  explanation TEXT,
  difficulty VARCHAR(20) DEFAULT 'Medium',
  topic VARCHAR(100), -- Quant, Reasoning, English, GA, etc.
  section VARCHAR(50), -- For section-wise organization
  marks INTEGER DEFAULT 1,
  negative_marks DECIMAL(3,2) DEFAULT 0.25,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Results Table
CREATE TABLE results (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  exam_id INTEGER NOT NULL REFERENCES exams(id),
  score DECIMAL(6,2),
  accuracy DECIMAL(5,2), -- Percentage
  speed DECIMAL(5,2), -- Questions per minute
  correct_answers INTEGER DEFAULT 0,
  wrong_answers INTEGER DEFAULT 0,
  unanswered INTEGER DEFAULT 0,
  time_taken INTEGER, -- in seconds
  rank INTEGER,
  is_submitted BOOLEAN DEFAULT TRUE,
  started_at TIMESTAMP,
  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Answers Table (for tracking each answer)
CREATE TABLE user_answers (
  id SERIAL PRIMARY KEY,
  result_id INTEGER NOT NULL REFERENCES results(id) ON DELETE CASCADE,
  question_id INTEGER NOT NULL REFERENCES questions(id),
  selected_answer VARCHAR(1),
  is_correct BOOLEAN,
  time_spent INTEGER, -- seconds spent on question
  is_reviewed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Performance Table (for analytics)
CREATE TABLE user_performance (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  exam_type VARCHAR(50), -- PO, Clerk, etc.
  topic VARCHAR(100),
  total_questions INTEGER DEFAULT 0,
  correct_answers INTEGER DEFAULT 0,
  accuracy DECIMAL(5,2),
  average_speed DECIMAL(5,2),
  level_attempted VARCHAR(20), -- Easy, Medium, Hard
  last_attempted TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Gamification Table
CREATE TABLE gamification (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  total_xp INTEGER DEFAULT 0,
  current_streak INTEGER DEFAULT 0,
  max_streak INTEGER DEFAULT 0,
  badges TEXT, -- JSON format
  total_exams_taken INTEGER DEFAULT 0,
  rank_in_leaderboard INTEGER,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Leaderboard Table (Daily)
CREATE TABLE leaderboard (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  score DECIMAL(6,2),
  rank INTEGER,
  exam_type VARCHAR(50),
  UNIQUE(user_id, date, exam_type)
);

-- AI Recommendations Table
CREATE TABLE ai_recommendations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  topic VARCHAR(100),
  weak_area BOOLEAN, -- If true, this is a weak area
  difficulty_level VARCHAR(20),
  recommended_questions INTEGER,
  recommendation_text TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doubt Solver Sessions Table
CREATE TABLE doubt_solver_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  question_id INTEGER REFERENCES questions(id),
  image_url VARCHAR(255),
  query_text TEXT,
  ai_response TEXT,
  confidence_score DECIMAL(3,2),
  is_helpful BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes for better performance
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
