from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(SubjectInfo)
class SubjectInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'kind']


@admin.register(LessonInfo)
class LessonInfoAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(LessonOfStudent)
class LessonOfStudentAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'price']


@admin.register(LessonOfTeacher)
class LessonOfTeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'lesson', 'price']


@admin.register(ScheduleLessonInfo)
class ScheduleLessonInfoAdmin(admin.ModelAdmin):
    list_display = ['lesson_of_teacher', 'start', 'end']
