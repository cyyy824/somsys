from django.contrib import admin
from .models import Budget, Pay, BudgetYear
# Register your models here.

admin.site.register(Budget)
admin.site.register(Pay)
admin.site.register(BudgetYear)
