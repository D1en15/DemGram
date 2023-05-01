from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import timedelta


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    expired_email = models.BooleanField(default=False)
    deadline_email = models.BooleanField(default=False)
    deadline_email_time = models.PositiveIntegerField(blank=True, null=True, default=12)


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expired = models.DateTimeField()

    def __str__(self):
        return f"Verification for {self.user.username}"

    def send_verification_email(self):
        email = self.user.email
        link = reverse(
            "accounts:email_verification", kwargs={"email": email, "code": self.code}
        )
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Подтверждение для {self.user.username}"
        message = f"Для подтверждения учетной записи  для {self.user.username} перейдите по сслыке: {verification_link}"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if (now()) >= self.expired else False


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expired = models.DateTimeField()

    def send_reset_email(self):
        link = reverse(
            "accounts:password_reset",
            kwargs={"code": self.code, "email": self.user.email},
        )
        reset_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Сброс пароля для {self.user.username}"
        message = f"Чтобы сбросить пароль перейдите по ссылке: {reset_link}\nЕсли это были не вы, никак не реагируйте"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() > self.expired else False
