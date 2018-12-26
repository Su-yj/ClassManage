import copy
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import *

from utils import errmsg
from utils.ParseJson import parse_json


# Create your views here.
class TeacherView(View):
    """老师视图"""
    def get(self, request):
        return render(request, 'teacher/teacher.html')


class CheckAccount(View):
    """检查老师账号是否有重复"""
    def post(self, request):
        json_data = parse_json(request)
        if not json_data:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        account = json_data.get('account')
        if not account:
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        success = copy.deepcopy(errmsg.SUCCESS)
        if TeacherInfo.objects.filter(account=account).first():
            success.update({'repeat': True})
        else:
            success.update({'repeat': False})
        return JsonResponse(success)


class TeacherInfoView(View):
    """老师信息"""
    def post(self, request):
        json_data = parse_json(request)
        if not json_data:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        method = {
            'add': self.add,
            'edit': self.edit,
            'delete': self.delete,
        }
        option = method.get(json_data.get('type'))
        if not option:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        return option(json_data)

    def add(self, data):
        name = data.get('name')
        gender = data.get('gender')

        if not all([name, gender]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        try:
            TeacherInfo(name=name, gender=gender).save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def edit(self, data):
        """
        修改老师信息
        :param data:
        :return:
        """
        _id = data.get('id')
        name = data.get('name')
        gender = data.get('gender')
        account = data.get('account')

        if not all([_id, name, gender, account]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        teacher = TeacherInfo.objects.filter(pk=_id).first()
        if not teacher:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        if len(account) != 8:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        try:
            teacher.name = name
            teacher.gender = gender
            teacher.account = account
            student.save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def delete(self, data):
        """
        删除老师信息
        :param data:
        :return:
        """
        _id = data.get('id')
        teacher = TeacherInfo.objects.filter(pk=_id).first()
        if not teacher:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        teacher.delete()
        return JsonResponse(errmsg.SUCCESS)
