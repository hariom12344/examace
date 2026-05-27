"""
Advanced Question Filtering Routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from database import get_db
from models import Question, Exam
from schemas import QuestionWithoutAnswer

router = APIRouter(prefix="/api/questions", tags=["Question Filtering"])


@router.get("/filter")
async def filter_questions(
    exam_id: int = Query(..., description="Exam ID"),
    category: str = Query(None, description="Filter by category/topic"),
    difficulty: str = Query(None, description="Filter by difficulty (Easy, Medium, Hard)"),
    section: str = Query(None, description="Filter by section"),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """
    Advanced question filtering by category, difficulty, and section
    """
    try:
        # Build filter conditions
        filters = [Question.exam_id == exam_id, Question.is_active == True]

        if category:
            filters.append(Question.topic.ilike(f"%{category}%"))
        if difficulty and difficulty in ["Easy", "Medium", "Hard"]:
            filters.append(Question.difficulty == difficulty)
        if section:
            filters.append(Question.section.ilike(f"%{section}%"))

        # Execute query
        questions = db.query(Question).filter(and_(*filters)).limit(limit).offset(offset).all()
        total_count = db.query(Question).filter(and_(*filters)).count()

        # Convert to response format (without showing correct answers)
        questions_data = []
        for q in questions:
            questions_data.append({
                "id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "section": q.section,
                "marks": q.marks
            })

        return {
            "questions": questions_data,
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "filters_applied": {
                "exam_id": exam_id,
                "category": category,
                "difficulty": difficulty,
                "section": section
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-difficulty/{exam_id}")
async def get_questions_by_difficulty(
    exam_id: int,
    db: Session = Depends(get_db)
):
    """
    Get questions grouped by difficulty level
    """
    try:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        difficulties = ["Easy", "Medium", "Hard"]
        result = {}

        for difficulty in difficulties:
            questions = db.query(Question).filter(
                Question.exam_id == exam_id,
                Question.difficulty == difficulty,
                Question.is_active == True
            ).all()

            result[difficulty] = {
                "count": len(questions),
                "percentage": round((len(questions) / max(
                    db.query(Question).filter(
                        Question.exam_id == exam_id,
                        Question.is_active == True
                    ).count(), 1)) * 100, 2),
                "sample_questions": [
                    {
                        "id": q.id,
                        "topic": q.topic,
                        "marks": q.marks
                    }
                    for q in questions[:3]  # Show first 3 as sample
                ]
            }

        return {
            "exam_id": exam_id,
            "exam_title": exam.title,
            "difficulty_breakdown": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-category/{exam_id}")
async def get_questions_by_category(
    exam_id: int,
    db: Session = Depends(get_db)
):
    """
    Get questions grouped by category/topic
    """
    try:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        # Get all unique topics
        topics = db.query(Question.topic).filter(
            Question.exam_id == exam_id,
            Question.is_active == True
        ).distinct().all()

        result = {}
        total_questions = db.query(Question).filter(
            Question.exam_id == exam_id,
            Question.is_active == True
        ).count()

        for topic_tuple in topics:
            topic = topic_tuple[0]
            if not topic:
                continue

            questions = db.query(Question).filter(
                Question.exam_id == exam_id,
                Question.topic == topic,
                Question.is_active == True
            ).all()

            result[topic] = {
                "count": len(questions),
                "percentage": round((len(questions) / max(total_questions, 1)) * 100, 2),
                "by_difficulty": {
                    "Easy": len([q for q in questions if q.difficulty == "Easy"]),
                    "Medium": len([q for q in questions if q.difficulty == "Medium"]),
                    "Hard": len([q for q in questions if q.difficulty == "Hard"])
                }
            }

        return {
            "exam_id": exam_id,
            "exam_title": exam.title,
            "total_questions": total_questions,
            "category_breakdown": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics/{exam_id}")
async def get_question_statistics(exam_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive question statistics for an exam
    """
    try:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        questions = db.query(Question).filter(
            Question.exam_id == exam_id,
            Question.is_active == True
        ).all()

        total_marks = sum(q.marks for q in questions)
        avg_marks = total_marks / len(questions) if questions else 0

        return {
            "exam_id": exam_id,
            "exam_title": exam.title,
            "total_questions": len(questions),
            "total_marks": total_marks,
            "avg_marks_per_question": round(avg_marks, 2),
            "difficulty_distribution": {
                "Easy": len([q for q in questions if q.difficulty == "Easy"]),
                "Medium": len([q for q in questions if q.difficulty == "Medium"]),
                "Hard": len([q for q in questions if q.difficulty == "Hard"])
            },
            "negative_marking": float(questions[0].negative_marks) if questions else 0,
            "sections": len(set(q.section for q in questions if q.section)),
            "topics": len(set(q.topic for q in questions if q.topic))
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
