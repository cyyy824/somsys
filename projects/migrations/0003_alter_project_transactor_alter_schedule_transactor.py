# Generated by Django 4.0.1 on 2023-10-10 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from accounts.models import OAUser

def schedule_cov(apps, schema_editor):
    Schedule = apps.get_model("projects", "Schedule")
    for schedule in  Schedule.objects.all():
        transactor = schedule.transactor
        user = OAUser.objects.filter(realname=transactor).first()
        schedule.transactor = user.id
        schedule.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_alter_project_transactor'),
    ]

    operations = [
        migrations.RunPython(schedule_cov),
        migrations.AlterField(
            model_name='project',
            name='transactor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactor_projects', to=settings.AUTH_USER_MODEL, verbose_name='经办人'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='transactor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactor_schedules', to=settings.AUTH_USER_MODEL, verbose_name='经办人'),
        ),
    ]
