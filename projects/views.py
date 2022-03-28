from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.forms import ProjectForm, ScheduleForm

from .models import Project, Schedule
from accounts.models import Department, OAUser
from django.db.models import Q
import json
from django.core import serializers
# Create your views here.


def load_projects(request):

    kw = request.GET.get('q', '')
    data = {}
    if kw != '':
        user = request.user
        projects = Project.objects.filter(
            Q(department=user.department), Q(name__contains=kw))
        data["results"] = [{"id": lt.pk, "text": lt.name} for lt in projects]
    data["pagination"] = {"more": True}
    return HttpResponse(json.dumps(data))


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'projects/project_list.html'
    model = Project
    context_object_name = 'project_list'

    page_type = ''
    paginate_by = 20
    page_kwarg = 'page'

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(
            page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

    def get(self, request, *args, **kwargs):
        state = self.kwargs.get('state')

        states = ['all', 'fin', 'unfin']
        if state == None or state not in states:
            state = 'unfin'
            return HttpResponseRedirect(reverse_lazy('project_list', kwargs={'state': state}))

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        state = self.kwargs.get('state', 'unfin')
        if state == 'fin':
            new_context = Project.objects.filter(
                Q(task_state=u'完结'), Q(department=user.department)).order_by('-cdate')
        elif state == 'unfin':
            new_context = Project.objects.filter(
                ~Q(task_state=u'完结'), Q(department=user.department)).order_by('-cdate')
        else:
            new_context = Project.objects.filter(
                department=user.department).order_by('-cdate')
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        states = [['all', reverse('project_list', kwargs={'state': 'all'}), False, '全部'],
                  ['fin', reverse('project_list', kwargs={
                                  'state': 'fin'}), False, '已完成'],
                  ['unfin', reverse('project_list', kwargs={'state': 'unfin'}), False, '未完成']]
        for state in states:
            if state[0] == self.kwargs['state']:
                state[2] = True
                break
        context['states'] = states
        context['state'] = self.kwargs['state']
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy('project_list')
    model = Project
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        user = self.request.user
        pk = self.kwargs.get('parentpk')
        kwargs.update({'user': self.request.user})
        kwargs.update(
            {'initial': {'transactor': user.realname}}
        )
        if pk != None:
            try:
                pp = Project.objects.get(id=pk)
                kwargs.update(
                    {'initial': {'parent_project': pp, 'transactor': user.realname}}
                )
            except Project.DoesNotExist:
                pass
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        project = form.save(False)
        project.cuser = user
        project.lcuser = user
        project.department = user.department
        project.save(True)
        return HttpResponseRedirect(self.success_url)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = 'projects/project_detail.html'
    model = Project
    context_object_name = 'project'


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'projects/project_update.html'
    model = Project
    form_class = ProjectForm
    context_object_name = 'project'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('project_detail', kwargs={'pk': pk})

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        user = self.request.user
        kwargs.update({'user': user})
        kwargs.update(
            {'initial': {'lcuser': user}}
        )
        return kwargs


class ScheduleListView(LoginRequiredMixin, ListView):
    template_name = 'projects/schedule_list.html'
    model = Schedule
    context_object_name = 'schedule_list'
    #ordering = ['-lcdate']

    page_type = ''
    paginate_by = 30
    page_kwarg = 'page'

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(
            page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

    def get_queryset(self):
        user = self.request.user
        new_context = Schedule.objects.filter(
            department=user.department).order_by('-lcdate')
        return new_context


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'projects/schedule_create.html'
    model = Schedule
    form_class = ScheduleForm

    def get_success_url(self):
        pk = self.kwargs['project_id']
        return reverse_lazy('project_detail', kwargs={'pk': pk})

    def get_form_kwargs(self):
        kwargs = super(ScheduleCreateView, self).get_form_kwargs()
        project_id = self.kwargs['project_id']

        if project_id:
            project = Project.objects.get(id=project_id)
            # 进入网页，该字段值：{'initial': {}, 'prefix': None, 'instance': None}
            user = self.request.user
            kwargs.update(
                # 给表单的phase字段传递外键实例
                {'initial': {'project': project, 'transactor': user.realname}}
            )
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        schedule = form.save(False)
        schedule.cuser = user
        schedule.lcuser = user
        schedule.department = user.department
        schedule.save(True)
        return HttpResponseRedirect(self.get_success_url())


class ScheduleDetailView(LoginRequiredMixin, DetailView):
    template_name = 'projects/schedule_detail.html'
    model = Schedule
    context_object_name = 'schedule'


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'projects/schedule_update.html'
    model = Schedule
    form_class = ScheduleForm
    context_object_name = 'schedule'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('schedule_detail', kwargs={'pk': pk})

    def get_form_kwargs(self):
        kwargs = super(ScheduleUpdateView, self).get_form_kwargs()
        user = self.request.user

        kwargs.update(
            {'initial': {'lcuser': user}}
        )
        return kwargs
