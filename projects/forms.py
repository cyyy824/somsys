
from django.db import models
from django import forms
from django.forms import ModelForm
from .models import Project, Schedule


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})

        self.fields["parent_project"].queryset = Project.objects.filter(
            department=self.user.department)

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
        widgets = {'lcuser': forms.HiddenInput()}


class DateInput(forms.DateInput):
    input_type = 'date'


class ScheduleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ScheduleForm, self).__init__(*args, **kwargs)

        # for filed in self.fields.values():
        #   filed.widget.attrs.update({'class': 'form-control'})
        self.fields['project'].disabled = True
        self.fields['project'].widget.attrs.update({"class": "form-control"})
        self.fields['name'].widget.attrs.update({"class": "form-control"})
        self.fields['task_type'].widget.attrs.update({"class": "form-control"})
        self.fields['transactor'].widget.attrs.update(
            {"class": "form-control"})
        # self.fields['isfin'].widget.attrs.update(
        #    {"class": "form-control"})
        self.fields['progress'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['content'].widget.attrs.update({"class": "form-control"})
        self.fields['remark'].widget.attrs.update({"class": "form-control"})

        self.fields["project"].queryset = Project.objects.filter(
            department=self.user.department)

    class Meta:
        model = Schedule
        fields = ['project', 'name', 'task_type', 'transactor', 'iskey', 'isfin', 'progress', 'deadline',
                  'content', 'remark', 'lcuser']
        widgets = {
            'deadline': DateInput(),
        }

        labels = {
            'name': '事项',
            'task_type': '类型',
            'remark': '备注',
            'transactor': '经办人',
            'project': '项目',
            'content': '内容',
        }
        widgets = {'lcuser': forms.HiddenInput()}
