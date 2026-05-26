"""
Exam Management API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Exam, Question, User
from schemas import ExamCreate, ExamUpdate, ExamResponse
from dependencies import get_current_user

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.post("", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
async def create_exam(
    exam_data: ExamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new exam (Admin/Instructor only)
    """
    # Check if user is admin or instructor
    if current_user.role not in ["admin", "instructor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or instructor can create exams"
        )
    
    new_exam = Exam(
        title=exam_data.title,
        description=exam_data.description,
        duration=exam_data.duration,
        total_marks=exam_data.total_marks,
        exam_type=exam_data.exam_type,
        difficulty=exam_data.difficulty,
        sections=exam_data.sections,
        created_by=current_user.id
    )
    
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    
    return new_exam


@router.get("", response_model=list[ExamResponse])
async def list_exams(
    exam_type: str = None,
    difficulty: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all published exams with optional filters
    """
    query = db.query(Exam).filter(Exam.is_published == True)
    
    if exam_type:
        query = query.filter(Exam.exam_type == exam_type)
    
    if difficulty:
        query = query.filter(Exam.difficulty == difficulty)
    
    exams = query.offset(skip).limit(limit).all()
    
    return exams


@router.get("/{exam_id}", response_model=ExamResponse)
async def get_exam(
    exam_id: int,
    db: Session = Depends(get_db)
):
    """
    Get exam details by ID
    """
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.is_published == True).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    return exam


@router.put("/{exam_id}", response_model=ExamResponse)
async def update_exam(
    exam_id: int,
    exam_data: ExamUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update exam details (Admin/Creator only)
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Check if user is creator or admin
    if exam.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this exam"
        )
    
    # Update fields if provided
    if exam_data.title is not None:
        exam.title = exam_data.title
    if exam_data.description is not None:
        exam.description = exam_data.description
    if exam_data.duration is not None:
        exam.duration = exam_data.duration
    if exam_data.total_marks is not None:
        exam.total_marks = exam_data.total_marks
    if exam_data.difficulty is not None:
        exam.difficulty = exam_data.difficulty
    if exam_data.is_published is not None:
        exam.is_published = exam_data.is_published
    
    db.commit()
    db.refresh(exam)
    
    return exam


@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exam(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete exam (Admin/Creator only)
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Check if user is creator or admin
    if exam.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this exam"
        )
    
    db.delete(exam)
    db.commit()


@router.get("/{exam_id}/stats")
async def get_exam_stats(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get exam statistics (creator/admin only)
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Check if user is creator or admin
    if exam.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this exam's stats"
        )
    
    # Get statistics
    total_questions = db.query(Question).filter(Question.exam_id == exam_id).count()
    
    stats = {
        "exam_id": exam.id,
        "title": exam.title,
        "total_questions": total_questions,
        "duration": exam.duration,
        "total_marks": exam.total_marks,
        "is_published": exam.is_published
    }
    
    return stats
