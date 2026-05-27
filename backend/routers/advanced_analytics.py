"""
Advanced Analytics Routes for ExamAce
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from database import get_db
from models import Result, Question, User, UserAnswer, Exam
from dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/analytics", tags=["Advanced Analytics"])


@router.get("/topics/{user_id}")
async def analyze_by_topics(
    user_id: int,
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    """
    Analyze user performance by topic/category
    Returns strength and weakness areas
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get all user answers with question details
        user_answers = db.query(
            Question.topic,
            func.count(UserAnswer.id).label('total_attempts'),
            func.sum(
                (UserAnswer.selected_answer == Question.correct_answer).cast(int)
            ).label('correct_count')
        ).join(UserAnswer, Question.id == UserAnswer.question_id).join(
            Result, UserAnswer.result_id == Result.id
        ).filter(
            Result.user_id == user_id,
            Question.topic.isnot(None)
        ).group_by(Question.topic).all()

        topic_analysis = []
        for topic, total, correct in user_answers:
            accuracy = (correct / total * 100) if total > 0 else 0
            topic_analysis.append({
                "topic": topic,
                "total_questions": total,
                "correct_answers": correct,
                "accuracy": round(accuracy, 2),
                "status": "Strong" if accuracy >= 75 else "Moderate" if accuracy >= 50 else "Weak"
            })

        # Sort by accuracy
        topic_analysis.sort(key=lambda x: x['accuracy'])

        return {
            "user_id": user_id,
            "user_name": user.name,
            "total_topics": len(topic_analysis),
            "strongest_topics": sorted(topic_analysis, key=lambda x: x['accuracy'], reverse=True)[:3],
            "weakest_topics": topic_analysis[:3],
            "all_topics": topic_analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance-trends/{user_id}")
async def get_performance_trends(
    user_id: int,
    days: int = Query(30),
    db: Session = Depends(get_db)
):
    """
    Get performance trends over time
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        start_date = datetime.utcnow() - timedelta(days=days)

        # Get daily performance
        daily_stats = db.query(
            func.date(Result.submitted_at).label('date'),
            func.count(Result.id).label('exams_taken'),
            func.avg(Result.accuracy).label('avg_accuracy'),
            func.avg(Result.score).label('avg_score')
        ).filter(
            Result.user_id == user_id,
            Result.submitted_at >= start_date
        ).group_by(func.date(Result.submitted_at)).order_by(
            func.date(Result.submitted_at)
        ).all()

        trend_data = []
        for date, exams, accuracy, score in daily_stats:
            trend_data.append({
                "date": str(date),
                "exams_taken": exams,
                "avg_accuracy": round(float(accuracy), 2) if accuracy else 0,
                "avg_score": round(float(score), 2) if score else 0
            })

        # Calculate trend
        if len(trend_data) > 1:
            first_accuracy = float(trend_data[0]['avg_accuracy'])
            last_accuracy = float(trend_data[-1]['avg_accuracy'])
            trend_direction = "improving" if last_accuracy > first_accuracy else "declining" if last_accuracy < first_accuracy else "stable"
        else:
            trend_direction = "insufficient_data"

        return {
            "user_id": user_id,
            "period_days": days,
            "total_exams": sum(d['exams_taken'] for d in trend_data),
            "trend_direction": trend_direction,
            "trend_data": trend_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comparison/{user_id}")
async def compare_with_peers(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Compare user's performance with peers
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get user's stats
        user_results = db.query(Result).filter(Result.user_id == user_id).all()
        if not user_results:
            return {
                "user_id": user_id,
                "message": "No exam data found for comparison"
            }

        user_avg_accuracy = sum(r.accuracy for r in user_results) / len(user_results)
        user_avg_score = sum(float(r.score) for r in user_results) / len(user_results)

        # Get global stats
        all_results = db.query(Result).all()
        if not all_results:
            return {
                "user_id": user_id,
                "message": "Insufficient peer data"
            }

        global_avg_accuracy = sum(r.accuracy for r in all_results) / len(all_results)
        global_avg_score = sum(float(r.score) for r in all_results) / len(all_results)

        # Calculate percentile
        better_performers = len([r for r in all_results if sum(
            float(rr.accuracy) for rr in db.query(Result).filter(
                Result.user_id == r.user_id
            ).all()
        ) / len([x for x in db.query(Result).filter(Result.user_id == r.user_id).all()]) > user_avg_accuracy])
        
        percentile = (better_performers / len(set(r.user_id for r in all_results))) * 100

        return {
            "user_id": user_id,
            "user_metrics": {
                "avg_accuracy": round(user_avg_accuracy, 2),
                "avg_score": round(user_avg_score, 2),
                "total_exams": len(user_results)
            },
            "global_metrics": {
                "avg_accuracy": round(global_avg_accuracy, 2),
                "avg_score": round(global_avg_score, 2),
                "total_users": len(set(r.user_id for r in all_results))
            },
            "comparison": {
                "accuracy_vs_global": round(user_avg_accuracy - global_avg_accuracy, 2),
                "score_vs_global": round(user_avg_score - global_avg_score, 2),
                "percentile": round(percentile, 2)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/difficulty-analysis/{user_id}")
async def analyze_by_difficulty(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Analyze performance by question difficulty
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        difficulties = ["Easy", "Medium", "Hard"]
        analysis = {}

        for difficulty in difficulties:
            answers = db.query(UserAnswer).join(
                Question, UserAnswer.question_id == Question.id
            ).join(
                Result, UserAnswer.result_id == Result.id
            ).filter(
                Result.user_id == user_id,
                Question.difficulty == difficulty
            ).all()

            if answers:
                correct = sum(1 for a in answers if a.selected_answer == a.question.correct_answer)
                accuracy = (correct / len(answers)) * 100
                analysis[difficulty] = {
                    "total_questions": len(answers),
                    "correct_answers": correct,
                    "accuracy": round(accuracy, 2),
                    "time_per_question": "N/A"
                }
            else:
                analysis[difficulty] = {
                    "total_questions": 0,
                    "correct_answers": 0,
                    "accuracy": 0,
                    "time_per_question": "N/A"
                }

        return {
            "user_id": user_id,
            "difficulty_analysis": analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/section-wise/{exam_id}/{user_id}")
async def analyze_by_section(
    exam_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Analyze performance by section within an exam
    """
    try:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get result for this exam
        result = db.query(Result).filter(
            and_(Result.exam_id == exam_id, Result.user_id == user_id)
        ).first()

        if not result:
            return {
                "exam_id": exam_id,
                "user_id": user_id,
                "message": "User hasn't taken this exam"
            }

        # Get sections
        sections = db.query(Question.section).filter(
            Question.exam_id == exam_id,
            Question.section.isnot(None)
        ).distinct().all()

        section_analysis = {}
        for section_tuple in sections:
            section = section_tuple[0]
            
            answers = db.query(UserAnswer).join(
                Question, UserAnswer.question_id == Question.id
            ).filter(
                UserAnswer.result_id == result.id,
                Question.section == section
            ).all()

            if answers:
                correct = sum(1 for a in answers if a.selected_answer == a.question.correct_answer)
                accuracy = (correct / len(answers)) * 100
                section_analysis[section] = {
                    "total_questions": len(answers),
                    "correct_answers": correct,
                    "accuracy": round(accuracy, 2),
                    "max_marks": sum(q.marks for q in db.query(Question).filter(
                        Question.exam_id == exam_id,
                        Question.section == section
                    ).all()) if answers else 0
                }

        return {
            "exam_id": exam_id,
            "exam_title": exam.title,
            "user_id": user_id,
            "section_analysis": section_analysis,
            "overall_accuracy": round(result.accuracy, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/time-analysis/{user_id}")
async def analyze_time_management(
    user_id: int,
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    """
    Analyze time management across exams
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        results = db.query(Result).filter(
            Result.user_id == user_id
        ).order_by(Result.submitted_at.desc()).limit(limit).all()

        time_analysis = []
        for result in results:
            exam = db.query(Exam).filter(Exam.id == result.exam_id).first()
            allocated_time = exam.duration * 60  # Convert to seconds
            time_utilization = (result.time_taken / allocated_time) * 100

            time_analysis.append({
                "exam_title": exam.title,
                "allocated_time_minutes": exam.duration,
                "actual_time_minutes": result.time_taken // 60,
                "time_utilization_percent": round(time_utilization, 2),
                "efficiency": "High" if time_utilization < 80 else "Moderate" if time_utilization < 95 else "Low",
                "accuracy": round(result.accuracy, 2)
            })

        avg_utilization = sum(a['time_utilization_percent'] for a in time_analysis) / len(time_analysis) if time_analysis else 0

        return {
            "user_id": user_id,
            "avg_time_utilization": round(avg_utilization, 2),
            "recent_exams": time_analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
