# from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
app_name='courseIndex'

urlpatterns = [
    #管理员首页
    path('root_index', views.root_index,name='root_index'),
    #获取当前可带课的老师数据
    path('getteacher',views.getteacher,name='getteacher' ),
    #获取当前空闲教室数据
    path('getroom',views.getroom,name='getroom' ),
    #获取当前无课班级数据
    path('getclasses',views.getclasses,name='getclasses' ),
    #获取当前课表数据
    path('getdata',views.getdata,name='getdata' ),
    #添加课表详细接口
    path('adddata',views.adddata,name='adddata' ),
    #删除课表详细接口
    path('deldata',views.deldata,name='deldata' ),
    #保存当前课表数据
    path('savedata',views.savedata,name='savedata' ),
    #首页
    path('', views.index,name='index'),
    #登录页
    path('login', views.Login.as_view(),name='login'),

]