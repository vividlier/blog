from django.conf.urls import url
from blog.views import *
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name='blog'
urlpatterns = [
    url(r'^post_login/', post_login, name='post_login'),
    # url(r'^logout/', do_logout, name='logout'),
    # url(r'^do_reg/', do_reg, name='do_reg'),
    url(r'^do_login/', do_login, name='do_login'),
    url(r'^$', index, name='index'),
    url(r'^archive/$', archive, name='archive'),
    # url('login/',LoginView.as_view(template_name='login.html'),name='login'),
    url('logout/',LogoutView.as_view(),name='logout'),
    url("register/",register.as_view(),name="register"),
    url('publish-article/', publish_article, name='publish_article' )
]