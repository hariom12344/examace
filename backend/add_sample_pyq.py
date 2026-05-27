from database import SessionLocal
from models import Exam, Question
from sqlalchemy.orm import Session

def add_comprehensive_exams():
    db = SessionLocal()
    try:
        exams_data = [
            {
                "title": "IBPS PO Prelims 2025",
                "description": "IBPS Probationary Officer Preliminary Exam",
                "duration": 60,
                "total_marks": 100,
                "exam_type": "Bank",
                "difficulty": "Medium",
                "questions": [
                    {"text": "If APPLE is coded as 1-16-16-12-5, how is MANGO coded?", "a": "13-1-14-7-15", "b": "13-1-13-7-15", "c": "12-1-14-7-15", "d": "13-2-14-7-15", "ans": "a", "topic": "Coding"},
                    {"text": "In a row of 40 children, A is 15th from left. What is A's position from right?", "a": "25", "b": "26", "c": "24", "d": "27", "ans": "b", "topic": "Arrangement"},
                    {"text": "All birds are animals. Some animals are mammals. Which conclusion is valid?", "a": "Some birds are mammals", "b": "All birds are mammals", "c": "No bird is a mammal", "d": "Some birds may be mammals", "ans": "d", "topic": "Logic"},
                    {"text": "If a number is divided by 8, remainder is 3. What is the remainder when the number is divided by 4?", "a": "1", "b": "2", "c": "3", "d": "0", "ans": "c", "topic": "Mathematics"},
                    {"text": "2, 5, 10, 17, 26, ?", "a": "35", "b": "37", "c": "40", "d": "42", "ans": "b", "topic": "Series"},
                ]
            },
            {
                "title": "SSC CGL Tier 1",
                "description": "Staff Selection Commission Combined Graduate Level",
                "duration": 75,
                "total_marks": 200,
                "exam_type": "SSC",
                "difficulty": "Medium",
                "questions": [
                    {"text": "What is the capital of Australia?", "a": "Sydney", "b": "Melbourne", "c": "Canberra", "d": "Brisbane", "ans": "c", "topic": "Geography"},
                    {"text": "Which planet is known as the Red Planet?", "a": "Venus", "b": "Mars", "c": "Jupiter", "d": "Saturn", "ans": "b", "topic": "Science"},
                    {"text": "What is 15% of 200?", "a": "30", "b": "25", "c": "35", "d": "20", "ans": "a", "topic": "Percentage"},
                    {"text": "Find the LCM of 12 and 18", "a": "24", "b": "36", "c": "48", "d": "60", "ans": "b", "topic": "Mathematics"},
                    {"text": "Who wrote the National Anthem of India?", "a": "Rabindranath Tagore", "b": "Bankim Chandra", "c": "Keshab Chandra", "d": "Rammohan Roy", "ans": "a", "topic": "History"},
                ]
            },
            {
                "title": "Railway Exam RRB NTPC",
                "description": "Railway Recruitment Board Non-Technical Popular Categories",
                "duration": 90,
                "total_marks": 120,
                "exam_type": "Railway",
                "difficulty": "Easy",
                "questions": [
                    {"text": "What is the SI unit of temperature?", "a": "Celsius", "b": "Fahrenheit", "c": "Kelvin", "d": "Rankine", "ans": "c", "topic": "Physics"},
                    {"text": "Which is the longest river in India?", "a": "Brahmaputra", "b": "Indus", "c": "Ganges", "d": "Godavari", "ans": "c", "topic": "Geography"},
                    {"text": "3 + 3 × 3 - 3 ÷ 3 = ?", "a": "9", "b": "11", "c": "12", "d": "8", "ans": "b", "topic": "Arithmetic"},
                    {"text": "How many sides does a hexagon have?", "a": "5", "b": "6", "c": "7", "d": "8", "ans": "b", "topic": "Geometry"},
                    {"text": "Which element has atomic number 6?", "a": "Oxygen", "b": "Carbon", "c": "Nitrogen", "d": "Hydrogen", "ans": "b", "topic": "Chemistry"},
                ]
            },
            {
                "title": "SBI PO Preliminary",
                "description": "State Bank of India Probationary Officer Exam",
                "duration": 60,
                "total_marks": 100,
                "exam_type": "Bank",
                "difficulty": "Medium",
                "questions": [
                    {"text": "If yesterday was Thursday, what day is tomorrow?", "a": "Friday", "b": "Saturday", "c": "Sunday", "d": "Monday", "ans": "b", "topic": "Logic"},
                    {"text": "Complete the series: 1, 1, 2, 3, 5, 8, 13, ?", "a": "20", "b": "21", "c": "18", "d": "22", "ans": "b", "topic": "Series"},
                    {"text": "What is the square root of 144?", "a": "10", "b": "11", "c": "12", "d": "13", "ans": "c", "topic": "Mathematics"},
                    {"text": "How many vowels are there in English alphabet?", "a": "4", "b": "5", "c": "6", "d": "7", "ans": "b", "topic": "English"},
                    {"text": "If 2x + 5 = 13, what is x?", "a": "3", "b": "4", "c": "5", "d": "6", "ans": "b", "topic": "Algebra"},
                ]
            },
            {
                "title": "CAT Quantitative Ability",
                "description": "Common Admission Test - Quant Section",
                "duration": 40,
                "total_marks": 66,
                "exam_type": "CAT",
                "difficulty": "Hard",
                "questions": [
                    {"text": "What is the value of (2^3 × 3^2) / (2^2 × 3)?", "a": "6", "b": "8", "c": "12", "d": "18", "ans": "a", "topic": "Algebra"},
                    {"text": "A man walks 5 km North, then 3 km East, then 5 km South. How far is he from start?", "a": "3 km", "b": "5 km", "c": "8 km", "d": "13 km", "ans": "a", "topic": "Geometry"},
                    {"text": "If A:B = 2:3 and B:C = 4:5, find A:B:C", "a": "8:12:15", "b": "2:3:5", "c": "4:6:8", "d": "3:4:5", "ans": "a", "topic": "Ratio"},
                    {"text": "What is the HCF of 24 and 36?", "a": "6", "b": "8", "c": "12", "d": "18", "ans": "c", "topic": "Number Theory"},
                    {"text": "If simple interest on Rs. 1000 for 2 years is Rs. 200, find rate?", "a": "5%", "b": "10%", "c": "15%", "d": "20%", "ans": "b", "topic": "Interest"},
                ]
            },
        ]

        for exam_data in exams_data:
            exam = Exam(
                title=exam_data["title"],
                description=exam_data["description"],
                duration=exam_data["duration"],
                total_marks=exam_data["total_marks"],
                exam_type=exam_data["exam_type"],
                difficulty=exam_data["difficulty"],
                is_published=True,
                is_pyq=True,
                created_by=1
            )
            db.add(exam)
            db.commit()
            db.refresh(exam)

            # Add questions
            marks_per_q = exam_data["total_marks"] // len(exam_data["questions"])
            for i, q_data in enumerate(exam_data["questions"], 1):
                question = Question(
                    exam_id=exam.id,
                    question_text=q_data["text"],
                    option_a=q_data["a"],
                    option_b=q_data["b"],
                    option_c=q_data["c"],
                    option_d=q_data["d"],
                    correct_answer=q_data["ans"].upper(),
                    marks=marks_per_q,
                    topic=q_data["topic"],
                    difficulty=exam_data["difficulty"]
                )
                db.add(question)
            
            db.commit()
            print(f"[SUCCESS] {exam_data['title']} - {len(exam_data['questions'])} questions added")

        print("\n" + "="*60)
        print("All Sample PYQ Exams Added Successfully!")
        print("="*60)
        
        # Display summary
        all_exams = db.query(Exam).filter(Exam.is_published == True).all()
        for exam in all_exams:
            print(f"Exam: {exam.title}: {len(exam.questions)} questions, {exam.total_marks} marks, {exam.duration} min")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_comprehensive_exams()
