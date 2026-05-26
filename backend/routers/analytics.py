"""
Performance Analytics API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Result, UserAnswer, Question, User, UserPerformance
from schemas import PerformanceResponse
from dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard statistics for user
    """
    # Total exams taken
    total_exams = db.query(Result).filter(Result.user_id == current_user.id).count()
    
    # Average accuracy (last 10 exams)
    recent_results = db.query(Result).filter(
        Result.user_id == current_user.id
    ).order_by(Result.submitted_at.desc()).limit(10).all()
    
    avg_accuracy = 0
    if recent_results:
        avg_accuracy = sum(r.accuracy for r in recent_results) / len(recent_results)
    
    # Average speed (last 10 exams)
    avg_speed = 0
    if recent_results:
        avg_speed = sum(r.speed for r in recent_results) / len(recent_results)
    
    # Best score
    best_result = db.query(Result).filter(
        Result.user_id == current_user.id
    ).order_by(Result.score.desc()).first()
    
    best_score = float(best_result.score) if best_result else 0
    
    # Last result
    last_result = db.query(Result).filter(
        Result.user_id == current_user.id
    ).order_by(Result.submitted_at.desc()).first()
    
    last_result_time = last_result.submitted_at if last_result else None
    
    # Current rank (overall)
    user_rank = db.query(func.count(func.distinct(Result.user_id))).filter(
        Result.score > (best_score if best_result else 0)
    ).scalar() + 1
    
    return {
        "total_exams_taken": total_exams,
        "average_accuracy": round(float(avg_accuracy), 2),
        "average_speed": round(float(avg_speed), 2),
        "best_score": best_score,
        "current_rank": user_rank,
        "last_exam_time": last_result_time
    }


