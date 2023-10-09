from django.shortcuts import render
from django.conf import settings
from django.views.generic import FormView, RedirectView
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from .models import Structure, OAUser
from projects.models import Project, Schedule
from cost.models import Pay
from django.db.models import Q, Sum
# Create your views here.


class OAUserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('projects:project_list')


class LogoutView(RedirectView):
    url = settings.LOGIN_URL  # '/accounts/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('project_list')
    template_name = 'accounts/changepassword.html'


class OARegisterView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        if form.is_valid():

            user = form.save(False)
            # user.is_active = False
            user.save(True)
            return HttpResponseRedirect(reverse_lazy('project_list'))
        else:
            return self.render_to_response({
                'form': form
            })


class PersonKanbanView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/person_kanban.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        u_id = self.kwargs.get('u_id', 0)
        if u_id > 0:
            user = OAUser.objects.get(pk=u_id)
        else:
            user = self.request.user

        if not user:
            return context

        projects = Project.objects.filter(
            Q(department=user.department),
            Q(transactor=user.realname))

        schedules = Schedule.objects.filter(
            Q(department=user.department),
            Q(transactor=user.realname))

        pays = Pay.objects.filter(
            Q(department=user.department),
            Q(transactor=user.realname))

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


class PersonKanbantoView(PersonKanbanView):
    template_name = 'accounts/person_kanbanto.html'

    