#admin.py
from django.contrib import admin
# Register your models here.
from  .models import *

#后台名字
admin.site.site_title = "后台管理"
admin.site.site_header = "排课系统"

#注册老师表后台管理功能
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    exclude = []
    list_display=['teacher_num','teacher_name']
    search_fields=['teacher_name']
#注册课程表后台管理功能    
@admin.register(CourseWeekData)
class CourseWeekDataAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['id','subject','week','teacher','Class','room','day','Section']
    ordering=['week','day','Section']
    search_fields=['week','teacher']
#注册班级表后台管理功能
@admin.register(BasicClass)
class BasicClassAdmin(admin.ModelAdmin):
    exclude = []
    search_fields=['class_name']
#注册教室表后台管理功能
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    exclude = []
    search_fields=['room_name']
#注册学生表后台管理功能
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=['student_num','student_name']
    exclude = []
    search_fields=['student_name']