@router.get("/performance-by-topic")
async def get_performance_by_topic(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get performance metrics grouped by topic
    """
    # Get all user answers with question details
    answers = db.query(UserAnswer, Question).join(
        Question, UserAnswer.question_id == Question.id
    ).join(
        Result, UserAnswer.result_id == Result.id
    ).filter(
        Result.user_id == current_user.id
    ).all()
    
    # Group by topic
    topic_stats = {}
    for answer, question in answers:
        topic = question.topic or "General"
        
        if topic not in topic_stats:
            topic_stats[topic] = {
                "total": 0,
                "correct": 0,
                "wrong": 0,
                "accuracy": 0
            }
        
        topic_stats[topic]["total"] += 1
        if answer.is_correct:
            topic_stats[topic]["correct"] += 1
        else:
            topic_stats[topic]["wrong"] += 1
    
    # Calculate accuracy for each topic
    result = []
    for topic, stats in topic_stats.items():
        if stats["total"] > 0:
            accuracy = (stats["correct"] / stats["total"]) * 100
            result.append({
                "topic": topic,
                "total_questions": stats["total"],
                "correct_answers": stats["correct"],
                "wrong_answers": stats["wrong"],
                "accuracy": round(accuracy, 2)
            })
    
    # Sort by accuracy (ascending - weakest first)
    result.sort(key=lambda x: x["accuracy"])
    
    return result


@router.get("/weak-areas")
async def get_weak_areas(
    current_user: User = Depends(get_current_user),
    threshold: float = 60.0,
    db: Session = Depends(get_db)
):
    """
    Get topics where accuracy is below threshold (weak areas)
    Helps identify what to study next
    """
    performance_data = await get_performance_by_topic(current_user, db)
    
    weak_areas = [
        topic for topic in performance_data
        if topic["accuracy"] < threshold
    ]
    
    # Add recommendations
    recommendations = []
    for area in weak_areas:
        topic = area["topic"]
        accuracy = area["accuracy"]
        
        if accuracy < 40:
            recommendation = "❌ Critical: Focus heavily on this topic"
        elif accuracy < 50:
            recommendation = "⚠️ Warning: Significant improvement needed"
        elif accuracy < 60:
            recommendation = "📚 Practice more questions on this topic"
        
        recommendations.append({
            **area,
            "recommendation": recommendation,
            "priority": "High" if accuracy < 40 else "Medium"
        })
    
    return {
        "weak_areas": recommendations,
        "total_weak_areas": len(recommendations),
        "strong_areas_count": len(performance_data) - len(recommendations)
    }


@router.get("/strong-areas")
async def get_strong_areas(
    current_user: User = Depends(get_current_user),
    threshold: float = 75.0,
    db: Session = Depends(get_db)
):
    """
    Get topics where accuracy is above threshold (strong areas)
    """
    performance_data = await get_performance_by_topic(current_user, db)
    
    strong_areas = [
        topic for topic in performance_data
        if topic["accuracy"] >= threshold
    ]
    
    return {
        "strong_areas": strong_areas,
        "total_strong_areas": len(strong_areas)
    }


@router.get("/score-trend")
async def get_score_trend(
    current_user: User = Depends(get_current_user),
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get score progression over time (trend analysis)
    """
    # Get results from last X days
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    results = db.query(Result).filter(
        Result.user_id == current_user.id,
        Result.submitted_at >= cutoff_date
    ).order_by(Result.submitted_at).all()
    
    trend = [
        {
            "date": r.submitted_at.strftime("%Y-%m-%d"),
            "score": float(r.score),
            "accuracy": float(r.accuracy),
            "speed": float(r.speed),
            "exam_type": "Unknown"  # Can be populated from Exam table
        }
        for r in results
    ]
    
    # Calculate trend metrics
    if trend:
        first_score = trend[0]["score"]
        last_score = trend[-1]["score"]
        improvement = last_score - first_score
        
        return {
            "trend_data": trend,
            "total_exams": len(trend),
            "first_score": first_score,
            "last_score": last_score,
            "improvement": round(improvement, 2),
            "trend_direction": "📈 Improving" if improvement > 0 else "📉 Declining" if improvement < 0 else "➡️ Stable",
            "average_score": round(sum(t["score"] for t in trend) / len(trend), 2)
        }
    
    return {
        "trend_data": [],
        "total_exams": 0,
        "message": "Not enough data for trend analysis"
    }


@router.get("/accuracy-vs-speed")
async def get_accuracy_vs_speed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze trade-off between accuracy and speed
    """
    results = db.query(Result).filter(
        Result.user_id == current_user.id
    ).order_by(Result.submitted_at.desc()).limit(20).all()
    
    if not results:
        return {"message": "Not enough data", "data": []}
    
    data = [
        {
            "accuracy": float(r.accuracy),
            "speed": float(r.speed),
            "score": float(r.score),
            "date": r.submitted_at.strftime("%Y-%m-%d")
        }
        for r in results
    ]
    
    avg_accuracy = sum(d["accuracy"] for d in data) / len(data)
    avg_speed = sum(d["speed"] for d in data) / len(data)
    
    return {
        "data": data,
        "average_accuracy": round(avg_accuracy, 2),
        "average_speed": round(avg_speed, 2),
        "analysis": "Balance is key - high accuracy with decent speed is ideal"
    }


@router.get("/recommendations")
async def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized study recommendations based on performance
    """
    weak_areas_response = await get_weak_areas(current_user, threshold=65.0, db=db)
    accuracy_speed = await get_accuracy_vs_speed(current_user, db=db)
    score_trend = await get_score_trend(current_user, days=7, db=db)
    
    recommendations = []
    
    # Weak area recommendations
    if weak_areas_response["weak_areas"]:
        top_weak = weak_areas_response["weak_areas"][0]
        recommendations.append({
            "type": "Study Weak Topic",
            "priority": "High",
            "suggestion": f"Focus on {top_weak['topic']} (Current: {top_weak['accuracy']}% accuracy)",
            "action": f"Practice 10+ questions on {top_weak['topic']}"
        })
    
    # Speed recommendations
    if accuracy_speed["average_speed"] < 0.5:
        recommendations.append({
            "type": "Improve Speed",
            "priority": "Medium",
            "suggestion": "You're solving questions slowly. Practice timed drills.",
            "action": "Do 5-10 minute speed challenges"
        })
    
    # Accuracy recommendations
    if accuracy_speed["average_accuracy"] < 70:
        recommendations.append({
            "type": "Improve Accuracy",
            "priority": "High",
            "suggestion": "Your accuracy is below target. Review concepts.",
            "action": "Study weak topics before attempting more tests"
        })
    
    # Consistency recommendations
    if score_trend.get("trend_direction") == "📉 Declining":
        recommendations.append({
            "type": "Performance Declining",
            "priority": "High",
            "suggestion": "Your recent scores are declining. Take a break and review.",
            "action": "Revisit fundamental concepts"
        })
    
    return {
        "recommendations": recommendations,
        "total_recommendations": len(recommendations)
    }


@router.get("/exam-type-performance")
async def get_exam_type_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get performance broken down by exam type (IBPS, SBI, SSC, etc.)
    """
    from models import Exam
    
    results = db.query(Result, Exam).join(
        Exam, Result.exam_id == Exam.id
    ).filter(
        Result.user_id == current_user.id
    ).all()
    
    exam_stats = {}
    for result, exam in results:
        exam_type = exam.exam_type
        
        if exam_type not in exam_stats:
            exam_stats[exam_type] = {
                "total": 0,
                "total_score": 0,
                "best_score": 0,
                "average_accuracy": 0,
                "scores": []
            }
        
        exam_stats[exam_type]["total"] += 1
        exam_stats[exam_type]["total_score"] += float(result.score)
        exam_stats[exam_type]["best_score"] = max(
            exam_stats[exam_type]["best_score"],
            float(result.score)
        )
        exam_stats[exam_type]["scores"].append(float(result.accuracy))
    
    # Calculate averages
    result = []
    for exam_type, stats in exam_stats.items():
        avg_score = stats["total_score"] / stats["total"] if stats["total"] > 0 else 0
        avg_accuracy = sum(stats["scores"]) / len(stats["scores"]) if stats["scores"] else 0
        
        result.append({
            "exam_type": exam_type,
            "total_exams": stats["total"],
            "average_score": round(avg_score, 2),
            "best_score": stats["best_score"],
            "average_accuracy": round(avg_accuracy, 2)
        })
    
    result.sort(key=lambda x: x["average_score"], reverse=True)
    
    return {
        "exam_type_performance": result,
        "total_exam_types": len(result)
    }


@router.get("/study-suggestions")
async def get_study_suggestions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed study plan based on performance analysis
    """
    weak_areas = await get_weak_areas(current_user, threshold=65.0, db=db)
    strong_areas = await get_strong_areas(current_user, threshold=75.0, db=db)
    
    study_plan = []
    
    # Phase 1: Weak areas
    if weak_areas["weak_areas"]:
        study_plan.append({
            "phase": 1,
            "name": "Focus on Weak Topics",
            "duration": "5-7 days",
            "topics": [a["topic"] for a in weak_areas["weak_areas"][:5]],
            "description": "Master the fundamentals of your weak areas"
        })
    
    # Phase 2: Medium areas
    medium_areas = []
    for area in weak_areas.get("weak_areas", []):
        if 60 <= area["accuracy"] < 75:
            medium_areas.append(area)
    
    if medium_areas:
        study_plan.append({
            "phase": 2,
            "name": "Strengthen Medium Areas",
            "duration": "3-5 days",
            "topics": [a["topic"] for a in medium_areas[:5]],
            "description": "Practice to improve from 60-75% to 75%+"
        })
    
    # Phase 3: Consolidation
    if strong_areas["strong_areas"]:
        study_plan.append({
            "phase": 3,
            "name": "Maintain Strong Topics",
            "duration": "2-3 days",
            "topics": [a["topic"] for a in strong_areas["strong_areas"]],
            "description": "Keep your strong areas sharp with occasional practice"
        })
    
    return {
        "study_plan": study_plan,
        "total_phases": len(study_plan)
    }
