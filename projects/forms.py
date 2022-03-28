from django.db import models
import django.forms
from django.forms import ModelForm
from .models import Project, Schedule


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({"class": "form-control"})
        self.fields['businessentity'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['task_state'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['content'].widget.attrs.update({"class": "form-control"})
        self.fields['amount'].widget.attrs.update({"class": "form-control"})
        self.fields['transactor'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['parent_project'].widget.attrs.update(
            {"class": "form-control"})
        self.fields["parent_project"].queryset = Project.objects.filter(
            department=self.user.department)
        self.fields['remark'].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Project
        fields = ['name', 'businessentity', 'task_state', 'content', 'amount',
                  'transactor', 'parent_project', 'remark', 'lcuser']

        labels = {
            'name': '项目名',
            'businessentity': '单位主体',
            'task_state': '状态',
            'amount': '金额',
            'content': '内容',
            'remark': '备注',
            'transactor': '经办人',
            'parent_project': '父项目',
        }
        widgets = {'lcuser': django.forms.HiddenInput()}


class ScheduleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['project'].widget.attrs.update({"class": "form-control"})
        self.fields['name'].widget.attrs.update({"class": "form-control"})
        self.fields['task_type'].widget.attrs.update({"class": "form-control"})
        self.fields['transactor'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['content'].widget.attrs.update({"class": "form-control"})
        self.fields['remark'].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Schedule
        fields = ['project', 'name', 'task_type', 'transactor',
                  'content', 'remark', 'lcuser']

        labels = {
            'name': '事项',
            'task_type': '类型',
            'remark': '备注',
            'transactor': '经办人',
            'project': '项目',
            'content': '内容',
        }
        widgets = {'lcuser': django.forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['project'].disabled = True
