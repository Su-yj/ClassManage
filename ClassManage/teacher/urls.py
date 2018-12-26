from django.urls import path
from .views import *

urlpatterns = [
    path('checkAccount/', CheckAccount.as_view()),
    path('info/', TeacherInfoView.as_view()),
    path('', TeacherView.as_view()),
]