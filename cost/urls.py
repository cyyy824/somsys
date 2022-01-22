from django.urls import path

from . import views

urlpatterns = [
    path('budget', views.BudgetListView.as_view(), name='budget_list'),
    path('budget/add', views.BudgetCreateView.as_view(),name='budget_create'),
    path('budget/update/<int:pk>', views.BudgetUpdateView.as_view(),name='budget_update'),
    path('budget/detail/<int:pk>', views.BudgetDetailView.as_view(),name='budget_detail'),

    path('pay', views.PayListView.as_view(), name='pay_list'),
    path('pay/update/<int:pk>', views.PayUpdateView.as_view(), name='pay_update'),
    path('pay/add', views.PayCreateView.as_view(), name='pay_create')
  #  path('pay', views.gridnode),
   
]