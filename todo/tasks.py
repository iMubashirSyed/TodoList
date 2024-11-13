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

# @shared_task(bind=True)
# def send_task_reminder(self, task_id):
#     # Change the logic according to celery beat
#     task = Task.objects.get(id=task_id)
#     send_mail(
#         f'Reminder: {task.title} is due soon!',
#         f'Dear {task.user.username}, your task "{task.title}" is due on {task.due_date}. Please complete it on time!',
#         'studypurpose220904@gmail.com',  # Replace with your sender email
#         [task.user.email],
#         fail_silently=False,
#     )


# from celery import shared_task
# from django.core.mail import send_mail
# from django.utils.timezone import now, timedelta
# from .models import Task

# @shared_task(bind=True)
# def send_task_reminder(self):
#     #  tomorrow = now() + timedelta(days=1)
#     #  tasks_due_tomorrow = Task.objects.filter(due_date__date=tomorrow.date())
#     current_time = now()
#     # Calculate the cutoff for tasks due more than one day from now
#     due_date_cutoff = current_time + timedelta(days=1)

#     # Get all tasks with a due date greater than the cutoff
#     tasks_due_later = Task.objects.filter(due_date__gt=due_date_cutoff)


#     for task in tasks_due_later:
#         send_mail(
#             f'Reminder: {task.title} is due tomorrow!',
#             f'Dear {task.user.username}, your task "{task.title}" is due on {task.due_date}. Please complete it on time!',
#             'studypurpose220904@gmail.com',  # Replace with your sender email
#             [task.user.email],
#             fail_silently=False,
#         )

# from celery import shared_task
# from django.core.mail import send_mail
# from django.utils.timezone import now
# from datetime import timedelta
# from .models import Task

# @shared_task(bind=True)
# def send_task_reminder(self):
#     # Get the current time
#     current_time = now()

#     # Define the 30-minute cutoff for upcoming tasks
#     reminder_cutoff = current_time + timedelta(minutes=30)

#     # Get all tasks due within the next 30 minutes
#     tasks_due_soon = Task.objects.filter(due_date__gt=current_time, due_date__lte=reminder_cutoff, reminder_sent=False)

#     for task in tasks_due_soon:
#         send_mail(
#             f'Reminder: {task.title} is due soon!',
#             f'Dear {task.user.username}, your task "{task.title}" is due on {task.due_date}. Please complete it on time!',
#             'studypurpose220904@gmail.com',  # Replace with your sender email
#             [task.user.email],
#             fail_silently=False,
#         )
        
#     task.reminder_sent = True
#     task.save()
from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from .models import Task

@shared_task
def send_task_reminder():
    # Get the current time
    current_time = now()
    
    # Define the reminder window: tasks due in the next 30 minutes
    reminder_window = current_time + timedelta(minutes=30)
    
    # Get tasks due in the next 30 minutes that haven't had a reminder sent
    tasks_due_soon = Task.objects.filter(due_date__lte=reminder_window, reminder_sent=False)
    
    for task in tasks_due_soon:
        # Send reminder email
        if task.user and task.user.email:
            send_mail(
                subject=f"Reminder: '{task.title}' is due soon!",
                message=f"Dear {task.user.username},\n\nYour task '{task.title}' is due on {task.due_date}. Please complete it on time!",
                from_email='studypurpose220904@gmail.com',  # Replace with your sender email
                recipient_list=[task.user.email],
                fail_silently=False,
            )
            
            # Mark reminder as sent
            task.reminder_sent = True
            task.save()

