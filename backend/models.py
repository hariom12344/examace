"""
SQLAlchemy Models for ExamAce
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="student")
    phone = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    exams = relationship("Exam", back_populates="creator")
    results = relationship("Result", back_populates="user")
    performance = relationship("UserPerformance", back_populates="user")
    gamification = relationship("Gamification", back_populates="user", uselist=False)

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(Integer, nullable=False)  # in minutes
    total_marks = Column(Integer, nullable=False)
    exam_type = Column(String, nullable=False, index=True)
    difficulty = Column(String, default="Medium")
    sections = Column(Integer, default=3)
    is_published = Column(Boolean, default=False)
    is_pyq = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="exams")
    questions = relationship("Question", back_populates="exam", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="exam")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(String(500), nullable=False)
    option_b = Column(String(500), nullable=False)
    option_c = Column(String(500), nullable=False)
    option_d = Column(String(500), nullable=False)
    correct_answer = Column(String(1), nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(String, default="Medium", index=True)
    topic = Column(String, nullable=True, index=True)
    section = Column(String, nullable=True)
    marks = Column(Integer, default=1)
    negative_marks = Column(Numeric(3, 2), default=0.25)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    exam = relationship("Exam", back_populates="questions")
    answers = relationship("UserAnswer", back_populates="question")

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    score = Column(Numeric(6, 2))
    accuracy = Column(Numeric(5, 2))
    speed = Column(Numeric(5, 2))
    correct_answers = Column(Integer, default=0)
    wrong_answers = Column(Integer, default=0)
    unanswered = Column(Integer, default=0)
    time_taken = Column(Integer)  # in seconds
    rank = Column(Integer, nullable=True)
    is_submitted = Column(Boolean, default=True)
    started_at = Column(DateTime, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="results")
    exam = relationship("Exam", back_populates="results")
    answers = relationship("UserAnswer", back_populates="result")

class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("results.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_answer = Column(String(1), nullable=True)
    is_correct = Column(Boolean, nullable=True)
    time_spent = Column(Integer)  # seconds
    is_reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    result = relationship("Result", back_populates="answers")
    question = relationship("Question", back_populates="answers")

class UserPerformance(Base):
    __tablename__ = "user_performance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exam_type = Column(String, nullable=True)
    topic = Column(String, nullable=True, index=True)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    accuracy = Column(Numeric(5, 2))
    average_speed = Column(Numeric(5, 2))
    level_attempted = Column(String)
    last_attempted = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="performance")

class Gamification(Base):
    __tablename__ = "gamification"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    total_xp = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    max_streak = Column(Integer, default=0)
    badges = Column(Text, nullable=True)  # JSON format
    total_exams_taken = Column(Integer, default=0)
    rank_in_leaderboard = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="gamification")

class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=datetime.utcnow, index=True)
    score = Column(Numeric(6, 2))
    rank = Column(Integer)
    exam_type = Column(String, nullable=True)
