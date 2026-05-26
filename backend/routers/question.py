"""
Question Management API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Question, Exam, User
from schemas import QuestionCreate, QuestionResponse, QuestionWithoutAnswer
from dependencies import get_current_user

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a question to an exam (Admin/Instructor only)
    """
    # Check if user is admin or instructor
    if current_user.role not in ["admin", "instructor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or instructor can create questions"
        )
    
    # Check if exam exists and user has permission
    exam = db.query(Exam).filter(Exam.id == question_data.exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Check if user is exam creator or admin
    if exam.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to add questions to this exam"
        )
    
    # Validate correct answer
    if question_data.correct_answer not in ["A", "B", "C", "D"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correct answer must be A, B, C, or D"
        )
    
    new_question = Question(
        exam_id=question_data.exam_id,
        question_text=question_data.question_text,
        option_a=question_data.option_a,
        option_b=question_data.option_b,
        option_c=question_data.option_c,
        option_d=question_data.option_d,
        correct_answer=question_data.correct_answer,
        explanation=question_data.explanation,
        difficulty=question_data.difficulty,
        topic=question_data.topic,
        section=question_data.section,
        marks=question_data.marks,
        negative_marks=question_data.negative_marks
    )
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    return new_question


@router.get("/exam/{exam_id}", response_model=list[QuestionWithoutAnswer])
async def get_exam_questions(
    exam_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all questions for an exam (without answers)
    Used when student takes the exam
    """
    print(f"[QUESTION DEBUG] get_exam_questions called for exam_id={exam_id}")
    
    # Check if exam exists and is published
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.is_published == True).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found or not published"
        )
    
    # Get active questions
    questions = db.query(Question).filter(
        Question.exam_id == exam_id,
        Question.is_active == True
    ).all()
    
    print(f"[QUESTION DEBUG] Returning {len(questions)} questions")
    return questions


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get question details with answer (Admin/Instructor only)
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Get exam and check permission
    exam = db.query(Exam).filter(Exam.id == question.exam_id).first()
    if exam.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this question"
        )
    
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update question (Admin/Instructor only)
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Get exam and check permission
    exam = db.query(Exam).filter(Exam.id == question.exam_id).first()
    if exam.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this question"
        )
    
    # Update fields
    question.question_text = question_data.question_text
    question.option_a = question_data.option_a
    question.option_b = question_data.option_b
    question.option_c = question_data.option_c
    question.option_d = question_data.option_d
    question.correct_answer = question_data.correct_answer
    question.explanation = question_data.explanation
    question.difficulty = question_data.difficulty
    question.topic = question_data.topic
    question.marks = question_data.marks
    question.negative_marks = question_data.negative_marks
    
    db.commit()
    db.refresh(question)
    
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete question (Admin/Instructor only)
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Get exam and check permission
    exam = db.query(Exam).filter(Exam.id == question.exam_id).first()
    if exam.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this question"
        )
    
    db.delete(question)
    db.commit()
