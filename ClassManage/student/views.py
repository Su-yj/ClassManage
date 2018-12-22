import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import *


# Create your views here.
class StudentView(View):
    """学生视图"""
    def get(self, request):
        return render(request, 'student/student.html')

    def post(self, request):
        # 处理接收的数据
        data = self.parse_json(request)
        if not data:
            return JsonResponse({})
        # 处理的方法
        method = {
            'info': self.info,
            'add': self.add,
            'update': self.update,
        }
        option = data.get('option')
        method = method.get(option)
        if not method:
            return JsonResponse({})

        return method(data)

    def info(self, data):
        student_id = data.get('student_id')
        if student_id:
            try:
                student = StudentInfo.objects.get(pk=student_id)
            except:
                return JsonResponse({})
            student_id = student.pk
            name = student.name
            gender = student.gender
            age = student.age
            grade = student.grade
            return JsonResponse(
                {
                    'code': 0, 
                    'data': {
                        'student_id': student_id,
                        'name': name,
                        'gender': gender,
                        'age': age,
                        'grade': grade,
                    }
                }
            )
        else:
            students = StudentInfo.objects.all()
            for student in students:
                info = {
                    
                }


        
    def parse_json(self, request):
        try:
            data = json.loads(request.body)
            return data
        except:
            return None
        