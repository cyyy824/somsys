from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import OAUser, Structure
# Register your models here.


class OAUserAdmin(UserAdmin):
    model = OAUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('department', 'realname')}),
    )


admin.site.register(OAUser, OAUserAdmin)
admin.site.register(Structure)
