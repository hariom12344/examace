"""
Test Result Management API Routes
"""
import sys
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
from models import Result, UserAnswer, Question, Exam, User
from schemas import ResultSubmit, ResultResponse, ResultDetail
from dependencies import get_current_user
from datetime import datetime
from decimal import Decimal

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='result_debug.log')
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/results", tags=["Results"])

# Debug endpoint - test if Authorization header is received
@router.post("/test-auth-debug")
async def test_auth_debug(request: Request):
    """Test endpoint to debug Authorization header"""
    auth_header = request.headers.get("authorization")
    logger.info(f"[DEBUG-ENDPOINT] Authorization header received: {auth_header[:50] if auth_header else 'NONE'}")
    return {
        "auth_header_present": bool(auth_header),
        "auth_header_preview": auth_header[:30] if auth_header else None
    }

@router.post("", response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
async def submit_test(
    result_data: ResultSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit test answers and calculate results
    """
    logger.info(f"[RESULT DEBUG] submit_test called for user_id={current_user.id}, exam_id={result_data.exam_id}")
    
    # Check if exam exists
    exam = db.query(Exam).filter(Exam.id == result_data.exam_id, Exam.is_published == True).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Calculate results
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    total_score = Decimal("0")
    
    # Get all questions in the exam
    all_questions = db.query(Question).filter(
        Question.exam_id == result_data.exam_id,
        Question.is_active == True
    ).all()
    
    # Create a dict of questions by ID for easy lookup
    question_dict = {q.id: q for q in all_questions}
    
    # Track answered question IDs
    answered_ids = {ans.question_id for ans in result_data.answers}
    
    # Calculate score
    for answer in result_data.answers:
        question = question_dict.get(answer.question_id)
        if not question:
            continue
        
        is_correct = False
        if answer.selected_answer and answer.selected_answer.upper() == question.correct_answer.upper():
            is_correct = True
            correct_count += 1
            total_score += Decimal(str(question.marks))
        else:
            wrong_count += 1
            # Apply negative marking if answer is selected
            if answer.selected_answer:
                total_score -= Decimal(str(question.negative_marks))
    
    # Count unanswered questions
    unanswered_count = len(all_questions) - len(answered_ids)
    
    # Calculate accuracy
    total_answered = correct_count + wrong_count
    accuracy = Decimal("0")
    if total_answered > 0:
        accuracy = (Decimal(str(correct_count)) / Decimal(str(total_answered))) * Decimal("100")
    
    # Calculate speed (questions per minute)
    speed = Decimal("0")
    if result_data.total_time > 0:
        speed = (Decimal(str(total_answered)) / Decimal(str(result_data.total_time / 60)))
    
    # Create result record
    new_result = Result(
        user_id=current_user.id,
        exam_id=result_data.exam_id,
        score=total_score,
        accuracy=accuracy,
        speed=speed,
        correct_answers=correct_count,
        wrong_answers=wrong_count,
        unanswered=unanswered_count,
        time_taken=result_data.total_time,
        is_submitted=True,
        started_at=datetime.utcnow(),
        submitted_at=datetime.utcnow()
    )
    
    db.add(new_result)
    db.flush()  # Get the result ID
    
    # Store individual answers
    for answer in result_data.answers:
        question = question_dict.get(answer.question_id)
        if not question:
            continue
        
        is_correct = False
        if answer.selected_answer and answer.selected_answer.upper() == question.correct_answer.upper():
            is_correct = True
        
        user_answer = UserAnswer(
            result_id=new_result.id,
            question_id=answer.question_id,
            selected_answer=answer.selected_answer,
            is_correct=is_correct,
            time_spent=answer.time_spent
        )
        db.add(user_answer)
    
    db.commit()
    db.refresh(new_result)
    
    return new_result


@router.get("/{result_id}", response_model=ResultDetail)
async def get_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get result details with answers
    """
    result = db.query(Result).filter(Result.id == result_id).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    # Check if user is the owner or admin
    if result.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this result"
        )
    
    return result


@router.get("/exam/{exam_id}/my-result", response_model=ResultResponse)
async def get_my_exam_result(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's latest result for an exam
    """
    result = db.query(Result).filter(
        Result.exam_id == exam_id,
        Result.user_id == current_user.id
    ).order_by(Result.submitted_at.desc()).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No result found for this exam"
        )
    
    return result


@router.get("/user/history")
async def get_user_results(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get user's result history
    """
    results = db.query(Result).filter(
        Result.user_id == current_user.id
    ).order_by(Result.submitted_at.desc()).offset(skip).limit(limit).all()
    
    return results


@router.get("/exam/{exam_id}/leaderboard")
async def get_exam_leaderboard(
    exam_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get top scorers for an exam
    """
    # Check if exam exists
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Get top results
    top_results = db.query(Result, User).join(User).filter(
        Result.exam_id == exam_id,
        Result.is_submitted == True
    ).order_by(Result.score.desc()).limit(limit).all()
    
    leaderboard = []
    for idx, (result, user) in enumerate(top_results, 1):
        leaderboard.append({
            "rank": idx,
            "user_name": user.name,
            "score": float(result.score),
            "accuracy": float(result.accuracy),
            "time_taken": result.time_taken
        })
    
    return {
        "exam_id": exam_id,
        "exam_title": exam.title,
        "leaderboard": leaderboard
    }
