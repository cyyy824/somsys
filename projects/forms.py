from django.db import models
import django.forms
from django.forms import ModelForm
from .models import Project, Schedule

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name','businessentity','task_state','amount','transactor','parent_project','remark']

        labels = {
            'name':'项目名',
            'businessentity':'单位主体',
            'task_state':'状态',
            'amount':'金额',
            'remark':'备注',
            'transactor':'经办人',
            'parent_project':'父项目',
        }



class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['project','name','transactor','content','remark']

        labels = {
            'name':'事项',
            'remark':'备注',
            'transactor':'经办人',
            'project':'项目',
            'content':'内容',
        }
    def __init__(self, *args, **kwargs):
         super(ScheduleForm, self).__init__(*args, **kwargs)
         self.fields['project'].disabled = True

