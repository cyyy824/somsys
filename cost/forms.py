from django.db import models
import django.forms
from django.forms import widgets
from django.forms import ModelForm
from .models import Budget, BudgetYear, Pay


class BudgetForm(ModelForm):
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
    budgetyear = django.forms.ModelChoiceField(label="出版社", queryset=BudgetYear.objects.all())

    def __init__(self, *args, **kwargs):
        super(PayForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget = widgets.TextInput(attrs={"class": "form-control"})
        self.fields['budget'].queryset = Budget.objects.none()

    class Meta:
        model = Pay
        fields = ['name', 'businessentity', 'paydate', 'transactor',
                  'amount', 'project', 'budget', 'remark', 'lcuser']

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
