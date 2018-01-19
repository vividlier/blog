from django.conf.urls import url
from blog.views import *

urlpatterns = [
    url(r'^logout/$', do_logout, name='logout'),
    url(r'^reg/$', do_reg, name='reg'),
    url(r'^login/$', do_login, name='login'),
    url(r'^$', index, name='index'),
]