from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_gender']


@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_gender']


@admin.register(SubjectInfo)
class SubjectInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_type']


@admin.register(LessonInfo)
class LessonInfoAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(StudentOfLesson)
class StudentOfLessonAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'price']


@admin.register(TeacherOfLesson)
class TeacherOfLessonAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'lesson', 'price']


@admin.register(ScheduleLessonInfo)
class ScheduleLessonInfoAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'schedule', 'hour']
