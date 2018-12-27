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


class SubjectView(View):
    """科目视图"""
    def get(self, request):
        return render(request, 'lesson/subject.html')


class SubjectInfoView(View):
    """科目类型信息"""
    def get(self, request):
        _id = request.GET.get('id')
        if not _id:
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        try:
            _id = int(_id)
        except:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        # subject = SubjectInfo.objects.filter(pk=_id).last()
        # if not subject:
        #     return JsonResponse(errmsg.NO_SUCH_DATA)

        # data = {
        #     'id': subject.pk,
        #     'name': subject.name,
        #     'kind': subject.kind,
        # }
        data = {
            'id': 1,
            'name': 'ddddd',
            'kind': 1,
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

        return option(data)

    def add(self, data):
        """
        添加科目种类信息
        :param data:
        :return:
        """
        name = data.get('name')
        kind = data.get('kind')

        if not all([name, kind]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        if kind not in [i[0] for i in SubjectInfo.CLASS_TYPE]:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        try:
            SubjectInfo(name=name, kind=kind).save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def edit(self, data):
        """
        修改科目种类信息
        :param data:
        :return:
        """
        _id = data.get('id')
        name = data.get('name')
        kind = data.get('kind')

        if not all([_id, name, kind]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        subject = SubjectInfo.objects.filter(pk=_id).first()
        if not subject:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        if kind not in [i[0] for i in SubjectInfo.CLASS_TYPE]:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        try:
            subject.name = name
            subject.kind = kind
            subject.save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def delete(self, data):
        """
        删除科目种类信息
        :param data:
        :return:
        """
        _id = data.get('id')
        subject = SubjectInfo.objects.filter(pk=_id).first()
        if not subject:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        subject.delete()
        return JsonResponse(errmsg.SUCCESS)


class StudentLessonView(View):
    """学生课程管理视图"""
    def get(self, request):
        return render(request, 'lesson/studentoflesson.html')

    def post(self, request):
        json_data = parse_json(request)
        if not json_data:
            return errmsg.PARAMETER_TYPE_ERROR

        _id = json_data.get('id')
        if not _id:
            return errmsg.INCOMPLETE_PARAMETERS

        lesson_of_student = LessonOfStudent.objects.filter(pk=_id).first()
        if not lesson_of_student:
            return errmsg.NO_SUCH_DATA

        data = {
            'id': lesson_of_student.id,
            'student': lesson_of_student.student.id,
            'subject': lesson_of_student.lesson.subject.id,
            'price': lesson_of_student.price,
        }
        success = copy.deepcopy(errmsg.SUCCESS)
        success.update({'data': data})
        return JsonResponse(success)
