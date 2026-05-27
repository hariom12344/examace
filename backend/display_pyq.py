"""
Display Real PYQ Questions in Database
"""
from database import SessionLocal
from models import Question

db = SessionLocal()

print("\n" + "="*90)
print("📚 REAL PREVIOUS YEAR QUESTIONS (PYQ) NOW IN EXAMACE DATABASE")
print("="*90 + "\n")

# Get sample questions
questions = db.query(Question).filter(
    Question.topic.in_(['Vocabulary', 'Algebra', 'Blood Relations', 'Simple Interest'])
).limit(6).all()

for idx, q in enumerate(questions, 1):
    print(f"\n{idx}. [{q.difficulty.upper()}] {q.topic}")
    print(f"   Section: {q.section}")
    print(f"   Source: {['IBPS PO', 'SBI PO', 'SSC CGL', 'Railway', 'CAT'][q.exam_id % 5]}")
    print(f"\n   Question: {q.question_text}")
    print(f"\n   Options:")
    print(f"   (A) {q.option_a}")
    print(f"   (B) {q.option_b}")
    print(f"   (C) {q.option_c}")
    print(f"   (D) {q.option_d}")
    print(f"\n   ✓ Answer: {q.correct_answer}")
    print(f"   📝 Explanation: {q.explanation}")
    print(f"   Marks: {q.marks} | Negative: -{q.negative_marks}")

print("\n" + "="*90)
print(f"✅ Total Real PYQ Questions in Database: {db.query(Question).count()}")
print("="*90 + "\n")

db.close()
