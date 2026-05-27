import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Exam, Question

db = SessionLocal()
try:
    exams = db.query(Exam).all()
    print(f"Total exams in DB: {len(exams)}")
    for e in exams:
        print(f"ID: {e.id} | Title: {e.title} | Type: {e.exam_type} | Published: {e.is_published} | Questions count: {len(e.questions)}")
except Exception as err:
    print("ERROR:", err)
finally:
    db.close()
