"""
Leaderboard Router for ExamAce
Handles leaderboard rankings and statistics
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from database import get_db
from models import User, Result, Exam, UserPerformance

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


@router.get("/global")
async def get_global_leaderboard(
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """
    Get global leaderboard rankings
    """
    try:
        # Get top performers with average accuracy
        leaderboard = db.query(
            User.id,
            User.name,
            User.email,
            func.count(Result.id).label('exams_completed'),
            func.avg(Result.accuracy).label('avg_accuracy'),
            func.avg(Result.score).label('avg_score'),
            func.avg(Result.speed).label('avg_speed')
        ).outerjoin(Result, User.id == Result.user_id).group_by(User.id).order_by(
            desc(func.avg(Result.accuracy))
        ).limit(limit).offset(offset).all()

        # Add rank
        rankings = []
        for idx, entry in enumerate(leaderboard, 1):
            rankings.append({
                "rank": idx,
                "user_id": entry[0],
                "name": entry[1],
                "email": entry[2],
                "exams_completed": entry[3] or 0,
                "avg_accuracy": round(float(entry[4]) if entry[4] else 0, 2),
                "avg_score": round(float(entry[5]) if entry[5] else 0, 2),
                "avg_speed": round(float(entry[6]) if entry[6] else 0, 2)
            })

        return {
            "leaderboard": rankings,
            "total_count": len(leaderboard),
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exam/{exam_id}")
async def get_exam_leaderboard(
    exam_id: int,
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """
    Get leaderboard for a specific exam
    """
    try:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        # Get top performers for this exam
        results = db.query(
            User.id,
            User.name,
            Result.id,
            Result.score,
            Result.accuracy,
            Result.time_taken,
            Result.submitted_at
        ).join(Result, User.id == Result.user_id).filter(
            Result.exam_id == exam_id
        ).order_by(
            desc(Result.score),
            Result.time_taken  # Secondary sort: faster time is better
        ).limit(limit).all()

        leaderboard = []
        for idx, result in enumerate(results, 1):
            leaderboard.append({
                "rank": idx,
                "user_id": result[0],
                "name": result[1],
                "result_id": result[2],
                "score": round(float(result[3]), 2),
                "accuracy": round(float(result[4]), 2),
                "time_taken_seconds": result[5],
                "submitted_at": result[6].isoformat() if result[6] else None
            })

        return {
            "exam_id": exam_id,
            "exam_title": exam.title,
            "leaderboard": leaderboard,
            "total_participants": len(leaderboard)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/stats")
async def get_user_statistics(user_id: int, db: Session = Depends(get_db)):
    """
    Get detailed statistics for a user
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get all results for the user
        results = db.query(Result).filter(Result.user_id == user_id).all()

        if not results:
            return {
                "user_id": user_id,
                "name": user.name,
                "exams_completed": 0,
                "total_score": 0,
                "avg_accuracy": 0,
                "avg_speed": 0,
                "best_exam": None,
                "worst_exam": None,
                "consistency_score": 0
            }

        # Calculate statistics
        total_exams = len(results)
        total_score = sum(float(r.score) for r in results if r.score)
        avg_accuracy = sum(float(r.accuracy) for r in results if r.accuracy) / total_exams if results else 0
        avg_speed = sum(r.time_taken for r in results if r.time_taken) / total_exams if results else 0

        # Find best and worst exams
        best_result = max(results, key=lambda r: float(r.score) if r.score else 0)
        worst_result = min(results, key=lambda r: float(r.score) if r.score else 0)

        best_exam = db.query(Exam).filter(Exam.id == best_result.exam_id).first()
        worst_exam = db.query(Exam).filter(Exam.id == worst_result.exam_id).first()

        # Get global rank
        global_rank = db.query(func.count(User.id)).filter(
            User.id != user_id,
            func.avg(Result.accuracy) > avg_accuracy
        ).scalar() + 1

        return {
            "user_id": user_id,
            "name": user.name,
            "email": user.email,
            "exams_completed": total_exams,
            "total_score": round(total_score, 2),
            "avg_accuracy": round(avg_accuracy, 2),
            "avg_speed": round(avg_speed / 60, 2),  # Convert to minutes
            "best_exam": {
                "title": best_exam.title if best_exam else "N/A",
                "score": round(float(best_result.score), 2),
                "accuracy": round(float(best_result.accuracy), 2)
            },
            "worst_exam": {
                "title": worst_exam.title if worst_exam else "N/A",
                "score": round(float(worst_result.score), 2),
                "accuracy": round(float(worst_result.accuracy), 2)
            },
            "global_rank": global_rank,
            "member_since": user.created_at.isoformat() if user.created_at else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending")
async def get_trending_performers(
    days: int = Query(7),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    """
    Get trending performers in the last N days
    """
    try:
        from datetime import datetime, timedelta
        
        start_date = datetime.utcnow() - timedelta(days=days)

        trending = db.query(
            User.id,
            User.name,
            func.count(Result.id).label('recent_exams'),
            func.avg(Result.accuracy).label('recent_accuracy')
        ).join(Result, User.id == Result.user_id).filter(
            Result.submitted_at >= start_date
        ).group_by(User.id).order_by(
            desc(func.avg(Result.accuracy))
        ).limit(limit).all()

        leaderboard = []
        for idx, entry in enumerate(trending, 1):
            leaderboard.append({
                "rank": idx,
                "user_id": entry[0],
                "name": entry[1],
                "recent_exams": entry[2],
                "recent_accuracy": round(float(entry[3]) if entry[3] else 0, 2)
            })

        return {
            "period_days": days,
            "trending_performers": leaderboard,
            "total_active_users": len(leaderboard)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
