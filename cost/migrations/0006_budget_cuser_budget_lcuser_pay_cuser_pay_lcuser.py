# Generated by Django 4.0.1 on 2022-01-22 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cost', '0005_alter_budget_remark_alter_pay_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='cuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_budgets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='budget',
            name='lcuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='change_budgets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pay',
            name='cuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_pays', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pay',
            name='lcuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='change_pays', to=settings.AUTH_USER_MODEL),
        ),
    ]
