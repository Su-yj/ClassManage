from django.urls import path
from .views import *

urlpatterns = [
    path('info/', StudengInfoView.as_view()),
    path('', StudentView.as_view()),
]