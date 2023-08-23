from audioop import reverse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from accounts.models import Structure, OAUser
from projects.models import Project
from .models import Budget, Pay, BudgetYear
from .forms import BudgetForm, PayForm
from django.db.models import Sum
from django.db.models import Q
import datetime
import csv

# Create your views here.


def load_budgets(request):
    user = request.user
    year_id = request.GET.get('yearid')
    budgets = Budget.objects.filter(
        Q(year_id=year_id), Q(department=user.department))
    return render(request, 'cost/budget_dropdown_list_options.html', {'budgets': budgets})


class BudgetListView(LoginRequiredMixin, ListView):
    template_name = 'cost/budget_list.html'
    model = Budget
    context_object_name = 'budget_list'

    def get(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        if year == None:
            nowyear = datetime.datetime.now().strftime('%Y')
            return HttpResponseRedirect(reverse_lazy('budget_list', kwargs={'year': nowyear}))

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        year = self.kwargs['year']
        yn = BudgetYear.objects.get(year=year)
        new_context = Budget.objects.filter(
            Q(year=yn), Q(department=user.department))
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 加入支出统计
        allpay = {}
        for budget in context['budget_list']:
            aa = budget.pays.all().aggregate(Sum('amount'))
            allpay[budget.id] = aa['amount__sum']

        years = [[year.year, reverse('budget_list', kwargs={
                                     'year': year.year}), False] for year in BudgetYear.objects.all()]
        for year in years:
            if year[0] == self.kwargs['year']:
                year[2] = True
                break

        context['years'] = years

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

    def form_valid(self, form):

        user = self.request.user
        budget = form.save(False)
        budget.cuser = user
        budget.lcuser = user
        budget.department = user.department
        budget.save(True)
        return HttpResponseRedirect(self.success_url)


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'cost/budget_update.html'
    model = Budget
    form_class = BudgetForm
    context_object_name = 'budget'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('budget_detail', kwargs={'pk': pk})

    def get_form_kwargs(self):
        kwargs = super(BudgetUpdateView, self).get_form_kwargs()
        user = self.request.user

        kwargs.update(
            {'initial': {'lcuser': user}}
        )
        return kwargs


class BudgetDetailView(LoginRequiredMixin, DetailView):
    template_name = 'cost/budget_detail.html'
    model = Budget
    context_object_name = 'budget'


class PaySearchView(LoginRequiredMixin, ListView):
    template_name = 'cost/pay_search.html'
    model = Pay
    context_object_name = 'pay_list'

    def get_queryset(self):
        user = self.request.user
        new_context = None
        keychar = self.request.GET.get('name', '')
        if keychar != None:
            new_context = Pay.objects.filter(
                Q(department=user.department),
                Q(name__contains=keychar) |
                Q(transactor__contains=keychar)
            ).order_by('-paydate')
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        keychar = self.request.GET.get('name', '')
        context['keychar'] = keychar
        return context

class MyPayListView(LoginRequiredMixin, ListView):
    template_name = 'cost/pay_my_list.html'
    model = Pay
    context_object_name = 'pay_list'

    page_type = ''
    paginate_by = 20
    page_kwarg = 'page'
    # ordering = ['-paydate']
    # queryset = Pay.objects.order_by('-paydate')

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(
            page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

    def get_queryset(self):
        user = self.request.user
        new_context = Pay.objects.filter(
            department=user.department,transactor=user.realname).order_by('-paydate')
        return new_context

class PayListView(LoginRequiredMixin, ListView):
    template_name = 'cost/pay_list.html'
    model = Pay
    context_object_name = 'pay_list'

    page_type = ''
    paginate_by = 20
    page_kwarg = 'page'
    # ordering = ['-paydate']
    # queryset = Pay.objects.order_by('-paydate')

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(
            page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

    def get_queryset(self):
        user = self.request.user
        new_context = Pay.objects.filter(
            department=user.department).order_by('-paydate')
        return new_context


class PayCreateView(LoginRequiredMixin, CreateView):
    template_name = 'cost/pay_create.html'
    model = Pay
    form_class = PayForm
    success_url = reverse_lazy('pay_list')

    def get_form_kwargs(self):
        kwargs = super(PayCreateView, self).get_form_kwargs()

        project_id = self.kwargs.get('project_id')

        kwargs.update({'user': self.request.user})
        if project_id:
            project = Project.objects.get(id=project_id)
            # 进入网页，该字段值：{'initial': {}, 'prefix': None, 'instance': None}
            user = self.request.user
            kwargs.update(
                # 给表单的phase字段传递外键实例
                {'initial': {'paydate': datetime.date.today(), 'remark': '',
                             'project': project, 'transactor': user.realname}}
            )
        else:
            kwargs.update(
                {'initial': {'paydate': datetime.date.today(), 'remark': '',
                             'transactor': self.request.user.realname}}
            )
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        pay = form.save(False)
        pay.cuser = user
        pay.lcuser = user
        pay.department = user.department
        pay.save(True)
        return HttpResponseRedirect(self.success_url)


class PayUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'cost/pay_update.html'
    model = Pay
    form_class = PayForm
    context_object_name = 'pay'
    success_url = reverse_lazy('pay_list')

    def get_form_kwargs(self):
        kwargs = super(PayUpdateView, self).get_form_kwargs()
        user = self.request.user
        kwargs.update({'user': user})
        kwargs.update(
            {'initial': {'lcuser': user}}
        )

        return kwargs


@login_required
def export_pays(request):
    response = HttpResponse(content_type='text/csv')
    response.charset = 'utf-8-sig' if "Windows" in request.headers.get(
        'User-Agent') else 'utf-8'
    response['Content-Disposition'] = 'attachment; filename="pays.csv"'

    writer = csv.writer(response)
    user = request.user
    keychar = request.GET.get('name', '')
    pay_list = []
    if (keychar == ''):
        pay_list = Pay.objects.filter(
            department=user.department).order_by('-paydate')
    else:
        pay_list = Pay.objects.filter(
            Q(department=user.department),
            Q(name__contains=keychar) |
            Q(transactor__contains=keychar)
        ).order_by('-paydate')

    writer.writerow(['payname', 'businessentity', 'date',
                    'author', 'amount', 'budget', 'project'])
    for pay in pay_list:
        writer.writerow([pay.name, pay.businessentity, str(
            pay.paydate), pay.transactor, pay.amount, pay.budget])

    return response
