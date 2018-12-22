from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_gender']

@admin.register(StudentOfLesson)
class StudentOfLessonAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'price']
