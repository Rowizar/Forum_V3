from datetime import timedelta
from celery import shared_task
from celery.utils.time import timezone
from django.contrib.auth.models import User
from qa_app.models import Question
from django.core.mail import send_mail

@shared_task
def send_daily_email():
    yesterday = timezone.now() - timedelta(days=1)
    recent_questions = Question.objects.filter(pub_date__gte=yesterday)

    if not recent_questions.exists():
        return "No questions were added in the last 24 hours."

    questions_info = "\n\n".join(
        f"Title: {question.title}\nText: {question.text}\n" for question in recent_questions
    )

    recipients = User.objects.filter(is_active=True).values_list('email', flat=True)
    recipients = [email for email in recipients if email]

    if not recipients:
        return "No users to send updates."

    send_mail(
        'Your daily update from the QA',
        'Here are the latest questions added to the QA in the last 24 hours:\n\n' + questions_info,
        'from@example.com',  # Адрес отправителя ИЗМЕНИТЬ !!!!
        recipients,
        fail_silently=False,
    )
    return "Emails sent successfully with the latest questions."


@shared_task
def send_question_created_email(user_email, question_title):
    send_mail(
        'Your Question Has Been Posted',
        f'Thank you for your question: "{question_title}"',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )
@shared_task
def test_task():
    print("Task is running")