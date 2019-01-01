from django.urls import path
from .views import *

urlpatterns = [
    path('schedule/info/', ScheduleInfoView.as_view()),
    path('student/info/', StudentLessonInfoView.as_view()),
    path('teacher/info/', TeacherLessonInfoView.as_view()),
    path('schedule/', ScheduleView.as_view()),
    path('student/', StudentLessonView.as_view()),
    path('teacher/', TeacherLessonView.as_view()),
    path('info/', SubjectInfoView.as_view()),
    path('', SubjectView.as_view()),
]