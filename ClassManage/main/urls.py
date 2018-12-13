from django.urls import path
from .views import *

urlpatterns = [
    path('student/', StudentView.as_view()),
    path('', index),
]