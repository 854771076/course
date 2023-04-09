from django.db import models
# Create your models here.



class Teacher(models.Model):
    id=models.BigAutoField(primary_key=True,blank=False)
    teacher_name = models.CharField(max_length=255,verbose_name='教师姓名')
    teacher_num = models.CharField(max_length=255, blank=True, null=True,verbose_name='教师工号')
    password=models.CharField(max_length=200,verbose_name='密码')
    teacher_level = models.IntegerField(verbose_name='教师等级')
    sex = models.IntegerField(verbose_name='性别',help_text='1 男 2 女')
    age = models.IntegerField(blank=True, null=True,verbose_name='年龄')
    phone = models.CharField(max_length=255,verbose_name='手机号')
    birthday = models.CharField(max_length=255, blank=True, null=True,verbose_name='出生年月')
    email = models.CharField(max_length=255, blank=True, null=True,verbose_name='教师邮箱')
    school = models.CharField(max_length=255, blank=True, null=True,verbose_name='毕业院校')
    department = models.CharField(max_length=255, blank=True, null=True,verbose_name='毕业院校院系')
    major = models.CharField(max_length=255, blank=True, null=True,verbose_name='毕业院校专业')
    education = models.CharField(max_length=255, blank=True, null=True,verbose_name='学历')
    def __str__(self):
        return self.teacher_name
    class Meta:
        verbose_name_plural='老师表'
        # managed = False
        db_table = 'teacher'

class BasicClass(models.Model):
    id=models.BigAutoField(primary_key=True,blank=False)
    class_name = models.CharField(max_length=200,verbose_name='班级名')
    class_cate = models.IntegerField(blank=True, null=True,verbose_name='班级分类',help_text='0 五天全日制 1 六天全日制 2预科班 3 周末班')
    start_time = models.DateTimeField(verbose_name='开班时间')
    class_status = models.IntegerField(blank=True, null=True,verbose_name='班级状态',help_text='0 正常 1禁用')
    description = models.CharField(max_length=200, blank=True, null=True,verbose_name='备注')
    def __str__(self):
        return self.class_name
    class Meta:
        verbose_name_plural='班级表'
        # managed = False
        db_table = 'basic_class'




class Student(models.Model):
    id=models.BigAutoField(primary_key=True,blank=False)
    student_name = models.CharField(max_length=200,verbose_name='学生姓名')
    password=models.CharField(max_length=200,verbose_name='密码')
    student_num = models.CharField(max_length=255, null=False,verbose_name='学号')
    Class =models.ForeignKey(BasicClass, verbose_name='班级', on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='加入班级时间')
    student_status = models.IntegerField(verbose_name='学生状态',help_text='0正常 1 请假 2 休学 3 退学')
    sex = models.IntegerField(blank=True, null=True,verbose_name='性别')
    age = models.IntegerField(blank=True, null=True,verbose_name='年龄')
    birthday = models.CharField(max_length=200, blank=True, null=True,verbose_name='出生年月日')
    student_email = models.CharField(max_length=200, blank=True, null=True,verbose_name='邮箱')
    student_school = models.CharField(max_length=200, blank=True, null=True,verbose_name='院校')
    student_department = models.CharField(max_length=200, blank=True, null=True,verbose_name='院系')
    student_major = models.CharField(max_length=200, blank=True, null=True,verbose_name='专业')
    student_school_class = models.CharField(max_length=200, blank=True, null=True,verbose_name='在校班级')
    student_education = models.CharField(max_length=200, blank=True, null=True,verbose_name='学历')
    phone = models.CharField(max_length=200,verbose_name='手机号')
    qq_number = models.CharField(max_length=200, blank=True, null=True,verbose_name='qq号')
    wechart_number = models.CharField(max_length=200, blank=True, null=True,verbose_name='微信号')
    idcard = models.CharField(max_length=200, blank=True, null=True,verbose_name='身份证号')
    emergency_name = models.CharField(max_length=200, blank=True, null=True,verbose_name='紧急联系人姓名')
    emergency_phone = models.CharField(max_length=200, blank=True, null=True,verbose_name='紧急联系人电话')
    family_address = models.CharField(max_length=200, blank=True, null=True,verbose_name='家庭住址')
    now_address = models.CharField(max_length=200, blank=True, null=True,verbose_name='现在住址')
    guarder = models.CharField(max_length=200, blank=True, null=True,verbose_name='监护人')
    guarder_phone = models.CharField(max_length=200, blank=True, null=True,verbose_name='监护人电话')
    description = models.CharField(max_length=200, blank=True, null=True,verbose_name='备注')
    def __str__(self):
        return self.student_name
    class Meta:
        verbose_name_plural='学生表'
        # managed = False
        db_table = 'student'
class Room(models.Model):
    id=models.BigAutoField(primary_key=True,blank=False)
    room_name = models.CharField(max_length=200,verbose_name='教室名')
    room_count = models.IntegerField(blank=True, null=True,verbose_name='教室容量')
    room_status = models.IntegerField(blank=True, null=True,verbose_name='教室状态',help_text='0教室空闲 1教室禁用',default=0)
    description = models.CharField(max_length=200, blank=True, null=True,verbose_name='描述')
    def __str__(self):
        return self.room_name
    class Meta:
        verbose_name_plural='教室表'
        # managed = False
        db_table = 'rooms'

class CourseWeekData(models.Model):
    id=models.BigAutoField(primary_key=True,blank=False)
    week = models.IntegerField(verbose_name="周数",default=0)
    Section=models.IntegerField(verbose_name="节次",null=False)
    subject=models.CharField(verbose_name="课程名", max_length=50,null=False)
    day=models.IntegerField(verbose_name="星期",null=False)
    teacher=models.ForeignKey(Teacher, verbose_name='老师', on_delete=models.CASCADE)
    Class=models.ForeignKey(BasicClass, verbose_name='班级', on_delete=models.CASCADE)
    room=models.ForeignKey(Room, verbose_name='教室', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.week)
    class Meta:
        verbose_name_plural='周课表数据'
        db_table='course_weekdata'