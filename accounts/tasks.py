from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from task_manager.celery import app
from accounts.models import User, EmailVerification, PasswordReset
from tasks.models import Task
import uuid
from django.utils.timezone import now



@app.task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    expired = now() + timedelta(hours=48)
    record = EmailVerification.objects.create(
        user=user, code=uuid.uuid4(), expired=expired
    )
    record.send_verification_email()



@app.task
def send_password_reset_email(user):
    user = User.objects.get(id=user.id)
    expired = now() + timedelta(hours=3)
    record = PasswordReset.objects.create(
        user=user, code=uuid.uuid4(), expired=expired
    )
    record.send_reset_email()
    
    
@app.task
def check_expired():
    verifications = EmailVerification.objects.all()
    for verification in verifications:
        if verification.is_expired():
            verification.delete()
    resets = PasswordReset.objects.all()
    for reset in resets:
        if reset.is_expired():
            reset.delete()