from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_gender']


@admin.register(TeacherOfLesson)
class TeacherOfLessonAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'lesson', 'price']
