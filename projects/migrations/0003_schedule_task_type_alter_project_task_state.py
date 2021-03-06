# Generated by Django 4.0.1 on 2022-03-28 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_task_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='task_type',
            field=models.CharField(choices=[('进度', '进度'), ('付款', '付款'), ('招采审核', '招采审核'), ('方案评审会', '方案评审会'), ('其他', '其他')], default='其他', max_length=20),
        ),
        migrations.AlterField(
            model_name='project',
            name='task_state',
            field=models.CharField(choices=[('前期', '前期'), ('设计', '设计'), ('招标', '招标'), ('合同流程', '合同流程'), ('实施', '实施'), ('验收完成', '验收完成'), ('完结', '完结'), ('暂停', '暂停')], max_length=20),
        ),
    ]
