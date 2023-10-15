from django.urls import path

from . import views

urlpatterns = [
    path('', views.PersonKanbanView.as_view(), name='ukanban'),
    path('<int:u_id>', views.PersonKanbanView.as_view(), name='ukanbanto'),
    path('dep/', views.DepmentKanbanView.as_view(), name='depkanban'),
]
