"""myblog URL Configuration

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
from django.urls import path,re_path
from blogs import views
from django.views.static import serve
from myblog import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('get_validCode_img/',views.get_validCode_img),
    path('logout/',views.logout),

    # 后台管理 匹配不加用户名的
    path('backend/',views.backend),

    # 文件上传
    path('upload/',views.upload),

    # 点赞
    path('diggit/',views.diggit),

    # 评论

    path('comment/',views.comment),

    # 删除评论

    path('comment/delete/',views.comment_delete),

    # 首页
    re_path(r'^$', views.index),

    # 后台管理页面
    # 匹配前面加了用户名的
    # re_path(r'^(?P<username>\w+)/backend/',views.backend),

    # 删除、修改文章
    re_path(r'backend/(?P<article_id>\d+)/(?P<param>update|delete)/$',views.backend),

    # 添加文章
    re_path(r'backend/add/$',views.add_article),



    # 静态文件(客户端访问)
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),

    # 文章详情
    re_path(r'^(?P<username>\w+)/article/(?P<article_id>\d+)/$',views.article_detail),
    # 标签分类
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|kind|date)/(?P<param>.*)/$',views.person_site),
    # 个人站点
    re_path(r'^(?P<username>\w+)/$',views.person_site),
    # re_path(r'(?P<username>\w+)/',views.person_site),



]
