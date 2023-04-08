
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from .models import *
import time
import numpy as np
import pandas as pd
import datetime
import calendar
import json
from django.db.models import Q
from django.views import View
from django.contrib.auth import login, logout
# 获取可带课教师


def getteacher(request):
    week = int(request.GET.get('week', 1))
    Section = int(request.GET.get('Section', 1))
    day = int(request.GET.get('day', 1))
    if week == -1:
        teachers = [{'id': i.id, 'name': i.teacher_name}
                    for i in Teacher.objects.all()]
        return JsonResponse({"list": teachers}, json_dumps_params={'ensure_ascii': False})
    exclude_teachers = CourseWeekData.objects.filter(
        Q(week=week) & Q(day=day) & Q(Section=Section)).values_list('teacher')
    teachers = [{'id': i.id, 'name': i.teacher_name}
                for i in Teacher.objects.exclude(Q(pk__in=exclude_teachers))]
    return JsonResponse({"list": teachers}, json_dumps_params={'ensure_ascii': False})


def getroom(request):
    week = int(request.GET.get('week', 1))
    Section = int(request.GET.get('Section', 1))
    day = int(request.GET.get('day', 1))
    exclude_rooms = CourseWeekData.objects.filter(
        Q(week=week) & Q(day=day) & Q(Section=Section)).values_list('room')
    rooms = [{'id': i.id, 'name': i.room_name}
             for i in Room.objects.exclude(Q(pk__in=exclude_rooms))]
    return JsonResponse({"list": rooms}, json_dumps_params={'ensure_ascii': False})


def getclasses(request):
    week = int(request.GET.get('week', 1))
    Section = int(request.GET.get('Section', 1))
    day = int(request.GET.get('day', 1))
    if week == -1:
        classes = [{'id': i.id, 'name': i.class_name}
                   for i in BasicClass.objects.all()]
        return JsonResponse({"list": classes}, json_dumps_params={'ensure_ascii': False})
    exclude_classes = CourseWeekData.objects.filter(
        Q(week=week) & Q(day=day) & Q(Section=Section)).values_list('Class')
    classes = [{'id': i.id, 'name': i.class_name}
               for i in BasicClass.objects.exclude(Q(pk__in=exclude_classes))]
    return JsonResponse({"list": classes}, json_dumps_params={'ensure_ascii': False})


def getdata(request):
    week = int(request.GET.get('week', 1))
    cid = request.GET.get('cid', '')
    tid = request.GET.get('tid', '')
    li = [[[] for j in range(6)] for i in range(7)]
    if cid == '':
        courses = CourseWeekData.objects.filter(Q(week=week))
    else:
        courses = CourseWeekData.objects.filter(Q(week=week) & Q(Class_id=cid))
    if tid == '':
        pass
    else:
        courses = courses.filter(teacher_id=tid)
    for course in courses:
        li[course.day-1][course.Section-1].append({'id': course.id, 'subject': course.subject, 'teacher': course.teacher.teacher_name, 't_id': course.teacher.id, 'class': course.Class.class_name,
                                                  'c_id': course.Class.id, 'room': course.room.room_name, 'r_id': course.room.id, 'week': course.week, 'day': course.day, 'Section': course.Section})
    return JsonResponse({"list": li, 'week': week}, json_dumps_params={'ensure_ascii': False})


def savedata(request):
    week = int(request.GET.get('week', 1))
    cid = request.GET.get('cid', '')
    cname = ''
    tid = request.GET.get('tid', '')
    li = {f'星期{i+1}': ['' for j in range(6)] for i in range(7)}
    if cid == '':
        courses = CourseWeekData.objects.filter(Q(week=week))
    else:
        cname = BasicClass.objects.get(id=cid).class_name
        courses = CourseWeekData.objects.filter(Q(week=week) & Q(Class_id=cid))
    if tid == '':
        pass
    else:
        courses = courses.filter(teacher_id=tid)
    for course in courses:
        li[f'星期{course.day}'][course.Section-1] += course.subject+'@' + \
            course.teacher.teacher_name+'@' + \
            course.Class.class_name+'@'+course.room.room_name+'\n'
    df = pd.DataFrame(li)
    df.columns = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    df.index = [i for i in range(1, 7)]
    name = f'{cname}第{week}周课程表_{datetime.datetime.now().timestamp()}.csv'
    df.to_csv(r'media/csv/'+name)
    return redirect('/media/csv/'+name)


