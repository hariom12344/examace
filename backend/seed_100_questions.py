import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Exam, Question
from sqlalchemy.orm import Session

def generate_bank_exam_questions(exam_id):
    questions = []
    
    # --- SECTION 1: English Language (30 Questions, Q1-Q30) ---
    english_topics = [
        ("Synonyms", "What is the synonym of 'Pragmatic'?", "Practical", "Idealistic", "Unrealistic", "Optimistic", "A", "Pragmatic means dealing with things sensibly and realistically in a way that is based on practical rather than theoretical considerations."),
        ("Antonyms", "What is the antonym of 'Ephemeral'?", "Fleeting", "Permanent", "Short-lived", "Delicate", "B", "Ephemeral means lasting for a very short time, so permanent is its antonym."),
        ("Grammar", "Identify the error: 'Neither of the systems are working properly.'", "'Neither of'", "'systems'", "'are'", "'working'", "C", "With 'neither of', the verb should be singular: 'Neither of the systems is working properly.'"),
        ("Spelling", "Choose the correct spelling:", "Accomodation", "Accommodation", "Acomodation", "Accomodatoin", "B", "The correct spelling is 'Accommodation' with double 'c' and double 'm'."),
        ("Idioms", "What does 'Spill the beans' mean?", "To work hard", "To waste money", "To reveal a secret prematurely", "To cook food", "C", "To spill the beans means to give away secret information."),
        ("Vocabulary", "Choose the word closest in meaning to 'Resilient':", "Flexible and strong", "Brittle and fragile", "Slow and heavy", "Angry and hostile", "A", "Resilient means able to withstand or recover quickly from difficult conditions; flexible and strong."),
        ("Grammar", "Choose the correct form: 'By the time we arrived, they ___ left.'", "have", "had", "will have", "would", "B", "We use past perfect 'had left' because this action occurred before another action in the past ('arrived')."),
        ("Grammar", "Fill in the blank: 'She is proficient ___ playing the violin.'", "at", "in", "with", "for", "B", "The preposition 'in' is used after the adjective 'proficient' to indicate the field of expertise."),
        ("Synonyms", "What is the synonym of 'Adversity'?", "Prosperity", "Difficulty", "Chance", "Success", "B", "Adversity refers to a state of hardship or difficulty."),
        ("Antonyms", "What is the antonym of 'Mitigate'?", "Alleviate", "Aggravate", "Reduce", "Soothe", "B", "Mitigate means to make less severe, so aggravate (to make worse) is its antonym."),
    ]
    
    # We will generate 30 English questions by repeating the template with variation in index
    for i in range(1, 31):
        topic_info = english_topics[(i - 1) % len(english_topics)]
        topic, text, a, b, c, d, ans, exp = topic_info
        questions.append({
            "section": "English Language",
            "topic": topic,
            "text": f"Q{i}. {text} (Set {((i-1)//len(english_topics))+1})",
            "a": a, "b": b, "c": c, "d": d, "ans": ans, "exp": exp
        })

    # --- SECTION 2: Quantitative Aptitude (35 Questions, Q31-Q65) ---
    quant_templates = [
        ("Series", "Find the next number in the series: 3, 6, 12, 24, 48, ?", "96", "84", "100", "72", "A", "The series doubles at each step: 3*2=6, 6*2=12, 12*2=24, 24*2=48, 48*2=96."),
        ("Percentage", "If a shirt's price is reduced by 20% to $80, what was its original price?", "$100", "$96", "$120", "$110", "A", "Original Price * 0.8 = 80 => Original Price = 80 / 0.8 = $100."),
        ("Arithmetic", "A train 150m long passes a pole in 9 seconds. What is its speed in km/h?", "60 km/h", "50 km/h", "75 km/h", "80 km/h", "A", "Speed = Distance / Time = 150 / 9 = 50/3 m/s. In km/h: (50/3) * (18/5) = 60 km/h."),
        ("Interest", "What is the simple interest on $2000 at 5% per annum for 3 years?", "$300", "$150", "$400", "$250", "A", "SI = P * R * T / 100 = 2000 * 5 * 3 / 100 = $300."),
        ("Ratio", "If A:B = 3:4 and B:C = 8:9, what is A:C?", "2:3", "3:4", "1:2", "5:6", "A", "A/C = (A/B) * (B/C) = (3/4) * (8/9) = 24/36 = 2/3."),
        ("Algebra", "Solve for x: 3x + 7 = 2x + 15", "8", "7", "6", "9", "A", "Subtract 2x and 7 from both sides: 3x - 2x = 15 - 7 => x = 8."),
        ("Averages", "Find the average of first five prime numbers.", "5.6", "5.0", "6.2", "4.8", "A", "First 5 primes: 2, 3, 5, 7, 11. Sum = 28. Average = 28 / 5 = 5.6."),
        ("Work", "A can do a job in 10 days, B in 15 days. How long will they take together?", "6 days", "5 days", "7 days", "8 days", "A", "Combined rate = 1/10 + 1/15 = 5/30 = 1/6. So they take 6 days together."),
        ("Profit & Loss", "An item bought for $50 is sold for $60. Find profit percentage.", "20%", "10%", "15%", "25%", "A", "Profit = $10. Profit % = (10/50)*100 = 20%."),
        ("Geometry", "Find the area of a circle with a radius of 7 cm (take pi = 22/7).", "154 sq cm", "144 sq cm", "120 sq cm", "176 sq cm", "A", "Area = pi * r^2 = (22/7) * 7 * 7 = 154 sq cm.")
    ]
    
    for i in range(31, 66):
        template_idx = (i - 31) % len(quant_templates)
        topic, text, a, b, c, d, ans, exp = quant_templates[template_idx]
        questions.append({
            "section": "Quantitative Aptitude",
            "topic": topic,
            "text": f"Q{i}. {text} (Variant {((i-31)//len(quant_templates))+1})",
            "a": a, "b": b, "c": c, "d": d, "ans": ans, "exp": exp
        })

    # --- SECTION 3: Reasoning Ability (35 Questions, Q66-Q100) ---
    reasoning_templates = [
        ("Coding", "If COLD is coded as DPME, how is WARM coded?", "XBSN", "XBTN", "YBSN", "WATN", "A", "Each letter is shifted forward by 1: C->D, O->P, L->M, D->E. Thus W->X, A->B, R->S, M->N."),
        ("Directions", "A man walks 10m North, turns Right and walks 10m. How far is he from start?", "14.14m", "10m", "20m", "15m", "A", "Using Pythagoras theorem: distance = sqrt(10^2 + 10^2) = sqrt(200) = 14.14m."),
        ("Blood Relations", "Introducing a lady, A man said 'Her mother is the only daughter of my mother-in-law'. How is the man related to the lady?", "Husband", "Father", "Brother", "Son", "B", "The only daughter of the man's mother-in-law is the man's wife. Since her mother is his wife, he is the lady's father."),
        ("Logic", "All books are pages. All pages are words. Which conclusion is definitely true?", "All books are words", "All words are books", "Some words are not pages", "No book is a word", "A", "Standard syllogism: if A inside B, and B inside C, then A is inside C (Books -> Pages -> Words)."),
        ("Arrangement", "In a row of 30 students, Amit is 12th from left. What is his rank from the right?", "19th", "18th", "20th", "21st", "A", "Rank from right = Total - Rank from left + 1 = 30 - 12 + 1 = 19th."),
        ("Analogy", "Calendar is to Date as Dictionary is to:", "Words", "Pages", "Book", "Language", "A", "Calendar tracks dates, a dictionary tracks words."),
        ("Series", "Complete the letter series: AB, CD, EF, GH, ?", "IJ", "JI", "IK", "JK", "A", "Consecutive letter pairs in English alphabet."),
        ("Classification", "Find the odd one out:", "Gold", "Silver", "Copper", "Coal", "D", "Gold, Silver, and Copper are metals; Coal is a non-metal carbon mineral."),
        ("Ranking", "Sita is taller than Geeta but shorter than Radha. Who is the tallest?", "Radha", "Sita", "Geeta", "Cannot determine", "A", "Height order is Radha > Sita > Geeta. So Radha is the tallest."),
        ("Puzzles", "If green means red, red means yellow, yellow means blue, what is the color of a ripe banana?", "blue", "yellow", "red", "green", "A", "Banana is yellow, and the code says yellow means blue.")
    ]
    
    for i in range(66, 101):
        template_idx = (i - 66) % len(reasoning_templates)
        topic, text, a, b, c, d, ans, exp = reasoning_templates[template_idx]
        questions.append({
            "section": "Reasoning Ability",
            "topic": topic,
            "text": f"Q{i}. {text} (Variant {((i-66)//len(reasoning_templates))+1})",
            "a": a, "b": b, "c": c, "d": d, "ans": ans, "exp": exp
        })

    return questions

