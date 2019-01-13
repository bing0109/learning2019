# coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
import time
from cjb.models import Testchart, Report
from zjj.models import Job, Jobneed, Tester
from qsj.models import UserAdmin, UserHR, UserExpert, Company, Factor, Moding, ModelDesign
from fxj.models import Qustion, Answer
from django.db import models
from django.db.models import *
from django.core.paginator import Paginator
import json


# Create your views here.
def jobneed3(request):
    return render(request, 'cjb/jobneed3.html')


def jobneed2(request):
    return render(request, 'cjb/base_hr2.html')


def main(request):
    return render(request, 'cjb/company2.html')


def company(request):
    return render(request, 'cjb/company2.html')


def jobneed_query(request):
    # if request.is_ajax():
        # jns = Jobneed.objects.values('id', 'create_hr_id__user', 'create_time', 'jobneed_name', 'jobneed_status')
        # # 遍历元素获取每个职位需求的各种状态的数据
        # for jn in jns:
        #     c_invite = Tester.objects.filter(Q(jobneed_id=jn['id']) & Q(status=2)).count()
        #     c_tested = Tester.objects.filter(Q(jobneed_id=jn['id']) & Q(status=3)).count()
        #     c_selected = Tester.objects.filter(Q(jobneed_id=jn['id']) & Q(status=4)).count()
        #     jn.update({'c_invite': c_invite, 'c_tested': c_tested, 'c_offer': c_selected})

    # 下面这个语句也可以直接获取到每个职位需求的各种状态的数据
    jns = Jobneed.objects.filter(isdelete=False).annotate(c_invite=Count('tester', filter=Q(tester__status__gte=1)),
                                   c_tested=Count('tester', filter=(Q(tester__status__gte=2)&Q(tester__status__lte=3))),
                                   c_selected=Count('tester', filter=(Q(tester__status=3))),
                                   c_deselect=Count('tester', filter=Q(tester__status=4))).order_by('-id')

    print(jns, '-------jns-----')
    nav_title = 'jobneed'
    context = {'ob_jns': jns, 'nav_title': nav_title}
    print(context, '----jn--context---')
    return render(request, 'cjb/jobneed2.html', context)
    # else:
    #     return redirect('/cjb/main/')


def jobneed_add(request):
    if request.is_ajax():
        jn_name = request.POST.get('jn_name')
        jn_desc = request.POST.get('jn_desc')
        jn_requ = request.POST.get('jn_requ')
        jn_model = request.POST.get('jn_model')
        jn_jb_id = request.POST.get('jn_jb_id')

        jn_data = Jobneed()
        jn_data.jobneed_name = jn_name
        jn_data.jobdescription = jn_desc
        jn_data.jobrequirements = jn_requ
        # jn_data.isdelete = False
        # jn_data.create_time = ''

        try:
            jn_data.job_id = Job.objects.get(pk=int(jn_jb_id))
        except Exception:
            jn_data.job_id = None

        try:
            jn_data.moding_id = Moding.objects.get(pk=int(jn_model))
        except Exception:
            jn_data.moding_id = None

        try:
            create_name = request.sessions.get('HR')
            jn_data.create_hr_id = UserHR.objects.get(user=create_name)
        except Exception:
            jn_data.create_hr_id = UserHR.objects.get(pk=1)
            print(jn_data.create_hr_id, '---create_hr_id---')

        if jn_model == (None or ''):
            jn_data.jobneed_status = 1
        else:
            jn_data.jobneed_status = 2

        jn_data.save()

    jns = Jobneed.objects.all()
    context = {'ob_jns': jns}
    return render(request, 'cjb/jobneed2.html', context)


def jobneed_edit(request):
    return render(request, 'cjb/jobneed2.html')


def jobneed_detail(request):
    return render(request, 'cjb/jobneed2.html')


