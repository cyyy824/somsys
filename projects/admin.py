from django.contrib import admin
from .models import Project, Schedule


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'businessentity', 'task_state',
                    'transactor', 'amount', 'lcdate', 'cuser', 'department')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'transactor', 'isfin',
                    'progress', 'deadline', 'project')


# Register your models here.
admin.site.register(Project, ProjectAdmin)

admin.site.register(Schedule, ScheduleAdmin)
