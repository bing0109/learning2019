from django.shortcuts import render, redirect
import time
from .models import Testchart, Tester, Report
from zjj.models import Job, Jobneed, Tester
from qsj.models import UserAdmin, UserHR, UserExpert, Company, Factor, Moding, ModelDesign
from fxj.models import Qustion, Answer
from django.db import models
from django.db.models import *
from django.core.paginator import Paginator


d = Jobneed.objects.annotate(
c=Value(Tester.objects.filter(Q(status=1) & Q(jobneed_id=F("jobneed_id_id"))), output_field=models.CharField()))

>>> Jobneed.objects.get(pk=5).tester_set.all().values()
<QuerySet [{'create_hr_id_id': 1, 'sex': True, 'jobneed_id_id': 5, 'status': 2, 'name': '小明', 'id': 1, 'isdelete': False, 'comment': 'qqqqqqqqq'}, {'create_hr_id_id': 2, 'sex': True, 'jobneed_id_id': 5, 'status': 1, 'name': '小红', 'id': 2, 'isdelete': False, 'comment': 'ssssssssssss'}, {'create_hr_id_id': 1, 'sex': True, 'jobneed_id_id': 5, 'status': 1, 'name': '刘八', 'id': 4, 'isdelete': False, 'comment': 'ssssssssdfwedfgsertgdfg'}]>


e = Jobneed.objects.filter(tester__status=1).values()

Jobneed.objects.aggregate(c_invite=Count('tester', filter=Q(tester__status=2)),c_tested=Count('tester', filter=Q(tester__status=3)),c_offer=Count('tester', filter=Q(tester__status=4)))


Jobneed.objects.annotate(c_invite=Count('tester', filter=Q(tester__status=2)),c_tested=Count('tester', filter=Q(tester__status=3)),c_offer=Count('tester', filter=Q(tester__status=4)))

e = Jobneed.objects.get(pk=5).tester.all().values()
