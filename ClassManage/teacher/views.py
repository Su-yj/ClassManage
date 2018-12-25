from django.shortcuts import render
from django.views import View
from .models import *


# Create your views here.
class TeacherView(View):
    """老师视图"""
    def get(self, request):
        return render(request, 'teacher/teacher.html')
