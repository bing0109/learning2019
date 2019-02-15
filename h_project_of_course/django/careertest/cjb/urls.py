"""careertest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url('jobneed3/', views.jobneed3),
    url('jobneed2/', views.jobneed2),
    url('jobneed/', views.jobneed_query),
    url('jobneed_add/', views.jobneed_add),
    url('jobneed_edit/', views.jobneed_edit),
    url('jobneed_del/', views.jobneed_del),
    url('tester/', views.tester_query),
    url('tester_add/', views.tester_add),
    url('tester_edit/', views.tester_edit),
    url('tester_del/', views.tester_del),
    url('company/', views.company),
    url('main/', views.main),
    url('login/', views.login),
    url('login_process/', views.login_process),
    url('logout/', views.logout),
    url('get_jn_list/', views.get_jobneed_list),
    url('get_job_list/', views.get_job_list),
    url('get_te_list/', views.get_te_list),
    url('sub_invite_te_from_jn/', views.sub_invite_te_from_jn),
    url('sub_invite_te_from_tester/', views.sub_invite_te_from_tester),

]


handler404 = views.page_not_found
handler500 = views.page_error
handler403 = views.page403
handler400 = views.page400
