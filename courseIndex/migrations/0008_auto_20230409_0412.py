# Generated by Django 3.2.5 on 2023-04-08 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseIndex', '0007_alter_student_student_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='Class',
        ),
        migrations.AddField(
            model_name='student',
            name='Class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courseIndex.basicclass', verbose_name='班级'),
            preserve_default=False,
        ),
    ]