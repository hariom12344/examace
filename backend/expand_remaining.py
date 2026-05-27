import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Exam, Question

def expand_remaining_exams():
    """Expand all exams that have less than 100 questions to exactly 100"""
    db = SessionLocal()
    
    exams_to_expand = [
        (2, "SSC CGL Practice", "SSC"),
        (3, "IBPS PO Prelims 2025", "Bank"),
        (4, "SSC CGL Tier 1", "SSC"),
        (5, "Railway Exam RRB NTPC", "Railway"),
    ]
    
    for exam_id, exam_name, exam_type in exams_to_expand:
        # Get current count
        current_count = db.query(Question).filter(Question.exam_id == exam_id).count()
        questions_needed = 100 - current_count
        
        if questions_needed <= 0:
            print(f"✓ {exam_name} - already has {current_count} questions")
            continue
        
        print(f"\n📝 Expanding: {exam_name}")
        print(f"   Current: {current_count} | Adding: {questions_needed}")
        
        # Generate and add questions
        for i in range(questions_needed):
            question = Question(
                exam_id=exam_id,
                question_text=f"Question {current_count + i + 1}",
                option_a=f"Option A for Q{current_count + i + 1}",
                option_b=f"Option B for Q{current_count + i + 1}",
                option_c=f"Option C for Q{current_count + i + 1}",
                option_d=f"Option D for Q{current_count + i + 1}",
                correct_answer=["A", "B", "C", "D"][(current_count + i) % 4],
                explanation=f"Explanation for question {current_count + i + 1}",
                marks=1,
                difficulty="Medium" if exam_type != "CAT" else "Hard",
                section="General",
                topic="Test Topic"
            )
            db.add(question)
        
        db.commit()
        print(f"   ✅ Added {questions_needed} questions successfully!")
    
    # Print final summary
    print("\n" + "="*70)
    print("✅ FINAL DATABASE STATUS - ALL EXAMS")
    print("="*70)
    
    all_exams = db.query(Exam).all()
    for exam in all_exams:
        count = db.query(Question).filter(Question.exam_id == exam.id).count()
        status = "✅" if count >= 100 else "⚠️"
        print(f"{status} ID:{exam.id} | {exam.title:45} | Questions: {count:3d}")
    
    print("="*70)
    db.close()

if __name__ == "__main__":
    expand_remaining_exams()
