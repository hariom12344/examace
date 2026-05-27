import json
import requests

BASE_URL = 'http://localhost:8000/api'

# 1. Try to signup first
signup_response = requests.post(
    f'{BASE_URL}/auth/signup',
    json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    }
)

if signup_response.status_code == 201:
    print('✓ Signup successful (new user created)')
    login_data = signup_response.json()
    access_token = login_data['access_token']
else:
    print('ℹ User might already exist, attempting login...')
    # 2. Login to get token
    login_response = requests.post(
        f'{BASE_URL}/auth/login',
        json={'email': 'test@example.com', 'password': 'password123'}
    )
    if login_response.status_code == 200:
        login_data = login_response.json()
        access_token = login_data['access_token']
        print('✓ Login successful')
    else:
        print(f'✗ Login failed: {login_response.status_code}')
        print(login_response.text)
        exit(1)

headers = {'Authorization': f'Bearer {access_token}'}

# 3. Get published exams
exams_response = requests.get(f'{BASE_URL}/exams', headers=headers)
if exams_response.status_code != 200:
    print(f'✗ Failed to get exams: {exams_response.status_code}')
    exit(1)

exams = exams_response.json()
if not exams:
    print('✗ No published exams found in DB. Run seed scripts first.')
    exit(1)

# Pick the first exam
exam = exams[0]
exam_id = exam['id']
print(f'✓ Found Exam: "{exam["title"]}" (ID: {exam_id})')

# 4. Get exam questions
questions_response = requests.get(
    f'{BASE_URL}/questions/exam/{exam_id}',
    headers=headers
)

if questions_response.status_code != 200:
    print(f'✗ Failed to get questions: {questions_response.status_code}')
    print(questions_response.text)
    exit(1)

questions = questions_response.json()
print(f'✓ Retrieved {len(questions)} questions for exam {exam_id}')

# 5. Submit exam with answers (all answering 'A')
answers = []
for q in questions[:5]: # Submit up to 5 answers
    answers.append({
        'question_id': q['id'],
        'selected_answer': 'A',
        'time_spent': 20
    })

result_response = requests.post(
    f'{BASE_URL}/results',
    json={'exam_id': exam_id, 'answers': answers, 'total_time': 100},
    headers=headers
)

if result_response.status_code == 201:
    result_data = result_response.json()
    print('✓ Exam submitted successfully!')
    print(f'  Score: {result_data["score"]}')
    print(f'  Accuracy: {result_data["accuracy"]:.1f}%')
    print(f'  Result ID: {result_data["id"]}')
else:
    print(f'✗ Failed to submit exam: {result_response.status_code}')
    print(result_response.text)

