from django.urls import path
from .views import *

urlpatterns = [
    path('', StudentView.as_view()),
    path('', index),
]