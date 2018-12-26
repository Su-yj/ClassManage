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
    """"""
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