def adddata(request):
    if request.user.is_authenticated:
        data = {}
        try:
            id = request.GET.get('id', '')
            week = int(request.GET.get('week', 1))
            Section = int(request.GET.get('Section', 1))
            day = int(request.GET.get('day', 1))
            subject = request.GET.get('subject', None)
            t_id = int(request.GET.get('t_id', ''))
            c_id = int(request.GET.get('c_id', ''))
            r_id = int(request.GET.get('r_id', ''))
            teacher = Teacher.objects.get(id=t_id)
            Class = BasicClass.objects.get(id=c_id)
            room = Room.objects.get(id=r_id)
            if id == '':
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
            data['status'] = 200
            data['msg'] = 'success'
        except Exception as e:
            data['msg'] = f'{e}'
            data['status'] = 500
        return JsonResponse({"data": data}, json_dumps_params={'ensure_ascii': False}, status=data['status'])
    else:
        return redirect('/admin')


def deldata(request):
    if request.user.is_authenticated:
        data = {}
        try:
            id = int(request.GET.get('id', ''))
            CourseWeekData.objects.get(id=id).delete()
            data['status'] = 200
            data['msg'] = 'success'
        except Exception as e:
            data['msg'] = f'{e}'
            data['status'] = 500
        return JsonResponse({"data": data}, json_dumps_params={'ensure_ascii': False}, status=data['status'])
    else:
        return redirect('/admin')


def root_index(request):
    if str(request.user) != 'root':
        return redirect('/admin')
    week = int(request.GET.get('week', 1))
    cid = request.GET.get('cid', '')
    tid = request.GET.get('tid', '')

    if week <= 0:
        week = 1
    return render(request, 'root_index.html', {'week': week, 'cid': cid, 'tid': tid})


def index(request):
    week = int(request.GET.get('week', 1))
    cid = request.COOKIES.get('cid', '')
    tid = request.COOKIES.get('tid', '')
    sid = request.COOKIES.get('sid', '')
    user=''
    if sid:
        user=Student.objects.get(id=sid)
    if tid:
        user=Teacher.objects.get(id=tid)
    
    if week <= 0:
        week = 1
    if user=='':
         return redirect('/login')
    if str(request.user) == 'root':
        return redirect('/root_index')
    return render(request, 'index.html', {'week': week, 'cid': cid, 'tid': tid, 'user': user})


class Message:
    def __init__(self, status=None, msg=None):
        status = status
        msg = msg

    def __str__(self):
        return f'{self.msg}{self.status}'


class Login(View):
    def get(self, request):
        message = Message()
        logout(request)
        return render(request, 'login.html', {'message': message})

    def post(self, request):
        message = Message()
        no = request.POST.get('no', '')
        type = request.POST.get('type', '学生')
        pwd = request.POST.get('pwd')
        tid = ''
        cid = ''
        sid=''
        if no:
            try:
                if type == '学生':
                    
                    u = Student.objects.get(student_num=no)
                    sid=no
                    cid = u.Class.id
                    
                else:
                    u = Teacher.objects.get(teacher_num=no)
                    tid = no
            except Exception as e:
                message.status = 0
                message.msg = f'学号/工号错误'
                return render(request, 'login.html', {'message': message})
        else:
            message.status = 0
            message.msg = '请输入学号/工号'
            return render(request, 'login.html', {'message': message})
        if u.password != pwd:
            message.msg = '密码错误!'
            message.status = 0
            return render(request, 'login.html', {'message': message})
        else:
            r=redirect(f'/')
            r.set_cookie('tid',tid)
            r.set_cookie('cid',cid)
            r.set_cookie('sid',sid)
            return r
