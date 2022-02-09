from django.db import models
import django.forms
from django.forms import widgets
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
        widgets = {'lcuser': django.forms.HiddenInput()}


class PayForm(ModelForm):
    budgetyear = django.forms.ModelChoiceField(
        label="预算年", queryset=BudgetYear.objects.all())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PayForm, self).__init__(*args, **kwargs)

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

        self.fields['budget'].queryset = Budget.objects.none()

        if 'budgetyear' in self.data:
            try:
                yearid = int(self.data.get('budgetyear'))
                self.fields['budget'].queryset = Budget.objects.filter(
                    year_id=yearid)
            except (ValueError, TypeError):
                pass
        # elif self.instance.pk:
        #    self.fields['budget'].queryset = self.instance.country.city_set.order_by('name')

    class Meta:
        model = Pay
        fields = ['name', 'businessentity', 'paydate', 'transactor',
                  'amount', 'budgetyear', 'budget', 'project', 'remark', 'lcuser']

        labels = {
            'name': '支付项',
            'businessentity': '单位主体',
            'paydate': '预算年',
            'transactor': '经办人',
            'amount': '金额',
            'budget': '预算',
            'project': '项目',
            'remark': '备注'
        }

        widgets = {'lcuser': django.forms.HiddenInput()}
