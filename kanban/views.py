from django.shortcuts import render
from django.conf import settings
from django.views.generic import FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView
from projects.models import Project, Schedule
from cost.models import Pay
from django.db.models import Q, Sum
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.


class PersonKanbanView(LoginRequiredMixin, TemplateView):
    template_name = 'kanban/personto.html'

    def get_projects(self, user: User):
        return Project.objects.filter(
            Q(department=user.department),
            Q(transactor=user))

    def get_schedules(self, user: User):
        return Schedule.objects.filter(
            Q(department=user.department),
            Q(transactor=user))

    def get_pays(self, user: User):
        return Pay.objects.filter(
            Q(department=user.department),
            Q(transactor=user))

    def attach_context(self, user, projects, schedules, pays, context):
        pay_value = pays.aggregate(Sum('amount'))['amount__sum'] or 0
        projectnum = projects.count
        projectfin = projects.filter(task_state=u'完成').count
        projectufin = projects.exclude(task_state=u'完成').count

        tasknum = schedules.count
        taskfin = schedules.filter(isfin=True).count
        taskufin = schedules.filter(isfin=False).count

        paynum = pays.count

        projects = projects[:5]
        schedules = schedules[:5]
        pays = pays[:5]

        context['touser'] = user
        context['paynum'] = paynum
        context['pay_value'] = pay_value
        context['projectnum'] = projectnum
        context['projectfin'] = projectfin
        context['projectufin'] = projectufin
        context['schedulenum'] = tasknum
        context['schedulefin'] = taskfin
        context['scheduleufin'] = taskufin

        context['projects'] = projects
        context['schedules'] = schedules
        context['pays'] = pays

        cprogresses = {}
        for cproject in projects:
            aa = cproject.schedules.filter(
                isfin=True).aggregate(Sum('progress'))
            cprogresses[cproject.id] = aa['progress__sum'] or 0
        context['cprogresses'] = cprogresses

        sexpireds = {}
        for schedule in schedules:
            sexpireds[schedule.id] = schedule.is_expired()
        context['sexpireds'] = sexpireds
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # -1 则默认为查看自己的看板数据
        u_id = self.kwargs.get('u_id', -1)
        user = self.request.user if u_id < 0 else User.objects.get(pk=u_id)
        if not user:
            return context

        projects = self.get_projects(user)
        schedules = self.get_schedules(user)
        pays = self.get_pays(user)

        context = self.attach_context(user, projects, schedules, pays, context)

        return context


class DepmentKanbanView(PersonKanbanView):
    template_name = 'kanban/depment.html'

    def get_projects(self, user: User):
        return Project.objects.filter(department=user.department)

    def get_schedules(self, user: User):
        return Schedule.objects.filter(department=user.department)

    def get_pays(self, user: User):
        return Pay.objects.filter(department=user.department)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        projects = self.get_projects(user)
        schedules = self.get_schedules(user)
        pays = self.get_pays(user)

        projects = self.get_projects(user)
        schedules = self.get_schedules(user)
        pays = self.get_pays(user)

        context = self.attach_context(user, projects, schedules, pays, context)
        return context
