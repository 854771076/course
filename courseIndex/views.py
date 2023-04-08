
from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http import JsonResponse
from .models import *
import time,numpy as np,pandas as pd
import datetime,calendar,json
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
# 获取可带课教师
def getteacher(request):
    week=int(request.GET.get('week',1))
    Section=int(request.GET.get('Section',1))
    day=int(request.GET.get('day',1))
    exclude_teachers=CourseWeekData.objects.filter(Q(week=week)&Q(day=day)&Q(Section=Section)).values_list('teacher')
    teachers=[{'id':i.id,'name':i.teacher_name} for i in Teacher.objects.exclude(Q(pk__in=exclude_teachers))]
    return JsonResponse({"list": teachers},json_dumps_params={'ensure_ascii':False})
def getroom(request):
    week=int(request.GET.get('week',1))
    Section=int(request.GET.get('Section',1))
    day=int(request.GET.get('day',1))
    exclude_rooms=CourseWeekData.objects.filter(Q(week=week)&Q(day=day)&Q(Section=Section)).values_list('room')
    rooms=[{'id':i.id,'name':i.room_name} for i in Room.objects.exclude(Q(pk__in=exclude_rooms))]
    return JsonResponse({"list": rooms},json_dumps_params={'ensure_ascii':False})
def getclasses(request):
    week=int(request.GET.get('week',1))
    Section=int(request.GET.get('Section',1))
    day=int(request.GET.get('day',1))
    if week==-1:
        classes=[{'id':i.id,'name':i.class_name} for i in BasicClass.objects.all()]
        return JsonResponse({"list": classes},json_dumps_params={'ensure_ascii':False})
    exclude_classes=CourseWeekData.objects.filter(Q(week=week)&Q(day=day)&Q(Section=Section)).values_list('Class')
    classes=[{'id':i.id,'name':i.class_name} for i in BasicClass.objects.exclude(Q(pk__in=exclude_classes))]
    return JsonResponse({"list": classes},json_dumps_params={'ensure_ascii':False})

def getdata(request):
    week=int(request.GET.get('week',1))
    cid=request.GET.get('cid','')
    li=[[[] for j in range(6)] for i in range(7)]
    if cid=='':
        courses=CourseWeekData.objects.filter(Q(week=week))
    else:
        courses=CourseWeekData.objects.filter(Q(week=week)&Q(Class_id=cid))
    for course in courses:
        li[course.day-1][course.Section-1].append({'id':course.id,'subject':course.subject,'teacher':course.teacher.teacher_name,'t_id':course.teacher.id,'class':course.Class.class_name,'c_id':course.Class.id,'room':course.room.room_name,'r_id':course.room.id,'week':course.week,'day':course.day,'Section':course.Section})
    return JsonResponse({"list": li,'week':week},json_dumps_params={'ensure_ascii':False})
def savedata(request):
    week=int(request.GET.get('week',1))
    cid=request.GET.get('cid','')
    cname=''
    li={f'星期{i+1}':['' for j in range(6)] for i in range(7)}
    if cid=='':
        courses=CourseWeekData.objects.filter(Q(week=week))
    else:
        cname=BasicClass.objects.get(id=cid).class_name
        courses=CourseWeekData.objects.filter(Q(week=week)&Q(Class_id=cid))
    for course in courses:
        li[f'星期{course.day}'][course.Section-1]+=course.subject+'@'+course.teacher.teacher_name+'@'+course.Class.class_name+'@'+course.room.room_name+'\n'
    df=pd.DataFrame(li)
    df.columns=['星期一','星期二','星期三','星期四','星期五','星期六','星期天']
    df.index=[i for i in range(1,7)]
    name=f'{cname}第{week}周课程表_{datetime.datetime.now().timestamp()}.csv'
    df.to_csv(r'media/csv/'+name)
    return redirect('/media/csv/'+name)
def adddata(request):
    if request.user.is_authenticated:
        data={}
        try:
            id=request.GET.get('id','')
            week=int(request.GET.get('week',1))
            Section=int(request.GET.get('Section',1))
            day=int(request.GET.get('day',1))
            subject=request.GET.get('subject',None)
            t_id=int(request.GET.get('t_id',''))
            c_id=int(request.GET.get('c_id',''))
            r_id=int(request.GET.get('r_id',''))
            teacher=Teacher.objects.get(id=t_id)
            Class=BasicClass.objects.get(id=c_id)
            room=Room.objects.get(id=r_id)
            if id=='':
                CourseWeekData.objects.update_or_create(
                    week=week,
                    Section=Section,
                    day=day,
                    subject=subject,
                    teacher=teacher,
                    Class=Class,
                    room=room
                )
            else:
                CourseWeekData.objects.filter(id=id).update(
                    week=week,
                    Section=Section,
                    day=day,
                    subject=subject,
                    teacher=teacher,
                    Class=Class,
                    room=room
                )
            data['status']=200
            data['msg']='success'
        except Exception as e:
            data['msg']=f'{e}'
            data['status']=500
        return JsonResponse({"data": data},json_dumps_params={'ensure_ascii':False},status=data['status'])
    else:
        return redirect('/admin')
def deldata(request):
    if request.user.is_authenticated:
        data={}
        try:
            id=int(request.GET.get('id',''))
            CourseWeekData.objects.get(id=id).delete()
            data['status']=200
            data['msg']='success'
        except Exception as e:
            data['msg']=f'{e}'
            data['status']=500
        return JsonResponse({"data": data},json_dumps_params={'ensure_ascii':False},status=data['status'])
    else:
        return redirect('/admin')
def index(request):
    week=int(request.GET.get('week',1))
    cid=request.GET.get('cid',1)
    if week<=0:
        week=1
    return render(request,'index.html',{'week':week,'cid':cid})
