from accounts.models import User
from tasks.models import Task
from task_manager.celery import app
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta

@app.task
def check_expired():
    users = User.objects.filter(expired_email=True)
    for user in users:
        tasks = Task.objects.filter(
            user=user.id, is_expired_check=False, completed=False
        )
        for task in tasks:
            if now() > task.deadline:
                send_mail(
                    subject="Дедлайн задачи истёк",
                    message=f"Дедлайн задачи {task.name} истёк\nДля отмены рассылки перейдите по ссылке: http://127.0.0.1:8000/tasks/disable/expired/email/",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[
                        user.email,
                    ],
                    fail_silently=False,
                )
                task.is_expired_check = True
                task.save()


@app.task
def check_deadline():
    users = User.objects.filter(deadline_email=True)
    for user in users:
        tasks = Task.objects.filter(
            user=user, is_deadline_time_check=False, completed=False
        )
        for task in tasks:
            if (
                now() > (task.deadline - timedelta(hours=user.deadline_email_time))
                and not now() > task.deadline
            ):
                send_mail(
                    subject="Дедлайн задачи",
                    message=f"Дедлайн задачи {task.name} истечет в {task.deadline}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[
                        user.email,
                    ],
                    fail_silently=False,
                )
                task.is_deadline_time_check = True
                task.save()
