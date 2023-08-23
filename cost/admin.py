from django.contrib import admin
from .models import Budget, Pay, BudgetYear
# Register your models here.


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'businessentity', 'amount', 'year', 'department')


class PayAdmin(admin.ModelAdmin):
    list_display = ('name', 'transactor', 'paydate',
                    'project', 'amount', 'department')


admin.site.register(Budget, BudgetAdmin)
admin.site.register(Pay, PayAdmin)
admin.site.register(BudgetYear)
