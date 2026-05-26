from database import SessionLocal
from models import Exam, Question
from sqlalchemy.orm import Session

def add_test_exams():
    db = SessionLocal()
    try:
        # 1. IBPS PO Mock Test
        exam1 = Exam(
            title="IBPS PO Mock Test",
            description="Mock test for IBPS PO exam prep",
            duration=30,
            total_marks=100,
            exam_type="Bank",
            difficulty="Medium",
            is_published=True,
            created_by=1
        )
        db.add(exam1)
        db.commit()
        db.refresh(exam1)

        # Add 5 questions to IBPS PO
        for i in range(1, 6):
            q = Question(
                exam_id=exam1.id,
                question_text=f"IBPS PO Question {i}",
                option_a="Option A",
                option_b="Option B",
                option_c="Option C",
                option_d="Option D",
                correct_answer="A",
                marks=20  # 100 / 5
            )
            db.add(q)

        # 2. SSC CGL Practice
        exam2 = Exam(
            title="SSC CGL Practice",
            description="Practice session for SSC CGL",
            duration=45,
            total_marks=150,
            exam_type="SSC",
            difficulty="Medium",
            is_published=True,
            created_by=1
        )
        db.add(exam2)
        db.commit()
        db.refresh(exam2)

        # Add 5 questions to SSC CGL
        for i in range(1, 6):
            q = Question(
                exam_id=exam2.id,
                question_text=f"SSC CGL Question {i}",
                option_a="Option A",
                option_b="Option B",
                option_c="Option C",
                option_d="Option D",
                correct_answer="B",
                marks=30  # 150 / 5
            )
            db.add(q)

        db.commit()
        print("Exams and questions added successfully.")

        # Query database to show exams
        exams = db.query(Exam).filter(Exam.title.in_(["IBPS PO Mock Test", "SSC CGL Practice"])).all()
        for exam in exams:
            print(f"Exam: {exam.title}, ID: {exam.id}, Questions: {len(exam.questions)}, Duration: {exam.duration}, Marks: {exam.total_marks}")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_test_exams()
