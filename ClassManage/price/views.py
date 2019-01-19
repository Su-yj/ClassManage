import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import *
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
        # 计算日期范围
        date = request.GET.get('date')
        date1, date2 = self.get_date(date)
        if not all([date1, date2]):
            return JsonResponse(errmsg.PARAMETER_ERROR)

        student_id = request.GET.get('student')
        if not student_id:
            return self.student_all_price(request, date1, date2)
        else:
            if student_id == 'all':
                student = None
            else:
                student = StudentInfo.objects.filter(pk=student_id).first()
                if not student:
                    return JsonResponse(errmsg.NO_SUCH_DATA)
            return self.student_price(request, student, date1, date2)

    def post(self, request):
        """修改变动价格"""
        json_data = parse_json(request)
        _id = json_data.get('id')
        sliding_price = json_data.get('sliding_price')
        if not all([_id, sliding_price]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        price_info = PriceInfo.objects.filter(pk=_id).first()
        if not price_info:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        if not isinstance(sliding_price, int):
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        price_info.student_sliding_price = sliding_price
        price_info.save()
        return JsonResponse(errmsg.SUCCESS)

    def student_all_price(self, request, date1, date2):
        """学生价格统计总表"""
        schedules = ScheduleLessonInfo.objects.filter(start__gte=date1, start__lt=date2)
        price_info_list = PriceInfo.objects.filter(schedule__in=schedules)
        temp_dict = {}
        for price_info in price_info_list:
            student_price_info = temp_dict.get(price_info.student)
            if not student_price_info:
                student_price_info = {
                    'id': price_info.student.id,
                    'name': price_info.student.name,
                    'hour': 0,
                    'price': 0,
                }
            hour = student_price_info['hour'] + price_info.get_hour()
            price = student_price_info['price'] + price_info.get_student_price() * price_info.get_hour() + price_info.student_sliding_price
            student_price_info.update({'hour': hour, 'price': price})
            temp_dict.update({price_info.student: student_price_info})

        student_price_list = list(temp_dict.values())
        context = {
            'title': '学生价格统计',
            'student_price_list': student_price_list,
            'date': datetime.datetime.strftime(date1, '%Y-%m'),
        }
        return render(request, 'price/student_price.html', context)

    def student_price(self, request, student, date1, date2):
        schedules = ScheduleLessonInfo.objects.filter(start__gte=date1, start__lt=date2)
        if student:
            price_info_list = PriceInfo.objects.filter(schedule__in=schedules).filter(student=student)
        else:
            price_info_list = PriceInfo.objects.filter(schedule__in=schedules)
        detail_list = []
        for price_info in price_info_list:
            data = {
                'id': price_info.id,
                'name': price_info.student,
                'lesson': price_info.schedule.lesson_of_teacher,
                'start': datetime.datetime.strftime(price_info.schedule.start, '%Y-%m-%d %H:%M'),
                'end': datetime.datetime.strftime(price_info.schedule.end, '%Y-%m-%d %H:%M'),
                'hour': price_info.get_hour(),
                'price_hour': price_info.get_student_price(),
                'sliding_price': price_info.student_sliding_price,
                'price': price_info.get_hour() * price_info.get_student_price() + price_info.student_sliding_price,
                'start_time': price_info.schedule.start,
            }
            detail_list.append(data)

        detail_list.sort(key=lambda x: x['start_time'])
        if student:
            name = student
        else:
            name = '所有学生'
        context = {
            'title': '学生价格统计',
            'date': datetime.datetime.strftime(date1, '%Y-%m'),
            'name': name,
            'detail_list': detail_list,
            'type': 'student',
        }
        return render(request, 'price/price_detail.html', context)

    def get_date(self, date):
        """获取月份"""
        if date:
            try:
                date1 = datetime.datetime.strptime(date, '%Y-%m')
            except:
                return None, None
        else:
            year = datetime.datetime.today().year
            month = datetime.datetime.today().month
            date = '%s-%s' % (year, month)
            date1 = datetime.datetime.strptime(date, '%Y-%m')
        date2 = date1 + relativedelta(months=1)
        return date1, date2


class TeacherPriceView(View):
    """老师价格统计"""
    def get(self, request):
        # 计算需要的月份
        date = request.GET.get('date')
        date1, date2 = self.get_date(date)
        if not all([date1, date2]):
            return JsonResponse(errmsg.PARAMETER_ERROR)

        teacher_id = request.GET.get('teacher')
        if not teacher_id:
            return self.teacher_all_price(request, date1, date2)
        else:
            if teacher_id == 'all':
                teacher = None
            else:
                teacher = TeacherInfo.objects.filter(pk=teacher_id).first()
                if not teacher:
                    return JsonResponse(errmsg.NO_SUCH_DATA)
            return self.teacher_price(request, teacher, date1, date2)

    def post(self, request):
        """修改老师变动价格"""
        json_data = parse_json(request)
        _id = json_data.get('id')
        sliding_price = json_data.get('sliding_price')
        if not all([_id, sliding_price]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        schedule = ScheduleLessonInfo.objects.filter(pk=_id).first()
        if not schedule:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        if not isinstance(sliding_price, int):
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        schedule.teacher_sliding_price = sliding_price
        schedule.save()
        return JsonResponse(errmsg.SUCCESS)

    def teacher_all_price(self, request, date1, date2):
        """老师价格统计总表"""
        schedules = ScheduleLessonInfo.objects.filter(start__gte=date1, start__lt=date2)
        temp_dict = {}
        for schedule in schedules:
            teacher = schedule.get_teacher()
            teacher_price_info = temp_dict.get(teacher)
            if not teacher_price_info:
                teacher_price_info = {
                    'id': teacher.id,
                    'name': teacher.name,
                    'hour': 0,
                    'price': 0,
                }
            hour = teacher_price_info['hour'] + schedule.get_hour()
            price = teacher_price_info['price'] + schedule.get_teacher_price() * schedule.get_hour() + schedule.teacher_sliding_price
            teacher_price_info.update({'hour': hour, 'price': price})
            temp_dict.update({teacher: teacher_price_info})

        teacher_price_list = list(temp_dict.values())
        context = {
            'title': '老师价格统计',
            'teacher_price_list': teacher_price_list,
            'date': datetime.datetime.strftime(date1, '%Y-%m'),
        }
        return render(request, 'price/teacher_price.html', context)

    def teacher_price(self, request, teacher, date1, date2):
        if teacher:
            schedules = ScheduleLessonInfo.objects.filter(start__gte=date1, start__lt=date2, lesson_of_teacher__teacher=teacher).order_by('start')
        else:
            schedules = ScheduleLessonInfo.objects.filter(start__gte=date1, start__lt=date2).order_by('start')
        detail_list = []
        for schedule in schedules:
            data = {
                'id': schedule.id,
                'name': schedule.lesson_of_teacher,
                'start': datetime.datetime.strftime(schedule.start, '%Y-%m-%d %H:%M'),
                'end': datetime.datetime.strftime(schedule.end, '%Y-%m-%d %H:%M'),
                'hour': schedule.get_hour(),
                'price_hour': schedule.get_teacher_price(),
                'sliding_price': schedule.teacher_sliding_price,
                'price': schedule.get_hour() * schedule.get_teacher_price() + schedule.teacher_sliding_price,
            }
            detail_list.append(data)

        if teacher:
            name = teacher
        else:
            name = '所有老师'
        context = {
            'title': '老师价格统计',
            'date': datetime.datetime.strftime(date1, '%Y-%m'),
            'name': name,
            'detail_list': detail_list,
            'type': 'teacher',
        }
        return render(request, 'price/price_detail.html', context)

    def get_date(self, date):
        """获取月份"""
        if date:
            try:
                date1 = datetime.datetime.strptime(date, '%Y-%m')
            except:
                return None, None
        else:
            year = datetime.datetime.today().year
            month = datetime.datetime.today().month
            date = '%s-%s' % (year, month)
            date1 = datetime.datetime.strptime(date, '%Y-%m')
        date2 = date1 + relativedelta(months=1)
        return date1, date2
