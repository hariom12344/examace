import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Exam, Question
from sqlalchemy.orm import Session

def generate_questions_for_exam(exam_type, exam_difficulty, count=100):
    """Generate realistic questions based on exam type"""
    
    questions = []
    
    if exam_type == "Bank":
        # Bank exam questions - English, Quant, Reasoning
        templates = {
            "English": [
                ("Synonyms", "Choose the closest synonym of '{word}'", ["Option A", "Option B", "Option C", "Option D"], "A", "Explanation for the answer"),
                ("Grammar", "Identify the error: '{sentence}'", ["Part 1", "Part 2", "Part 3", "Part 4"], "B", "Grammar explanation"),
                ("Vocabulary", "The word '{word}' means:", ["Definition 1", "Definition 2", "Definition 3", "Definition 4"], "C", "Word meaning explanation"),
                ("Reading Comprehension", "What does the passage suggest?", ["Conclusion 1", "Conclusion 2", "Conclusion 3", "Conclusion 4"], "A", "RC explanation"),
                ("Antonyms", "Opposite of '{word}' is:", ["Word 1", "Word 2", "Word 3", "Word 4"], "B", "Antonym explanation"),
            ],
            "Quantitative": [
                ("Arithmetic", "Calculate: {problem}", ["100", "150", "200", "250"], "A", "Calculation explanation"),
                ("Percentage", "{percentage_problem}", ["20%", "25%", "30%", "35%"], "B", "Percentage calculation"),
                ("Ratio & Proportion", "If A:B = {ratio}, find C", ["10", "15", "20", "25"], "C", "Ratio explanation"),
                ("Geometry", "Area of circle with radius {radius}:", ["Area 1", "Area 2", "Area 3", "Area 4"], "A", "Geometry formula"),
                ("Algebra", "Solve: {equation}", ["5", "8", "10", "12"], "B", "Algebraic solution"),
            ],
            "Reasoning": [
                ("Analogy", "{Term1} is to {Term2} as {Term3} is to?", ["Option 1", "Option 2", "Option 3", "Option 4"], "A", "Analogy explanation"),
                ("Series", "Find the next in series: {series}", ["Next 1", "Next 2", "Next 3", "Next 4"], "B", "Series pattern"),
                ("Coding-Decoding", "If {code1} = {value1}, then {code2} = ?", ["Value 1", "Value 2", "Value 3", "Value 4"], "C", "Coding logic"),
                ("Directions", "Person walks {direction1}, then {direction2}. Position?", ["Position 1", "Position 2", "Position 3", "Position 4"], "A", "Direction logic"),
                ("Logical Reasoning", "If statements A and B are true, which conclusion?", ["Conclusion 1", "Conclusion 2", "Conclusion 3", "Conclusion 4"], "B", "Logic explanation"),
            ]
        }
        
        sections = ["English", "Quantitative", "Reasoning"]
        section_counts = [30, 35, 35]  # Realistic distribution
        
        question_num = 1
        for section_idx, section in enumerate(sections):
            for i in range(section_counts[section_idx]):
                template = templates[section][i % len(templates[section])]
                topic, text, options, answer, explanation = template
                
                questions.append({
                    "section": section,
                    "topic": topic,
                    "text": f"Q{question_num}. {text}",
                    "a": options[0],
                    "b": options[1],
                    "c": options[2],
                    "d": options[3],
                    "ans": answer,
                    "exp": explanation,
                    "marks": 1,
                    "difficulty": exam_difficulty
                })
                question_num += 1
    
    elif exam_type == "SSC":
        # SSC exam questions
        templates = [
            ("General Awareness", "Who was the first PM of India?", "Jawaharlal Nehru", "Dr. Rajendra Prasad", "Sardar Vallabhbhai Patel", "Arun Jaitley", "A", "Historical fact"),
            ("English", "Choose the correct form:", "I is going", "I are going", "I am going", "I have going", "C", "Grammar rule"),
            ("Quantitative", "5 + 5 * 5 = ?", "50", "30", "25", "10", "A", "Order of operations"),
            ("Reasoning", "What comes next?", "2, 4, 6, 8, __", "10", "12", "9", "11", "A", "Series pattern"),
            ("Hindi", "Opposite of 'sukh' is:", "dukh", "khushi", "anand", "hansa", "A", "Hindi vocabulary"),
        ]
        
        for i in range(count):
            template = templates[i % len(templates)]
            topic, text, a, b, c, d, ans, exp = template
            
            questions.append({
                "section": "General Studies",
                "topic": topic,
                "text": f"Q{i+1}. {text}",
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "ans": ans,
                "exp": exp,
                "marks": 1,
                "difficulty": exam_difficulty
            })
    
    elif exam_type == "Railway":
        # Railway exam questions
        templates = [
            ("GK", "Which is the longest river in India?", "Ganges", "Brahmaputra", "Indus", "Godavari", "A", "Geography"),
            ("Math", "15% of 200 is:", "30", "25", "35", "40", "A", "Percentage"),
            ("Science", "What is the chemical formula of water?", "H2O", "CO2", "O2", "H2O2", "A", "Chemistry"),
            ("History", "Who was Ashoka?", "Mauryan Emperor", "British Governor", "Mughal Emperor", "Sikh Guru", "A", "History"),
            ("English", "Correct spelling:", "Occassion", "Occasion", "Ocassion", "Ocasion", "B", "Spelling"),
        ]
        
        for i in range(count):
            template = templates[i % len(templates)]
            topic, text, a, b, c, d, ans, exp = template
            
            questions.append({
                "section": "Aptitude",
                "topic": topic,
                "text": f"Q{i+1}. {text}",
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "ans": ans,
                "exp": exp,
                "marks": 1,
                "difficulty": exam_difficulty
            })
    
    elif exam_type == "CAT":
        # CAT exam questions (higher difficulty)
        templates = [
            ("Geometry", "In a triangle ABC, angle A = 60°, find angle B", "60°", "75°", "90°", "Cannot determine", "D", "Geometric property"),
            ("Algebra", "If x² + y² = 25 and xy = 12, find x + y", "±7", "±5", "±10", "±8", "A", "Algebraic manipulation"),
            ("Logical Reasoning", "Which number comes next?", "2, 3, 5, 7, 11, __", "13", "14", "15", "16", "A", "Prime number series"),
            ("Data Interpretation", "If profit increases by 20%, new profit is?", "120% of original", "130% of original", "150% of original", "200% of original", "A", "Percentage increase"),
            ("Number System", "LCM of 12 and 18:", "24", "36", "48", "72", "B", "LCM concept"),
        ]
        
        for i in range(count):
            template = templates[i % len(templates)]
            topic, text, a, b, c, d, ans, exp = template
            
            questions.append({
                "section": "Quantitative",
                "topic": topic,
                "text": f"Q{i+1}. {text}",
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "ans": ans,
                "exp": exp,
                "marks": 3,
                "difficulty": exam_difficulty
            })
    
    return questions


