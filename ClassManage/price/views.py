import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import PriceInfo
from lesson.models import ScheduleLessonInfo, LessonOfTeacher, LessonOfStudent, LessonInfo, SubjectInfo
from student.models import StudentInfo
from teacher.models import TeacherInfo
from dateutil.relativedelta import relativedelta

from utils import errmsg
from utils.ParseJson import parse_json


# Create your views here.
class StudentPriceView(View):
    """学生价格统计"""
    def get(self, request):
        student_id = request.GET.get('student')
        if not student_id:
            return self.student_all_price(request)
        else:
            student = StudentInfo.objects.filter(pk=student_id)
            if not student:
                return JsonResponse(errmsg.NO_SUCH_DATA)
            return self.student_price(request)

    def student_all_price(self, request):
        """学生价格统计总表"""
        date = request.GET.get('date')
        try:
            date1 = datetime.datetime.strptime(date, '%Y%m')
        except:
            return JsonResponse(errmsg.PARAMETER_ERROR)
        date2 = date1 + relativedelta(months=1)

        schedules = ScheduleLessonInfo.objects.filter(start__gte=date1, start__lt=date2)
        price_info_list = PriceInfo.objects.filter(schedule__in=schedules)

        temp = {}
        for price_info in price_info_list:
            student = price_info.student
            student_price_info = temp.get(student)
            if not student_price_info:
                student_price_info = {
                    'hour': 0,
                    'price': 0,
                }

            hour = student_price_info.get('hour') + self.get_hour(price_info)
            price =




        temp = []
        for schedule in schedules:
            lesson = schedule.lesson_of_teacher.lesson
            lesson_of_students = LessonOfStudent.objects.filter(lesson=lesson)
            hour = self.get_hour(schedule)
            for lesson_of_student in lesson_of_students:
                price = lesson_of_student.price
                name = lesson_of_student.student.name
                student_id = lesson_of_student.student.id
                student_price_info = {
                    'student_id': student_id,
                    'name': name,
                    'price': price,
                    'hour': hour,
                }
                student_info_list = temp.get(student_id)
                if not student_info_list:
                    student_info_list = []
                student_info_list

    def get_hour(self, price_info):
        """计算课时"""
        schedule = price_info.schedule
        hour = schedule.end - schedule.start
        hour = hour.seconds / 3600
        return hour

