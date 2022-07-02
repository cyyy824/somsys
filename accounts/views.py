from django.shortcuts import render
from django.views.generic import FormView, RedirectView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
# Create your views here.


class OAUserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('projects:project_list')


class LogoutView(RedirectView):
    url = '/accounts/login'

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
            user.save(True)
            return HttpResponseRedirect(reverse_lazy('project_list'))
        else:
            return self.render_to_response({
                'form': form
            })
