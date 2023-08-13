from django.urls import path

from . import views

urlpatterns = [
    path('budget', views.BudgetListView.as_view(), name='budget_list'),
    path('budget/<int:year>', views.BudgetListView.as_view(), name='budget_list'),
    path('budget/add', views.BudgetCreateView.as_view(), name='budget_create'),
    path('budget/update/<int:pk>',
         views.BudgetUpdateView.as_view(), name='budget_update'),
    path('budget/detail/<int:pk>',
         views.BudgetDetailView.as_view(), name='budget_detail'),
    path('budget/ajax/load_budget', views.load_budgets, name='load_budget'),

    path('pay', views.PayListView.as_view(), name='pay_list'),
    path('pay/update/<int:pk>', views.PayUpdateView.as_view(), name='pay_update'),
    path('pay/add', views.PayCreateView.as_view(), name='pay_create'),
    path('pay/add/<int:project_id>',
         views.PayCreateView.as_view(), name='pay_create'),
    path('pay/search', views.PaySearchView.as_view(), name='pay_search'),
    path('pay/exportpays', views.export_pays, name='export_pays')
    #  path('pay', views.gridnode),

]
