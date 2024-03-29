# Generated by Django 4.0.1 on 2023-10-10 05:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from accounts.models import OAUser
#from SOMSYS. import Project

def covxx(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    for project in  Project.objects.all():
        transactor = project.transactor
        user = OAUser.objects.filter(realname=transactor).first()
        project.transactor = user.id
        project.save()



class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        
        migrations.RunPython(covxx),
        migrations.AlterField(
            model_name='project',
            name='transactor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactors', to=settings.AUTH_USER_MODEL, verbose_name='经办人'),
        ),
    ]
