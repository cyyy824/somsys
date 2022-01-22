from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.forms import ProjectForm, ScheduleForm

from .models import Project, Schedule
# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'projects/project_list.html'
    model = Project
    context_object_name = 'project_list'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy('project_list')
    model = Project
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        user = self.request.user

        kwargs.update(
            {'initial': {'transactor': user.realname}}
        )
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        project = form.save(False)
        project.cuser = user
        project.lcuser = user
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

        kwargs.update(
            {'initial': {'lcuser': user}}
        )
        return kwargs


class ScheduleListView(LoginRequiredMixin, ListView):
    template_name = 'projects/schedule_list.html'
    model = Schedule
    context_object_name = 'project_list'


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
        schedule.save(True)
        return HttpResponseRedirect(self.success_url)


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
