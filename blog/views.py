# -*- coding:utf-8 -*-
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
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views import View
from django.utils.datastructures import MultiValueDictKeyError
import json


logger = logging.getLogger('blog.views')

# Create your views here.

def global_setting(request):
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    #分类信息获取
    category_list = Category.objects.all()[:5]
    #文章归档信息获取
    archive_list = Article.objects.distinct_date()
    #评论计数集合
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by(
        '-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    return locals()


class register(View):

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        try:
            errors = request.GET['errors']
        except MultiValueDictKeyError:
            errors = "请务必填写真实信息"
        return render(request, 'account/register.html', context={"errors": errors})

    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            phone = request.POST['phone']
            user_id = request.POST['user_id']
        except MultiValueDictKeyError:
            raise Http404("your form is corrupted")

        try:
            user = User.objects.get(username=username)

            # exist
            return HttpResponseRedirect("%s?errors=%s" % (reverse("account:register"), "您与他人发生了重名,请在姓名后添加任意后缀"))
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password)

            # userinfo = UserInfo.objects.create(user=user, phone=phone, user_ID_number=user_id)

        return HttpResponseRedirect(reverse("account:login"))


# def do_reg(request):
#     try:
#         if request.method == 'POST':
#             reg_form = RegForm(request.POST)
#             if reg_form.is_valid():
#                 user = User.objects.create(username=reg_form.cleaned_data["username"],
#                                            # email=reg_form.cleaned_data["email"],
#                                            # url=reg_form.cleaned_data["url"],
#                                            password=make_password(reg_form.cleaned_data["password"]),
#                                            )
#                 user.save()
#
#                 user.backend = 'django.contrib.auth.backends.ModelBackend'
#                 login(request, user)
#                 return redirect(request.POST.get('source.url'))
#             else:
#                 return redirect(request, 'failure.html', {'reason': reg_form.errors})
#         else:
#             reg_form = RegForm()
#     except Exception as e:
#         logger.error(e)
#     return redirect(request, 'login.html', locals())
#
def post_login(request):
    return render(request, 'login.html', locals())
#
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
                return render(requset, 'index.html', locals())
            else:
                return redirect(requset, 'failure.html', {'reason':login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return (requset, 'login.html', locals())

def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        # print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

def index(request):
    try:
        # 文章归档信息获取
        article_list = Article.objects.all()
        article_list = getPage(request, article_list)
        # logger.error(e)             #记录错误日志
    except Exception as e:
            logger.error(e)
            # logger.error(e)             #记录错误日志
    return render(request, 'index.html', locals())

def archive(request):
    try:
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains=year + '-' + month)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())

def getPage(request, article_list):
    paginator = Paginator(article_list, 5)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

def publish_article(request):
    return render(request, 'publish_articles.html', locals())


