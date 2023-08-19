from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import OAUser, Structure
# Register your models here.


class OAUserAdmin(UserAdmin):
    model = OAUser
    fieldsets = (
        (None,{'fields': ('username','password','realname','department')}),
        ('权限',{'fields': ('is_active','is_staff','is_superuser')})
    )

    list_display = ('username','realname','department','is_active','is_superuser')
    
    #UserAdmin.fieldsets + (
    #    (None, {'fields': ('department', 'realname')}),
    #)


admin.site.register(OAUser, OAUserAdmin)
admin.site.register(Structure)
