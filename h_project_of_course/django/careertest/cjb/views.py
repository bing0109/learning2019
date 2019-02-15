# coding=utf-8
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
import time
from cjb.models import Testchart, Report
from zjj.models import Job, Jobneed, Tester
from qsj.models import UserAdmin, UserHR, UserExpert, Company, Factor, Moding, ModelDesign
from fxj.models import Qustion, Answer
from django.db import models
from django.db.models import *
from django.core.paginator import Paginator
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def login(request):
    return render(request, 'pjs/login.html')


def login_process(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if UserHR.objects.filter(Q(user=username) & Q(password=password)):
            request.session['user'] = username
            request.session.set_expiry(0)
            print('----hr user--')
            return redirect('/cjb/company/')

        elif UserExpert.objects.filter(Q(user=username) & Q(password=password)):
            request.session['user'] = username
            print('---expert user----')
            return render(request, 'cjb/expert.html')

        elif UserHR.objects.filter(Q(user=username) & Q(password=password)):
            request.session['user'] = username
            print('----admin user---')
            return render(request, 'cjb/admin.html')
        else:
            print('---login failed---')
            return HttpResponse('用户名密码不匹配')


def check_login(func):
    def checklogin(request, *args, **kwargs):
        is_login = request.session.get('user', False)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/cjb/login/')
            # return HttpResponseRedirect(request, 'pjs/login.html')

    return checklogin


def logout(request):
    is_login = request.session.get('user', False)
    if is_login:
        del request.session['user']
        request.session.clear()
        return redirect('/cjb/login/')
    else:
        return HttpResponse('您还未登录，请登录，谢谢！')

# 注销使用
# request.session.clear()
#
# 设置超时时间，set_expiry(value)方法是在最后一次刷新开始计算
# request.session.set_expiry(value)
# * 如果value是个整数，session会在些秒数后失效。
# * 如果value是个datatime或timedelta，session就会在这个时间后失效。
# * 如果value是0,用户关闭浏览器session就会失效。
# * 如果value是None,session会依赖全局session失效策略。


def jobneed3(request):
    return render(request, 'cjb/jobneed3.html')


def jobneed2(request):
    return render(request, 'cjb/base_hr2.html')


# @login_required
def main(request):
    return render(request, 'cjb/company.html')


@check_login
def company(request):
    if request.session['user']:
        session_user = request.session['user']

    context = {'session_user': session_user, 'nav_title': 'company'}
    return render(request, 'cjb/company.html', context)


@check_login
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

    if request.session['user']:
        session_user = request.session['user']

    context = {'ob_jns': jns, 'nav_title': nav_title, 'session_user': session_user}

    print(context, '----jn--context---')
    return render(request, 'cjb/jobneed.html', context)
    # else:
    #     return redirect('/cjb/main/')


@check_login
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
            create_name = request.session['user']
            # print(create_name, '-----create_name-----')
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
    return render(request, 'cjb/jobneed.html', context)


@check_login
def jobneed_edit(request):
    return render(request, 'cjb/jobneed.html')


@check_login
def jobneed_detail(request):
    return render(request, 'cjb/jobneed.html')


@check_login
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


@check_login
def get_jobneed_list(request):
    if request.is_ajax():
        jns = Jobneed.objects.filter(isdelete=False).values('id', 'jobneed_name')
        # context = {'ob_jns': jns}
        context = json.dumps(list(jns))
        # print(context, '-----contest------')
    return JsonResponse(context, safe=False)


@check_login
def get_job_list(request):
    if request.is_ajax():
        jbs = Job.objects.filter(isdelete=False).values('id', 'jobname', 'moding_id', 'moding_id__name')
        context = json.dumps(list(jbs))
        print(context, '-----get_job_list------')
    return JsonResponse(context, safe=False)


@check_login
def get_te_list(request):
    if request.is_ajax():
        jn_id = request.POST.get('jn_id')
        tes = Tester.objects.filter(status=0).filter(Q(jobneed_id=None)|Q(jobneed_id=jn_id)).values('name', 'id')
        context = json.dumps(list(tes))
        print(context, '---tes---')
    return JsonResponse(context, safe=False)


@check_login
def tester_query(request):
    tes = Tester.objects.filter(isdelete=False).order_by('-id').values('id','create_hr_id__user', 'status', 'sex', 'jobneed_id__jobneed_name', 'name')
    # print(context, '---testquery---')

    if request.session['user']:
        session_user = request.session['user']

    context = {'obj_tes': tes, 'nav_title': 'tester', 'session_user': session_user}

    return render(request, 'cjb/tester.html', context)


@check_login
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


@check_login
def tester_edit(request):
    return render(request, 'cjb/tester.html')


@check_login
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


@check_login
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


@check_login
def sub_invite_te_from_tester(request):
    return redirect('/cjb/tester/')


def page_not_found(request):
    # return HttpResponse('404,找不到页面！')
    return render_to_response('404.html')
    # 404网页要直接放在templates目录下，不能在其他目录下
    # 要用render_to_response，不能用HttpResponse


def page_error(request):
    return render_to_response('500.html')


def page403(request):
    return render_to_response('403.html')


def page400(request):
    return render_to_response('400.html')
