from django.db import models

from django import forms
from django.forms import widgets, ModelForm, ModelChoiceField, HiddenInput
from django.forms import ModelForm
from .models import Budget, BudgetYear, Pay
from accounts.models import OAUser, Department
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


# class PayForm1(forms.Form):
#     BUSINESSENTITY_CHOICES = (
#         (u'集团', u'集团'),
#         (u'管委会', u'管委会')
#     )
#     name = forms.CharField(max_length=128)
#     businessentity = forms.CharField(
#         max_length=6, choices=BUSINESSENTITY_CHOICES)
#     paydate = forms.DateTimeField()
#     transactor = forms.CharField(max_length=32)

#     amount = forms.DecimalField(max_digits=11, decimal_places=2)
#     remark = forms.CharField(max_length=256, blank=True)
#     budgetyear = ModelChoiceField(
#         label="预算年", queryset=BudgetYear.objects.all())
#     budget = forms.ModelChoiceField(label=r'预算')

#     def __init__(self, *args, **kwargs):
#         if 'budgetyear' in self.data:
#             try:
#                 yearid = int(self.data.get('budgetyear'))
#                 self.fields['budget'].queryset = Budget.objects.filter(
#                     year_id=yearid)
#             except (ValueError, TypeError):
#                 pass


class PayForm(ModelForm):
    budgetyear = ModelChoiceField(
        label="预算年", queryset=BudgetYear.objects.all())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PayForm, self).__init__(*args, **kwargs)
        project = self.initial.get('project')
        print(self.initial)

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
        self.fields["project"].queryset = Project.objects.filter(
            department=self.user.department)

        self.fields['remark'].widget.attrs.update({"class": "form-control"})

        print(self.initial)
        self.initial['project'] = project.id
        budgetid = self.initial.get('budget')
        if budgetid is not None:
            budget = Budget.objects.get(pk=budgetid)
            #self.budgetyear = budget.year
            self.initial['budgetyear'] = budget.year
            self.fields['budget'].queryset = Budget.objects.filter(
                year=budget.year)
        else:
            self.fields['budget'].queryset = Budget.objects.none()

        # elif self.instance.pk:
        #    self.fields['budget'].queryset = self.instance.country.city_set.order_by('name')

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
