from django.contrib import admin
from tasks.models import *
from accounts.models import User

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Category)

