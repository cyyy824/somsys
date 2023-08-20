from django.urls import path

from . import views

urlpatterns = [

    path('add', views.ProjectCreateView.as_view(), name='project_create'),
    path('add/<int:parentpk>', views.ProjectCreateView.as_view(),
         name='project_create'),
    path('detail/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('update/<int:pk>', views.ProjectUpdateView.as_view(), name='project_update'),
    path('search', views.ProjectSearchView.as_view(), name='project_search'),

    path('ajax/load_projects', views.load_projects, name='load_project'),

    path('schedules', views.ScheduleListView.as_view(), name='schedule_list'),
    path('schedules/search', views.ScheduleSearchView.as_view(), name='schedule_search'),
    path('<int:project_id>/addschedule',
         views.ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/detail/<int:pk>',
         views.ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule/update/<int:pk>',
         views.ScheduleUpdateView.as_view(), name='schedule_update'),

    path('', views.ProjectListView.as_view(), name='project_list'),
    path('<slug:state>/<slug:main>', views.ProjectListView.as_view(), name='project_list'),
    path('', views.ProjectListView.as_view(), name='project_list'),
    #   path('schedule', views.ScheduleListView.as_view(), name='pay_list'),schedule
    #   path('schedule/add', views.ScheduleCreateView.as_view(), name='pay_create')
    #  path('pay', views.gridnode),
    path('schedule/exportschedules',
         views.export_schedules, name='export_schedules'),
    path('exportprojects', views.export_projects,name='export_projects')

]
