"""word URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from django.urls import include
from word.settings import MEDIA_ROOT
from django.views.static import serve
import login.views
import captcha.views
import user.urls
import home.urls
import check.urls
import user.views
import note.urls

urlpatterns = [

    re_path(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    path('admin/', admin.site.urls),
    # login 模块
    path('login/', login.views.login),
    path('logout/', login.views.logout),
    path('register/', login.views.register),
    path('confirm/', login.views.user_confirm),
    path('forget/', login.views.forget),
    path('reset/', login.views.reset),
    path('ajax_reset', login.views.ajax_reset),

    # 验证码
    path('captcha/', include('captcha.urls')),
    path('ajax_val', login.views.ajax_val, name='ajax_val'),
    path('refresh', captcha.views.captcha_refresh, name='captcha-refresh'),

    # 用户
    re_path(r'user/', include(user.urls)),
    # re_path(r'user/([\w]+)/', user.views.user_info),

    # 首页
    path('', include(home.urls)),

    # 单词检测
    path('check/', include(check.urls)),

    # 笔记
    path('note/', include(note.urls))

]
