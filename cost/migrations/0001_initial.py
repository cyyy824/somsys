# Generated by Django 4.0.1 on 2022-01-08 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('businessentity', models.CharField(choices=[('集团', '集团'), ('管委会', '管委会')], max_length=6)),
                ('year', models.DecimalField(decimal_places=0, max_digits=4)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('cdate', models.DateField()),
                ('lcdate', models.DateField()),
                ('remark', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('businessentity', models.CharField(choices=[('集团', '集团'), ('管委会', '管委会')], max_length=6)),
                ('paydate', models.DateField()),
                ('transactor', models.CharField(max_length=32)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('remark', models.TextField()),
                ('budget', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pays', to='cost.budget')),
            ],
        ),
    ]
