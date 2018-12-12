from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from .models import *


def index(request):
    context = {'test': 'hello haha'}
    return render(request, "base.html", context)


class StudentView(View):
    """学生视图"""
    def get(self, request):
        return render(request, 'student.html')

    def post(self, request):
        return JsonResponse({'a': 'a'})
        # print('11111')
        # return render(request, 'index.html')
        # return HttpResponse('111')
