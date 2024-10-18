# # todo/tasks.py
# from celery import shared_task
# from django.core.mail import send_mail
# from django.utils import timezone
# from .models import Task

# @shared_task
# def send_task_reminders():
#     # Get current time
#     now = timezone.now()
    
#     # Reminder threshold: send reminders for tasks due within the next 1 day
#     reminder_threshold = now + timezone.timedelta(days=1)
    
#     # Fetch tasks where due date is within the next day and not completed
#     tasks_to_remind = Task.objects.filter(due_date__lte=reminder_threshold, due_date__gt=now, completed=False)
    
#     for task in tasks_to_remind:
#         # Send an email reminder to the user
#         send_mail(
#             subject=f"Reminder: Your task '{task.title}' is due soon",
#             message=f"Dear {task.user.username},\n\nYour task '{task.title}' is due on {task.due_date}. Please complete it soon!",
#             from_email='noreply@mytodoapp.com',
#             recipient_list=[task.user.email],
#             fail_silently=False,
#         )

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Task

@shared_task(bind=True)
def send_task_reminder(self, task_id):
    task = Task.objects.get(id=task_id)
    send_mail(
        f'Reminder: {task.title} is due soon!',
        f'Dear {task.user.username}, your task "{task.title}" is due on {task.due_date}. Please complete it on time!',
        'studypurpose220904@gmail.com',  # Replace with your sender email
        [task.user.email],
        fail_silently=False,
    )
