from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('add', views.ProjectCreateView.as_view(), name='project_create'),
    path('add/<int:parentpk>', views.ProjectCreateView.as_view(), name='project_create'),
    path('detail/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('update/<int:pk>', views.ProjectUpdateView.as_view(), name='project_update'),

    path('schedule', views.ScheduleListView.as_view(), name='schedule_list'),
    path('<int:project_id>/addschedule',
         views.ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/detail/<int:pk>',
         views.ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule/update/<int:pk>',
         views.ScheduleUpdateView.as_view(), name='schedule_update'),

     path('<slug:state>', views.ProjectListView.as_view(), name='project_list'),
    #   path('schedule', views.ScheduleListView.as_view(), name='pay_list'),schedule
    #   path('schedule/add', views.ScheduleCreateView.as_view(), name='pay_create')
    #  path('pay', views.gridnode),

]
