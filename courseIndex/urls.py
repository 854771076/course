# from django.contrib import admin
from django.urls import path
from . import views

app_name='courseIndex'

urlpatterns = [
    path('', views.index,name='index'),
    path('getteacher',views.getteacher,name='getteacher' ),
    path('getroom',views.getroom,name='getroom' ),
    path('getclasses',views.getclasses,name='getclasses' ),
    path('getdata',views.getdata,name='getdata' ),
    path('adddata',views.adddata,name='adddata' ),
    path('deldata',views.deldata,name='deldata' ),
    path('savedata',views.savedata,name='savedata' ),
   
]