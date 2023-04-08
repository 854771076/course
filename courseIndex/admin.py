from django.contrib import admin

# Register your models here.
from  .models import *

# Register your models here.

admin.site.site_title = "后台管理"
admin.site.site_header = "排课系统"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    exclude = []
    list_display=['teacher_num','teacher_name']
    search_fields=['teacher_name']
    
@admin.register(CourseWeekData)
class CourseWeekDataAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['id','subject','week','teacher','Class','room','day','Section']
    ordering=['week','day','Section']
    search_fields=['week','teacher']
@admin.register(BasicClass)
class BasicClassAdmin(admin.ModelAdmin):
    exclude = []
    search_fields=['class_name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    exclude = []
    search_fields=['room_name']
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=['student_num','student_name']
    exclude = []
    search_fields=['student_name']

