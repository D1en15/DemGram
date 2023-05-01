from django.contrib import admin
from accounts import models

admin.site.register(models.EmailVerification)
admin.site.register(models.PasswordReset)