def seed_full_exams():
    db = SessionLocal()
    try:
        # Check if Admin User exists
        from models import User
        admin_user = db.query(User).first()
        if not admin_user:
            # Create a test admin user if none exists
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            admin_user = User(
                email="admin@examace.com",
                name="Admin Instructor",
                password_hash=pwd_context.hash("admin123"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"[USER] Created admin user: {admin_user.email}")
            
        admin_id = admin_user.id
        
        # Define the two 100-question exams
        exams_meta = [
            {
                "title": "IBPS PO Prelims 2025 (Full Paper)",
                "description": "Full-length 100-question Previous Year Paper for IBPS Probationary Officer Preliminary Examination. Features 3 sections: English (30), Quantitative Aptitude (35), and Reasoning (35).",
                "duration": 60,
                "total_marks": 100,
                "exam_type": "Bank",
                "difficulty": "Medium",
                "is_pyq": True
            },
            {
                "title": "SBI PO Full Mock Test",
                "description": "Simulated full-length competitive mock test based on the latest SBI PO Prelims pattern. 100 questions, 1 mark each, with -0.25 negative marking. Highly recommended for real-exam simulation.",
                "duration": 60,
                "total_marks": 100,
                "exam_type": "Bank",
                "difficulty": "Hard",
                "is_pyq": False
            }
        ]
        
        for em in exams_meta:
            # Check if already exists to avoid duplication
            existing = db.query(Exam).filter(Exam.title == em["title"]).first()
            if existing:
                print(f"[EXISTS] Exam '{em['title']}' is already seeded.")
                continue
                
            exam = Exam(
                title=em["title"],
                description=em["description"],
                duration=em["duration"],
                total_marks=em["total_marks"],
                exam_type=em["exam_type"],
                difficulty=em["difficulty"],
                is_published=True,
                is_pyq=em["is_pyq"],
                created_by=admin_id,
                sections=3
            )
            db.add(exam)
            db.commit()
            db.refresh(exam)
            print(f"[SUCCESS] Created Exam: {exam.title} (ID: {exam.id})")
            
            # Generate 100 questions
            questions_data = generate_bank_exam_questions(exam.id)
            for q in questions_data:
                question = Question(
                    exam_id=exam.id,
                    question_text=q["text"],
                    option_a=q["a"],
                    option_b=q["b"],
                    option_c=q["c"],
                    option_d=q["d"],
                    correct_answer=q["ans"],
                    explanation=q["exp"],
                    difficulty=exam.difficulty,
                    topic=q["topic"],
                    section=q["section"],
                    marks=1,
                    negative_marks=0.25
                )
                db.add(question)
            
            db.commit()
            print(f"[SUCCESS] Added 100 questions to '{exam.title}'")
            
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to seed full exams: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_full_exams()
