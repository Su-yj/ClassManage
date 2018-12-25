from django.urls import path
from .views import *

urlpatterns = [
    path('', TeacherView.as_view()),
    # path('info/', StudengInfoView.as_view()),
]