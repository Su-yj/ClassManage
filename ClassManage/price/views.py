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
        if date:
            try:
                date1 = datetime.datetime.strptime(date, '%Y%m')
            except:
                return JsonResponse(errmsg.PARAMETER_ERROR)
        else:
            year = datetime.datetime.today().year
            month = datetime.datetime.today().month
            date = '%s%s' % (year, month)
            date1 = datetime.datetime.strptime(date, '%Y%m')
        date2 = date1 + relativedelta(months=1)

        schedules = ScheduleLessonInfo.objects.filter(start__gte=date1, start__lt=date2).values_list('id', flat=True)
        print(schedules)
        price_info_list = PriceInfo.objects.filter(schedule__in=schedules)
        print('-'*50)
        print(price_info_list)

        temp = {}
        for price_info in price_info_list:
            student = price_info.student
            lesson = price_info.schedule.lesson_of_teacher.lesson
            lesson_of_student = LessonOfStudent.objects.filter(lesson=lesson, student=student).first()
            price_hour = lesson_of_student.price
            student_price_info = temp.get(student.id)
            if not student_price_info:
                student_price_info = {
                    'id': student.id,
                    'name': student.name,
                    'hour': 0,
                    'price': 0,
                }
            hour = student_price_info.get('hour') + self.get_hour(price_info)
            price = student_price_info.get('price') + hour * price_hour + price_info.more_price
            student_price_info.update({'hour': hour, 'price': price})
            temp.update({student.id: student_price_info})
        student_price_list = list(temp.values())
        context = {
            'title': '学生价格统计',
            'student_price_list': student_price_list,
        }
        return render(request, 'price/student_price.html', context)

    def student_price(self, request):
        pass

    def get_hour(self, price_info):
        """计算课时"""
        schedule = price_info.schedule
        hour = schedule.end - schedule.start
        hour = hour.seconds / 3600
        return hour

