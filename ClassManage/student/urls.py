from django.urls import path
from .views import *

urlpatterns = [
    path('lesson/', StudentLessonView.as_view()),
    path('info/', StudengInfoView.as_view()),
    path('', StudentView.as_view()),
]