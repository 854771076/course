#courseIndex.views.py
#导包
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from .models import *
import pandas as pd
import datetime
from django.db.models import Q
from django.views import View
from django.contrib.auth import login, logout
# 获取可带课教师
def getteacher(request):
    #获取前端由GET方式传入的参数(当前周数、当前星期、当前节次信息)
    week = int(request.GET.get('week', 1))#当前周数
    Section = int(request.GET.get('Section', 1))#当前节次
    day = int(request.GET.get('day', 1))#当前星期
    #如果为-1周，返回所有教师数据，返回格式为json,方便前端获取参数
    if week == -1:
        teachers = [{'id': i.id, 'name': i.teacher_name}
                    for i in Teacher.objects.all()]
        return JsonResponse({"list": teachers}, json_dumps_params={'ensure_ascii': False})
    #查找到当前时段有课的老师数据
    exclude_teachers = CourseWeekData.objects.filter(
        Q(week=week) & Q(day=day) & Q(Section=Section)).values_list('teacher')
    #筛选掉有课的老师，并返回json数据列表，格式为[{'id': i.id, 'name': i.teacher_name}]
    teachers = [{'id': i.id, 'name': i.teacher_name}
                for i in Teacher.objects.exclude(Q(pk__in=exclude_teachers))]
    return JsonResponse({"list": teachers}, json_dumps_params={'ensure_ascii': False})
#获取空闲教室，原理同上
def getroom(request):
    week = int(request.GET.get('week', 1))
    Section = int(request.GET.get('Section', 1))
    day = int(request.GET.get('day', 1))
    exclude_rooms = CourseWeekData.objects.filter(
        Q(week=week) & Q(day=day) & Q(Section=Section)).values_list('room')
    rooms = [{'id': i.id, 'name': i.room_name}
             for i in Room.objects.exclude(Q(pk__in=exclude_rooms))]
    return JsonResponse({"list": rooms}, json_dumps_params={'ensure_ascii': False})
#获取空闲班级，原理同上
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
#获取课程表数据
def getdata(request):
    #获取当前周次
    week = int(request.GET.get('week', 1))
    #筛选条件
    cid = request.GET.get('cid', '')#班级id
    tid = request.GET.get('tid', '')#老师id
    #初始化课程表
    '''
    [[[], [], [], [], [], []],
     [[], [], [], [], [], []],
     [[], [], [], [], [], []],
     [[], [], [], [], [], []],
     [[], [], [], [], [], []],
     [[], [], [], [], [], []],
     [[], [], [], [], [], []]]
    是一个7行6列的列表，行代表星期，列代表课程节次，最里面的小列表是为了处理一个时间段有多个班级多门课的情况
    '''
    li = [[[] for j in range(6)] for i in range(7)]
    #如果传入了老师/班级筛选条件，就进行筛选
    if cid == '':
        courses = CourseWeekData.objects.filter(Q(week=week))
    else:
        courses = CourseWeekData.objects.filter(Q(week=week) & Q(Class_id=cid))
    if tid == '':
        pass
    else:
        courses = courses.filter(teacher_id=tid)
    #将每行里的小列表填上查到的课表数据
    for course in courses:
        li[course.day-1][course.Section-1].append({'id': course.id, 'subject': course.subject, 'teacher': course.teacher.teacher_name, 't_id': course.teacher.id, 'class': course.Class.class_name,
                                                  'c_id': course.Class.id, 'room': course.room.room_name, 'r_id': course.room.id, 'week': course.week, 'day': course.day, 'Section': course.Section})
    return JsonResponse({"list": li, 'week': week}, json_dumps_params={'ensure_ascii': False})

#保存csv，查询原理同上
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
    #将查询到的课表数据转换为DataFrame对象
    df = pd.DataFrame(li)
    #改字段名
    df.columns = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    df.index = [i for i in range(1, 7)]
    #生成课表名
    name = f'{cname}第{week}周课程表_{datetime.datetime.now().timestamp()}.csv'
    #保存至项目media/csv/目录下
    df.to_csv(r'media/csv/'+name)
    #返回保存路径
    return redirect('/media/csv/'+name)

#添加课表数据
def adddata(request):
    #判断是否登录管理员账号，如果未登录返回管理员登录界面
    if request.user.is_authenticated:
        data = {}
        try:
            #获取前端传入的添加课表数据
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
            #保存至数据库
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
        #返回该操作的状态和消息
        return JsonResponse({"data": data}, json_dumps_params={'ensure_ascii': False}, status=data['status'])
    else:
        return redirect('/admin')

#删除课程表数据
def deldata(request):
    #判断是否登录管理员账号，如果未登录返回管理员登录界面
    if request.user.is_authenticated:
        data = {}
        try:
            #获取传入的id数据
            id = int(request.GET.get('id', ''))
            #数据库删除id相等的数据
            CourseWeekData.objects.get(id=id).delete()
            data['status'] = 200
            data['msg'] = 'success'
        except Exception as e:
            data['msg'] = f'{e}'
            data['status'] = 500
        #返回该操作的状态和消息
        return JsonResponse({"data": data}, json_dumps_params={'ensure_ascii': False}, status=data['status'])
    else:
        return redirect('/admin')

#管理员首页界面
def root_index(request):
    #如果管理员未登录转入登录界面
    if str(request.user) != 'root':
        return redirect('/admin')
    #课表的查询数据
    week = int(request.GET.get('week', 1))
    cid = request.GET.get('cid', '')
    tid = request.GET.get('tid', '')
	
    if week <= 0:
        week = 1
    return render(request, 'root_index.html', {'week': week, 'cid': cid, 'tid': tid})

#用户首页
def index(request):
    week = int(request.GET.get('week', 1))
    #获取cookie数据
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

#用户登录界面
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
