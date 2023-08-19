import os
import pathlib
import random
import sys
import datetime

import django
import faker
from django.utils import timezone
from django.contrib.auth.hashers import make_password

back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "somsys.settings")
    django.setup()

    from cost.models import Budget, Pay, BudgetYear
    from projects.models import Project, Schedule
    from accounts.models import OAUser, Structure

    fake = faker.Faker(locale='zh_CN')

    print('----delete------')
    # BudgetYear.objects.all().delete()
    # Pay.objects.all().delete()
    # Budget.objects.all().delete()

    # Schedule.objects.all().delete()
    # Project.objects.all().delete()
    # Department.objects.all().delete()

    print('----create department------')
    Structure.objects.create(title='智慧办', type="department")
    Structure.objects.create(title='综合组', type="department")
    Structure.objects.create(title='市政组', type="department")

    print('----create user------')
    for _ in range(10):
        budget = Budget.objects.order_by('?').first()
        depart = Structure.objects.order_by('?').first()
        user = OAUser.objects.create(
            username=fake.romanized_name(), realname=fake.name(), password='111111', department=depart)

    print('----create budgetyear------')
    for i in range(4):
        budget_year = BudgetYear.objects.create(year=2021+i)

    print('----create budget------')
    for _ in range(20):
        depart = Structure.objects.order_by('?').first()
        budget_year = BudgetYear.objects.order_by('?').first()
        budget = Budget.objects.create(name=fake.sentence(),
                                       businessentity='管委会',
                                       year=budget_year,
                                       department=depart,
                                       amount=random.randint(1, 5000)*10000)

    print('----create pay------')
    for _ in range(100):

        budget = Budget.objects.order_by('?').first()
        pay = Pay.objects.create(name=fake.sentence(),
                                 businessentity='管委会',
                                 paydate=fake.date_time_between(
                                     start_date='-1y', end_date="-30d"),
                                 transactor=fake.name(),
                                 department=budget.department,
                                 amount=random.randint(1, 2000)*10000,
                                 budget=budget)

    print('----create project------')
    TAKESTATE = ['前期', '设计', '招标', '合同流程', '实施', '完结', '暂停']
    for _ in range(100):
        user = OAUser.objects.order_by('?').first()
        if user.username == "admin":
            continue
        project = Project.objects.create(name=fake.sentence(),
                                         businessentity='管委会',
                                         task_state=TAKESTATE[random.randint(
                                             0, len(TAKESTATE)-1)],
                                         transactor=user.realname,
                                         department=user.department,
                                         amount=random.randint(1, 200)*10000,
                                         content=fake.text())

    print('----create schedule------')
    for _ in range(200):
        project = Project.objects.order_by('?').first()
        schedule = Schedule.objects.create(name=fake.sentence(),
                                           transactor=project.transactor,
                                           department=project.department,
                                           content=fake.text(),
                                           project=project,
                                           iskey=False,
                                           isfin=False,
                                           progress=0,
                                           deadline=fake.date_time_between(
                                     start_date='-1y', end_date="-30d"))
