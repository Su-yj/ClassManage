from django.urls import path
from .views import *

urlpatterns = [
    path('student/info/', StudentLessonInfoView.as_view()),
    path('student/', StudentLessonView.as_view()),
    path('info/', SubjectInfoView.as_view()),
    path('', SubjectView.as_view()),
]