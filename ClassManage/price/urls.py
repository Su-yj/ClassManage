from django.urls import path
from .views import *

urlpatterns = [
    path('student/', StudentPriceView.as_view()),
    path('teacher/', TeacherPriceView.as_view()),
]