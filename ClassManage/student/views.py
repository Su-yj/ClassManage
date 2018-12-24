import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import *

"""
********************************************************外部接口********************************************************
"""


class StudentView(View):
    """学生视图"""
    def get(self, request):
        return render(request, 'student/student.html')


class StudengInfoView(View):
    """学生信息视图"""
    def post(self, request):
        # 处理接收的数据
        data = parse_json(request)
        if not data:
            return JsonResponse({})
        # 处理的方法
        method = {
            'add': self.add,
            'edit': self.edit,
            'del': self.delete,
        }
        option = data.get('option')
        method = method.get(option)
        if not method:
            return JsonResponse({})

        return method(data)

    def add(self, data):
        """
        添加学生信息
        :param data:
        :return:
        """
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        grade = data.get('grade')

        if not all([name, gender]):
            return JsonResponse({})

        if age and (age < 3 or age > 50):
            return JsonResponse({})

        if grade and grade not in [i[0] for i in StudentInfo.GRADE]:
            return JsonResponse({})

        try:
            StudentInfo(name=name, gender=gender, age=age, grade=grade).save()
            return JsonResponse({'code': 0})
        except:
            return JsonResponse({})

    def edit(self, data):
        """
        修改学生信息
        :param data:
        :return:
        """
        _id = data.get('id')
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        grade = data.get('grade')

        if not all([_id, name, gender]):
            return JsonResponse({})

        student = StudentInfo.objects.filter(pk=_id).first()
        if not student:
            return JsonResponse({})

        if age and (age < 3 or age > 50):
            return JsonResponse({})

        if grade and grade not in [i[0] for i in StudentInfo.GRADE]:
            return JsonResponse({})

        try:
            student.name = name
            student.gender = gender
            student.age = age
            student.grade = grade
            student.save()
            return JsonResponse({'code': 0})
        except:
            return JsonResponse({})

    def delete(self, data):
        """
        删除学生信息
        :param data:
        :return:
        """
        _id = data.get('id')
        student = StudentInfo.objects.filter(pk=_id).first()
        if not student:
            return JsonResponse({})

        student.delete()
        return JsonResponse({'code': 0})


"""
********************************************************内部方法********************************************************
"""


def parse_json(request):
    """
    解析json数据
    :param request: 请求内容
    :return: data, 请求参数
    """
    try:
        data = json.loads(request.body)
        return data
    except:
        return None
        