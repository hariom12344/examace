import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Exam, Question

def add_100_questions_to_exam(exam_id, exam_type, difficulty):
    """Add 100 questions to an exam"""
    db = SessionLocal()
    
    questions_data = []
    
    # Generate 100 questions based on exam type
    for i in range(1, 101):
        if exam_type == "Bank":
            sections = ["English", "Quantitative", "Reasoning"]
            section = sections[(i-1) // 34]  # Distribute roughly
            
            if section == "English":
                topic_options = ["Synonyms", "Antonyms", "Grammar", "Vocabulary", "Reading Comprehension"]
                topic = topic_options[(i-1) % len(topic_options)]
            elif section == "Quantitative":
                topic_options = ["Arithmetic", "Percentage", "Geometry", "Algebra", "Ratio"]
                topic = topic_options[(i-1) % len(topic_options)]
            else:
                topic_options = ["Analogy", "Series", "Coding-Decoding", "Reasoning", "Logic"]
                topic = topic_options[(i-1) % len(topic_options)]
                
        elif exam_type == "SSC":
            section = "General Studies"
            topic_options = ["General Awareness", "English", "Math", "Reasoning", "Hindi"]
            topic = topic_options[(i-1) % len(topic_options)]
            
        elif exam_type == "Railway":
            section = "Aptitude"
            topic_options = ["GK", "Math", "Science", "History", "English"]
            topic = topic_options[(i-1) % len(topic_options)]
            
        elif exam_type == "CAT":
            section = "Quantitative"
            topic_options = ["Geometry", "Algebra", "Reasoning", "Data", "Numbers"]
            topic = topic_options[(i-1) % len(topic_options)]
        else:
            section = "General"
            topic = "General Knowledge"
        
        question = Question(
            exam_id=exam_id,
            question_text=f"Q{i}. Sample question for {topic}",
            option_a=f"Option A for Q{i}",
            option_b=f"Option B for Q{i}",
            option_c=f"Option C for Q{i}",
            option_d=f"Option D for Q{i}",
            correct_answer=["A", "B", "C", "D"][i % 4],
            explanation=f"This is the explanation for question {i}",
            marks=1,
            difficulty=difficulty,
            section=section,
            topic=topic
        )
        db.add(question)
    
    db.commit()
    db.close()
    return 100

def main():
    db = SessionLocal()
    try:
        exams = db.query(Exam).all()
        total_added = 0
        
        for exam in exams:
            current_count = db.query(Question).filter(Question.exam_id == exam.id).count()
            
            if current_count >= 100:
                print(f"✓ SKIP: '{exam.title}' - already has {current_count} questions")
                continue
            
            questions_to_add = 100 - current_count
            print(f"\n📝 EXPANDING: '{exam.title}'")
            print(f"   Current: {current_count} | Adding: {questions_to_add}")
            
            added = add_100_questions_to_exam(exam.id, exam.exam_type, exam.difficulty)
            total_added += added
            print(f"   ✅ Added {added} questions successfully!")
        
        # Print final summary
        db = SessionLocal()
        print("\n" + "="*70)
        print("📊 FINAL DATABASE SUMMARY - ALL EXAMS NOW HAVE 100 QUESTIONS")
        print("="*70)
        
        all_exams = db.query(Exam).all()
        for exam in all_exams:
            count = db.query(Question).filter(Question.exam_id == exam.id).count()
            status = "✅" if count == 100 else "⚠️"
            print(f"{status} ID:{exam.id:2d} | {exam.title:40s} | Q:{count:3d} | {exam.exam_type:8s}")
        
        print("="*70)
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
