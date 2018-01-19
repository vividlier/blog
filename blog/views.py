# -*- coding:utf-8 -*-
# import logging
# from django.shortcuts import render
# from django.conf import settings
# from django.core.paginator import EmptyPage,Paginator,InvalidPage,PageNotAnInteger
# from .models import *

import logging
from django.shortcuts import render, redirect, HttpResponse
# from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Count
from .models import *
from .forms import *
import json


logger = logging.getLogger('blog.views')

# Create your views here.

def global_setting(request):
    return {
        'SITE_NAME':settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESC,
        'WEIBO_SINA': settings.WEIBO_SINA,
        'WEIBO_TENCENT': settings.WEIBO_TENCENT,
        'PRO_RSS': settings.PRO_RSS,
        'PRO_EMAIL': settings.PRO_EMAIL,
    }

def index(request):

        # f = open('zero.txt','r')  #打开一个不存在的文件
    category_list = Category.objects.all()[:5]
    article_list = Article.objects.all()
    paginator = Paginator(article_list,5)
    try:
        page = int(request.GET.get('page',1))
        article_list = paginator.page(page)
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        article_list = paginator.page(1)
        # logger.error(e)             #记录错误日志
    return render(request, 'index.html', locals())

def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        # print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           email=reg_form.cleaned_data["email"],
                                           url=reg_form.cleaned_data["url"],
                                           password=make_password(reg_form.cleaned_data["password"]),
                                           )
                user.save()

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect(request.POST.get('source.url'))
            else:
                return redirect(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return redirect(request, 'login.html', locals())

def do_login(requset):
    try:
        if requset.method == "POST":
            login_form = LoginForm(requset.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(requset, user)
                else:
                    return redirect(requset, 'failure.html', {'reason':'登录验证失败'})
                return redirect(requset.POST.get('source_url'))
            else:
                return redirect(requset, 'failure.html', {'reason':login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return (requset, 'login.html', locals())







