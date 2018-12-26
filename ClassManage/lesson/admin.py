from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(SubjectInfo)
class SubjectInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'kind']


@admin.register(LessonInfo)
class LessonInfoAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ScheduleLessonInfo)
class ScheduleLessonInfoAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'start', 'end']
