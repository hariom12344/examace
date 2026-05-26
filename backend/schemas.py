"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Auth Schemas
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class LoginResponse(UserResponse):
    access_token: str
    refresh_token: str
    expires_in: int

# Exam Schemas
class ExamCreate(BaseModel):
    title: str
    description: Optional[str] = None
    duration: int
    total_marks: int
    exam_type: str
    difficulty: Optional[str] = "Medium"
    sections: Optional[int] = 3

class ExamUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    total_marks: Optional[int] = None
    difficulty: Optional[str] = None
    is_published: Optional[bool] = None

class ExamResponse(ExamCreate):
    id: int
    is_published: bool
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Question Schemas
class QuestionCreate(BaseModel):
    exam_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: Optional[str] = "Medium"
    topic: Optional[str] = None
    section: Optional[str] = None
    marks: Optional[int] = 1
    negative_marks: Optional[float] = 0.25

class QuestionResponse(QuestionCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class QuestionWithoutAnswer(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    marks: int
    negative_marks: float
    topic: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Answer Schemas
class AnswerSubmit(BaseModel):
    question_id: int
    selected_answer: Optional[str] = None
    time_spent: int

class UserAnswerResponse(BaseModel):
    question_id: int
    selected_answer: Optional[str]
    is_correct: bool
    time_spent: int

    model_config = ConfigDict(from_attributes=True)

# Result Schemas
class ResultSubmit(BaseModel):
    exam_id: int
    answers: List[AnswerSubmit]
    total_time: int

class ResultResponse(BaseModel):
    id: int
    exam_id: int
    score: float
    accuracy: float
    speed: float
    correct_answers: int
    wrong_answers: int
    unanswered: int
    rank: Optional[int]
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ResultDetail(ResultResponse):
    answers: List[UserAnswerResponse]

# Performance Schemas
class PerformanceResponse(BaseModel):
    exam_type: str
    topic: str
    accuracy: float
    total_questions: int
    correct_answers: int
    last_attempted: datetime

    model_config = ConfigDict(from_attributes=True)

# Leaderboard Schemas
class LeaderboardEntry(BaseModel):
    rank: int
    user_name: str
    score: float
    accuracy: float

class LeaderboardResponse(BaseModel):
    period: str
    exam_type: str
    leaderboard: List[LeaderboardEntry]

# Analytics Schemas
class DashboardStats(BaseModel):
    total_exams_taken: int
    average_accuracy: float
    average_speed: float
    current_rank: int
    current_streak: int
    total_xp: int

# AI Schemas
class DoubSolverResponse(BaseModel):
    question_text: str
    steps: List[str]
    answer: str
    confidence: float

class RecommendationResponse(BaseModel):
    topic: str
    weak_area: bool
    accuracy: float
    recommended_questions: int
    difficulty_level: str

# Pagination
class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)
