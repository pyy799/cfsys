from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from webapp.models import UserProfile
admin.site.register(UserProfile, UserAdmin)
# Register your models here.
