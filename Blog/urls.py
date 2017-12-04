"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from yii.views import *

urlpatterns = [
    # 后台
    url(r'^admin/$', admin),
    url(r'^admin/(\w+)/$', admin),
    url(r'^admin/(\w+)/(\d+)/$', admin),
    url(r'^admin/_developer/(\w+)/$', admin),
    url(r'^admin/_developer/(\w+)/(\d+)/$', admin),
    url(r'^admin/api/(\w+)/$', api),
    # 前台
    url(r'^$', webs),
    url(r'^(\w+)/$', webs),
    url(r'^(\w+)/(\w+)/$', webs),
]