def jobneed_del(request):
    if request.is_ajax():
        jn_id = request.POST.get('id')
        try:
            jn_tobedel = Jobneed.objects.filter(isdelete=False).get(pk=jn_id)
            jn_tobedel.isdelete = True
            jn_tobedel.save()
            # print(Jobneed.objects.get(pk=jn_id).isdelete,'-----isdelete----')
            context = {'del_result': 'delete success!', 'del_id': jn_id}
        except Exception:
            context = {'del_result': 'delete fail!'}

        # return HttpResponse(context)
        return JsonResponse(context)


def get_jobneed_list(request):
    if request.is_ajax():
        jns = Jobneed.objects.filter(isdelete=False).values('id', 'jobneed_name')
        # context = {'ob_jns': jns}
        context = json.dumps(list(jns))
        # print(context, '-----contest------')
    return JsonResponse(context, safe=False)


def get_job_list(request):
    if request.is_ajax():
        jbs = Job.objects.filter(isdelete=False).values('id', 'jobname', 'moding_id', 'moding_id__name')
        context = json.dumps(list(jbs))
        print(context, '-----get_job_list------')
    return JsonResponse(context, safe=False)


def get_te_list(request):
    if request.is_ajax():
        jn_id = request.POST.get('jn_id')
        tes = Tester.objects.filter(status=0).filter(Q(jobneed_id=None)|Q(jobneed_id=jn_id)).values('name', 'id')
        context = json.dumps(list(tes))
        print(context, '---tes---')
    return JsonResponse(context, safe=False)


def tester_query(request):
    tes = Tester.objects.filter(isdelete=False).order_by('-id').values('id','create_hr_id__user', 'status', 'sex', 'jobneed_id__jobneed_name', 'name')
    context = {'obj_tes': tes, 'nav_title': 'tester'}
    # print(context, '---testquery---')
    return render(request, 'cjb/tester.html', context)


def tester_add(request):
    te_name = request.POST.get('te_name')
    te_sex = request.POST.get('te_sex')
    te_comment = request.POST.get('te_comment')
    te_jn_select = request.POST.get('te_jn_select')

    te = Tester()
    te.name = te_name
    te.sex = te_sex
    te.comment = te_comment
    try:
        te.jobneed_id = Jobneed.objects.get(pk=int(te_jn_select))
    except Exception:
        te.jobneed_id = None

    try:
        create_name = request.sessions.get('HR')
        te.create_hr_id = UserHR.objects.get(user=create_name)
    except Exception:
        te.create_hr_id = UserHR.objects.get(pk=1)
        print(te.create_hr_id, '---create_hr_id---')

    try:
        invite = request.POST.get('te_invite')
        print(invite, 'invite----')
        if invite == ('' or None):
            te.status = 0
        else:
            te.status = 1
    except Exception:
        te.status = 0

    te.save()
    print(te, 'testeradd-------')
    # return render(request, 'cjb/tester.html')
    return redirect('/cjb/tester/')


def tester_edit(request):
    return render(request, 'cjb/tester.html')


def tester_del(request):
    if request.is_ajax():
        te_id = request.POST.get('id')
        try:
            te = Tester.objects.filter(isdelete=False).get(pk=int(te_id))
            te.isdelete = True
            # te.save()
            # print(Jobneed.objects.get(pk=jn_id).isdelete,'-----isdelete----')
            context = {'del_result': 'delete success!', 'del_id': te_id}
        except Exception:
            context = {'del_result': 'delete fail!'}

        # return HttpResponse(context)
        return JsonResponse(context)


def sub_invite_te_from_jn(request):
    jn_id = request.POST.get('invite_te_jn_id')
    te_id = request.POST.get('jn_select_te')
    print(jn_id,te_id,'----')
    te = Tester.objects.get(pk=int(te_id))
    te_jn = Jobneed.objects.get(pk=int(jn_id))
    te.jobneed_id = te_jn
    te.status = 1
    te.save()
    return redirect('/cjb/jobneed/')


def sub_invite_te_from_tester(request):
    return redirect('/cjb/tester/')


def login(request):

    return render(request, 'pjs/login.html')


