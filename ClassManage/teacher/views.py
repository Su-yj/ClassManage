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


class CheckAccount(view):
    """"""
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
    """docstring for TeacherInfoView"""
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

    def edit(self, data):
        pass

    def delete(self, data):
        pass
