# Generated by Django 4.0.1 on 2023-08-05 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='名称')),
                ('type', models.CharField(choices=[('firm', '公司'), ('department', '部门')], default='department', max_length=20, verbose_name='类型')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.structure', verbose_name='父类架构')),
            ],
            options={
                'verbose_name': '组织架构',
                'verbose_name_plural': '组织架构',
            },
        ),
        migrations.AlterField(
            model_name='oauser',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='accounts.structure', verbose_name='部门'),
        ),
    ]
