import json
import requests

# 1. Login to get token
login_response = requests.post(
    'http://localhost:8000/api/auth/login',
    json={'email': 'test@example.com', 'password': 'password123'}
)
login_data = login_response.json()
access_token = login_data['access_token']
print(f'✓ Login successful')
print(f'  Token: {access_token[:50]}...')

# 2. Get exam questions
headers = {'Authorization': f'Bearer {access_token}'}
questions_response = requests.get(
    'http://localhost:8000/api/questions/exam/1',
    headers=headers
)

if questions_response.status_code == 200:
    print(f'✓ Questions retrieved')
else:
    print(f'✗ Failed to get questions: {questions_response.status_code}')
    print(f'  Response: {questions_response.text}')

# 3. Submit exam with answers
answers = [
    {'question_id': 1, 'selected_answer': 'A', 'time_spent': 30},
    {'question_id': 2, 'selected_answer': 'B', 'time_spent': 30},
    {'question_id': 3, 'selected_answer': 'C', 'time_spent': 30},
    {'question_id': 4, 'selected_answer': 'D', 'time_spent': 30},
    {'question_id': 5, 'selected_answer': 'A', 'time_spent': 30},
]

result_response = requests.post(
    'http://localhost:8000/api/results',
    json={'exam_id': 1, 'answers': answers, 'total_time': 1800},
    headers=headers
)

if result_response.status_code == 200:
    result_data = result_response.json()
    print(f'✓ Exam submitted successfully!')
    print(f'  Score: {result_data["score"]}/{5*4}')
    print(f'  Accuracy: {result_data["accuracy"]:.1f}%')
    print(f'  Result ID: {result_data["id"]}')
else:
    print(f'✗ Failed to submit exam: {result_response.status_code}')
    print(f'  Response: {result_response.text}')
