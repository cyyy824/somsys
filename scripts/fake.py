import os
import pathlib
import random
import sys
import datetime

import django
import faker
from django.utils import timezone

back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "somsys.settings")
    django.setup()

    from cost.models import Budget, Pay, BudgetYear
    from projects.models import Project, Schedule
    from accounts.models import OAUser

    fake = faker.Faker(locale='zh_CN')

    BudgetYear.objects.all().delete()
    Pay.objects.all().delete()
    Budget.objects.all().delete()

    Schedule.objects.all().delete()
    Project.objects.all().delete()

    for _ in range(10):
        user = OAUser.objects.create(
            username=fake.romanized_name(), realname=fake.name(), password='111111')

    for i in range(2):
        budget_year = BudgetYear.objects.create(year=2021+i)

    for _ in range(20):
        budget_year = BudgetYear.objects.order_by('?').first()
        budget = Budget.objects.create(name=fake.sentence(),
                                       businessentity='管委会',
                                       year=budget_year,
                                       amount=random.randint(1, 5000)*10000)

    for _ in range(100):
        budget = Budget.objects.order_by('?').first()
        pay = Pay.objects.create(name=fake.sentence(),
                                 businessentity='管委会',
                                 paydate=fake.date_time_between(
                                     start_date='-1y', end_date="-30d"),
                                 transactor=fake.name(),
                                 amount=random.randint(1, 2000)*10000,
                                 budget=budget)

    TAKESTATE = ['前期', '设计', '招标', '合同流程', '实施', '完结', '暂停']
    for _ in range(100):
        project = Project.objects.create(name=fake.sentence(),
                                         businessentity='管委会',
                                         task_state=TAKESTATE[random.randint(
                                             0, len(TAKESTATE)-1)],
                                         transactor=fake.name(),
                                         amount=random.randint(1, 200)*10000,
                                         content=fake.text())

    for _ in range(200):
        project = Project.objects.order_by('?').first()
        schedule = Schedule.objects.create(name=fake.sentence(),
                                           transactor=fake.name(),
                                           content=fake.text(),
                                           project=project)
