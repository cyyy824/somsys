from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import OAUser
# Register your models here.

# class OAUserAdmin(admin.ModelAdmin):


admin.site.register(OAUser, UserAdmin)
