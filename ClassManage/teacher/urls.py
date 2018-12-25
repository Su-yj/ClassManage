from django.urls import path
from .views import *

urlpatterns = [
    path('checkAcount/', CheckAcount.as_view()),
    path('info/', TeacherInfoView.as_view()),
    path('', TeacherView.as_view()),
]