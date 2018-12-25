import json
import copy

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import *

from utils import errmsg
from utils.ParseJson import parse_json

"""
********************************************************外部接口********************************************************
"""


class StudentView(View):
    """学生视图"""
    def get(self, request):
        return render(request, 'student/student.html')


class StudengInfoView(View):
    """学生信息视图"""
    def get(self, request):
        """
        获取学生信息
        :param request:
        :return:
        """
        _id = request.GET.get('id')
        if not _id:
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        try:
            _id = int(_id)
        except:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        # student = StudentInfo.objects.filter(pk=_id).last()
        # if not student:
        #     return JsonResponse(errmsg.NO_SUCH_DATA)

        # data = {
        #     'id': student.pk,
        #     'name': student.name,
        #     'gender': student.gender,
        #     'age': student.age,
        #     'grade': student.grade,
        # }
        data = {
            'id': 1,
            'name': 'haha',
            'gender': False,
            'age': 34,
            'grade': 4,
        }
        success = copy.deepcopy(errmsg.SUCCESS)
        success.update({'data': data})
        return JsonResponse(success)

    def post(self, request):
        # 处理接收的数据
        data = parse_json(request)
        print(data)
        if not data:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)
        # 处理的方法
        method = {
            'add': self.add,
            'edit': self.edit,
            'delete': self.delete,
        }
        option = method.get(data.get('type'))
        if not option:
            return JsonResponse(errmsg.PARAMETER_ERROR)

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
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        if age and (age < 3 or age > 50):
            return JsonResponse(errmsg.PARAMETER_ERROR)

        if grade and grade not in [i[0] for i in StudentInfo.GRADE]:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        try:
            StudentInfo(name=name, gender=gender, age=age, grade=grade).save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

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
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        student = StudentInfo.objects.filter(pk=_id).first()
        if not student:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        if age and (age < 3 or age > 50):
            return JsonResponse(errmsg.PARAMETER_ERROR)

        if grade and grade not in [i[0] for i in StudentInfo.GRADE]:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        try:
            student.name = name
            student.gender = gender
            student.age = age
            student.grade = grade
            student.save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def delete(self, data):
        """
        删除学生信息
        :param data:
        :return:
        """
        _id = data.get('id')
        student = StudentInfo.objects.filter(pk=_id).first()
        if not student:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        student.delete()
        return JsonResponse(errmsg.SUCCESS)


"""
********************************************************内部方法********************************************************
"""
