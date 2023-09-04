"""super_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include, re_path
from django.conf import settings

from system.views import ProhibitedTextDetectionView, UserStatusDisableView
from apps.picture.views import SdModelSelectView

# 媒体文件流式响应
from utils.streamingmedia_response import streamingmedia_serve

urlpatterns = [
    # 处理媒体文件
    path('media/<path:path>', streamingmedia_serve, {'document_root': settings.MEDIA_ROOT}, ),
    # 违禁词检测
    path('python/system/textdetection/', ProhibitedTextDetectionView.as_view(), name='违禁词检测'),
    # 违禁状态检测
    path('python/system/userdisable/', UserStatusDisableView.as_view(), name='违禁状态检测'),
    # sd模型查询
    path('python/apps/sdmodelselect/', SdModelSelectView.as_view(), name='sd模型查询'),
]
