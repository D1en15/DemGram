from accounts.models import User, EmailVerification
from django.utils.timezone import now
import uuid
from datetime import timedelta

def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    expired = now() + timedelta(48)
    record = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expired=expired)
    record.send_verification_email()