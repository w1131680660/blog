"""blog URL Configuration

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
from django.conf.urls import url,include
from django.urls import path,re_path
from django.views.static import serve
from app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("not_found",views.not_fount),
    path("register", views.register),
    url("login", views.login),
    url(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),
    re_path('^$', views.main),
    path("digg/",views.digg),
    path("comment/",views.comment),
    path("upload/",views.upload),
    path("create_article/",views.create_article),
    path("logout/",views.logout),
    re_path("delete/(?P<article_id>\w+)$",views.del_article),

    # meida配置
    re_path(r"media/(?P<path>.*)$", serve, {"document_root":settings.MEDIA_ROOT}),
    # 个人站点url
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|category|archive|articles)/(?P<param>.*)/$',views.home_site),
    re_path(r'^(?P<username>\w+)$', views.home_site),
    # 后台管理
    re_path("cn_backend/$",views.cn_backecd),
    re_path("add_article/$",views.add_article),


    re_path(r"(?P<name>\w+)$",views.gooo),
    path(r"login/",views.qq)





]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
