from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Budget, Pay
from .forms import BudgetForm, PayForm
from django.db.models import Sum
import datetime

# Create your views here.


class BudgetListView(LoginRequiredMixin, ListView):
    template_name = 'cost/budget_list.html'
    model = Budget
    context_object_name = 'budget_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        allpay = {}
        for budget in context['budget_list']:
            aa = budget.pays.all().aggregate(Sum('amount'))
            allpay[budget.id] = aa['amount__sum']

        context['allpay'] = allpay

        return context


class BudgetCreateView(LoginRequiredMixin, CreateView):
    template_name = 'cost/budget_create.html'
    model = Budget
    form_class = BudgetForm
    success_url = reverse_lazy('budget_list')

    def get_form_kwargs(self):
        kwargs = super(BudgetCreateView, self).get_form_kwargs()

        kwargs.update(
            {'initial': {'cdate': datetime.date.today(
            ), 'lcdate': datetime.date.today(), 'remark': ''}}
        )
        return kwargs


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'cost/budget_update.html'
    model = Budget
    form_class = BudgetForm
    context_object_name = 'budget'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('budget_detail', kwargs={'pk': pk})


class BudgetDetailView(LoginRequiredMixin, DetailView):
    template_name = 'cost/budget_detail.html'
    model = Budget
    context_object_name = 'budget'


class PayListView(LoginRequiredMixin, ListView):
    template_name = 'cost/pay_list.html'
    model = Pay
    context_object_name = 'pay_list'


class PayCreateView(LoginRequiredMixin, CreateView):
    template_name = 'cost/pay_create.html'
    model = Pay
    form_class = PayForm
    success_url = reverse_lazy('pay_list')

    def get_form_kwargs(self):
        kwargs = super(PayCreateView, self).get_form_kwargs()

        kwargs.update(
            {'initial': {'paydate': datetime.date.today(), 'remark': ''}}
        )
        return kwargs


class PayUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'cost/pay_update.html'
    model = Pay
    form_class = PayForm
    context_object_name = 'pay'
    success_url = reverse_lazy('pay_list')
