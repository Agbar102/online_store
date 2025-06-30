from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import UserActivity

User = get_user_model()

admin.site.register(User)

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'method', 'path', 'time_start', 'data')
