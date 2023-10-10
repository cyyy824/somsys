# Generated by Django 4.0.1 on 2023-10-10 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from accounts.models import OAUser

def pay_cov(apps, schema_editor):
    Pay = apps.get_model("cost", "Pay")
    for pay in  Pay.objects.all():
        transactor = pay.transactor
        user = OAUser.objects.filter(realname=transactor).first()
        pay.transactor = user.id
        pay.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cost', '0002_alter_budget_businessentity_alter_budgetyear_year'),
    ]

    operations = [
        migrations.RunPython(pay_cov),
        migrations.AlterField(
            model_name='pay',
            name='transactor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactor_pays', to=settings.AUTH_USER_MODEL, verbose_name='经办人'),
        ),
    ]
