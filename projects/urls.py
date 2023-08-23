from django.urls import path,include

from . import views
from . import views_ajax

urlpatterns = [

    path('add', views.ProjectCreateView.as_view(), name='project_create'),
    path('add/<int:parentpk>', views.ProjectCreateView.as_view(),
         name='project_create'),
    path('detail/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('update/<int:pk>', views.ProjectUpdateView.as_view(), name='project_update'),
    path('search', views.ProjectSearchView.as_view(), name='project_search'),

    path('ajax/load_projects', views_ajax.load_projects, name='load_project'),
    path('ajax/load_tasks_fin',
         views_ajax.load_tasks_dayfin, name='load_tasks_dayfin'),
    path('ajax/load_tasks_fin/<int:u_id>',
         views_ajax.load_tasksto_dayfin, name='load_tasksto_dayfin'),
    path('schedule/exportschedules',
         views.export_schedules, name='export_schedules'),
    path('exportprojects', views.export_projects, name='export_projects'),

    path('schedules', views.ScheduleListView.as_view(), name='schedule_list'),
    path('myschedules', views.MyScheduleListView.as_view(), name='myschedule_list'),
    path('schedules/search', views.ScheduleSearchView.as_view(),
         name='schedule_search'),
    path('<int:project_id>/addschedule',
         views.ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/detail/<int:pk>',
         views.ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule/update/<int:pk>',
         views.ScheduleUpdateView.as_view(), name='schedule_update'),
    path('my/', views.MyProjectListView.as_view(), name='myproject_list'),
    path('my/<slug:state>/<slug:main>', views.MyProjectListView.as_view(), name='myproject_list'),
    path('<slug:state>/<slug:main>',
         views.ProjectListView.as_view(), name='project_list'),
    path('', views.ProjectListView.as_view(), name='project_list'),
    
   
    

]
