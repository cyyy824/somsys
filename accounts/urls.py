from django.urls import path

from . import views

urlpatterns = [
    path('login', views.OAUserLoginView.as_view(), name='login'),
    path('register', views.OARegisterView.as_view(), name='register'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('changepw', views.ChangePasswordView.as_view(), name='changepw'),
    path('ukanban', views.PersonKanbanView.as_view(), name='ukanban')


]
