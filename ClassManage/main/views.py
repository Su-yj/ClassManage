from django.shortcuts import render
from .models import *


def index(request):
    context = {'test': 'hello haha'}
    return render(request, "base.html", context)
