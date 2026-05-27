"""
Email Notification Router for ExamAce
Sends email notifications for exam completion and other events
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os

from database import get_db
from models import User, Result, Exam

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

# Email configuration (should be in environment variables)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "examace@example.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_app_password")


class EmailNotification(BaseModel):
    recipient_email: EmailStr
    subject: str
    message: str


def send_email(recipient_email: str, subject: str, message: str):
    """Send email notification"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
                .content {{ padding: 20px; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>ExamAce Notification</h1>
                </div>
                <div class="content">
                    {message}
                </div>
                <div class="footer">
                    <p>© 2026 ExamAce. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        # Connect to SMTP server and send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


@router.post("/send-exam-completion")
async def send_exam_completion_notification(
    result_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Send email notification when exam is completed
    """
    try:
        result = db.query(Result).filter(Result.id == result_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")

        user = db.query(User).filter(User.id == result.user_id).first()
        exam = db.query(Exam).filter(Exam.id == result.exam_id).first()

        if not user or not exam:
            raise HTTPException(status_code=404, detail="User or Exam not found")

        # Create notification message
        message = f"""
        <h2>Congratulations, {user.name}! 🎉</h2>
        <p>You have successfully completed the exam: <strong>{exam.title}</strong></p>
        <hr/>
        <h3>Your Performance:</h3>
        <ul>
            <li><strong>Score:</strong> {result.score}/{exam.total_marks}</li>
            <li><strong>Accuracy:</strong> {result.accuracy}%</li>
            <li><strong>Correct Answers:</strong> {result.correct_answers}</li>
            <li><strong>Wrong Answers:</strong> {result.wrong_answers}</li>
            <li><strong>Unanswered:</strong> {result.unanswered}</li>
            <li><strong>Time Taken:</strong> {result.time_taken // 60} minutes {result.time_taken % 60} seconds</li>
        </ul>
        <hr/>
        <p><strong>Rank:</strong> {result.rank if result.rank else 'Calculating...'}</p>
        <p>Keep practicing and improving your scores! Visit <a href="https://examace.com/analytics">your analytics</a> for detailed insights.</p>
        """

        # Send email in background
        background_tasks.add_task(
            send_email,
            user.email,
            f"ExamAce: {exam.title} - Results Ready! 🎯",
            message
        )

        return {
            "message": "Notification sent successfully",
            "status": "queued"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-performance-alert")
async def send_performance_alert(
    user_id: int,
    alert_type: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Send performance-based alerts to users
    alert_type: 'improvement', 'warning', 'milestone'
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        messages = {
            "improvement": f"""
                <h2>Great Progress, {user.name}! 📈</h2>
                <p>Your accuracy has improved by 5% in the last 3 exams!</p>
                <p>Keep up the momentum and continue practicing.</p>
            """,
            "warning": f"""
                <h2>Time for a Reality Check 🎯</h2>
                <p>Your recent scores have been below average.</p>
                <p>Try focusing on weaker sections and take more practice tests.</p>
            """,
            "milestone": f"""
                <h2>Milestone Achievement! 🏆</h2>
                <p>You've completed 10 exams on ExamAce!</p>
                <p>Check out your detailed analytics to see your progress.</p>
            """
        }

        message = messages.get(alert_type, "Performance Update")

        background_tasks.add_task(
            send_email,
            user.email,
            f"ExamAce: Performance Alert - {alert_type.title()}",
            message
        )

        return {"message": "Alert sent successfully", "status": "queued"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/email-preference/{user_id}")
async def get_email_preference(user_id: int, db: Session = Depends(get_db)):
    """Get user's email notification preferences"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return notification preferences
    return {
        "user_id": user_id,
        "email": user.email,
        "notifications_enabled": True,
        "email_on_exam_complete": True,
        "email_on_new_features": True,
        "email_frequency": "weekly"
    }