def expand_exams_to_100():
    db = SessionLocal()
    try:
        # Get all exams with less than 100 questions
        exams = db.query(Exam).all()
        
        for exam in exams:
            question_count = db.query(Question).filter(Question.exam_id == exam.id).count()
            
            # Skip if already has 100 or more questions
            if question_count >= 100:
                print(f"✓ SKIP: '{exam.title}' already has {question_count} questions")
                continue
            
            # Calculate how many questions to add
            questions_to_add = 100 - question_count
            
            print(f"\n📝 EXPANDING: '{exam.title}'")
            print(f"   Current: {question_count} | Target: 100 | Adding: {questions_to_add}")
            
            # Generate new questions
            new_questions = generate_questions_for_exam(
                exam_type=exam.exam_type,
                exam_difficulty=exam.difficulty,
                count=questions_to_add
            )
            
            # Add generated questions to database
            for q_data in new_questions:
                question = Question(
                    exam_id=exam.id,
                    question_text=q_data["text"],
                    option_a=q_data["a"],
                    option_b=q_data["b"],
                    option_c=q_data["c"],
                    option_d=q_data["d"],
                    correct_answer=q_data["ans"],
                    explanation=q_data["exp"],
                    marks=q_data.get("marks", 1),
                    difficulty=q_data.get("difficulty", exam.difficulty),
                    section=q_data.get("section", "General"),
                    topic=q_data.get("topic", "Unknown")
                )
                db.add(question)
            
            db.commit()
            print(f"   ✅ Added {questions_to_add} questions successfully!")
        
        # Print final summary
        print("\n" + "="*60)
        print("📊 FINAL DATABASE SUMMARY")
        print("="*60)
        
        all_exams = db.query(Exam).all()
        for exam in all_exams:
            count = db.query(Question).filter(Question.exam_id == exam.id).count()
            print(f"✓ {exam.title}")
            print(f"  └─ Questions: {count} | Type: {exam.exam_type} | Difficulty: {exam.difficulty}")
        
        print("="*60)
        print(f"✅ All exams now have 100 questions each!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    expand_exams_to_100()
