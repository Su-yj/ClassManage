from django.urls import path
from .views import *

urlpatterns = [
    path('', SubjectView.as_view()),
    path('info/', SubjectInfoView.as_view()),
]