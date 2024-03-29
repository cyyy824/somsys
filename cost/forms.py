from django.db import models

from django import forms
from django.forms import widgets, ModelForm, ModelChoiceField, HiddenInput
from django.forms import ModelForm
from .models import Budget, BudgetYear, Pay
from accounts.models import OAUser, Structure
from projects.models import Project


class BudgetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({"class": "form-control"})
        self.fields['businessentity'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['year'].widget.attrs.update({"class": "form-control"})
        self.fields['amount'].widget.attrs.update({"class": "form-control"})
        self.fields['remark'].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Budget
        fields = ['name', 'businessentity',
                  'year', 'amount', 'remark', 'lcuser']

        labels = {
            'name': '预算项',
            'businessentity': '单位主体',
            'year': '预算年',
            'amount': '金额',
            'remark': '备注'
        }
        widgets = {'lcuser': HiddenInput()}


class PayForm(ModelForm):
    budgetyear = ModelChoiceField(
        label="预算年", queryset=BudgetYear.objects.all())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PayForm, self).__init__(*args, **kwargs)
        project = self.initial.get('project')

        self.fields['name'].widget.attrs.update({"class": "form-control"})
        self.fields['businessentity'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['paydate'].widget.attrs.update({"class": "form-control"})
        self.fields['transactor'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['amount'].widget.attrs.update({"class": "form-control"})
        self.fields['budgetyear'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['budget'].widget.attrs.update({"class": "form-control"})

        self.fields['project'].widget.attrs.update({"class": "form-control"})

        self.fields['remark'].widget.attrs.update({"class": "form-control"})

        self.fields["project"].queryset = Project.objects.none()
        self.fields['budget'].queryset = Budget.objects.none()
     #   if 'project' in self.data:
        self.fields["project"].queryset = Project.objects.all()  # filter(
        #     department=self.user.department)

        if 'budgetyear' in self.data:
            try:
                yearid = int(self.data.get('budgetyear'))
                self.fields['budget'].queryset = Budget.objects.filter(
                    year_id=yearid)
            except (ValueError, TypeError):
                pass

        budgetid = self.initial.get('budget')

        if budgetid is not None:
            budget = Budget.objects.get(pk=budgetid)
            #self.budgetyear = budget.year
            self.initial['budgetyear'] = budget.year
            self.fields['budget'].queryset = Budget.objects.filter(
                year=budget.year)

    class Meta:
        model = Pay
        fields = ['name', 'businessentity', 'paydate', 'transactor',
                  'amount', 'budgetyear', 'budget', 'project', 'remark', 'lcuser']

        labels = {
            'name': '支付项',
            'businessentity': '单位主体',
            'paydate': '支付时间',
            'transactor': '经办人',
            'amount': '金额',
            'budget': '预算',
            'project': '项目',
            'remark': '备注'
        }

        widgets = {'lcuser': HiddenInput()}
