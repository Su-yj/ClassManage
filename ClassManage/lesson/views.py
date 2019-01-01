import json
import copy
import datetime
import pandas

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import *
from student.models import StudentInfo
from teacher.models import TeacherInfo

from utils import errmsg
from utils.ParseJson import parse_json

"""
********************************************************外部接口********************************************************
"""


class SubjectView(View):
    """科目视图"""
    def get(self, request):
        subject_list = SubjectInfo.objects.all()
        context = {
            'title': '课程种类',
            'modal_title': '课程种类',
            'add_button': '添加课程种类',
            'subject_list': subject_list,
            'class_type': SubjectInfo.CLASS_TYPE,
        }
        return render(request, 'lesson/subject.html', context)


class SubjectInfoView(View):
    """科目类型信息"""
    def get(self, request):
        _id = request.GET.get('id')
        if not _id:
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        try:
            _id = int(_id)
        except:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        subject = SubjectInfo.objects.filter(pk=_id).last()
        if not subject:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        data = {
            'id': subject.pk,
            'name': subject.name,
            'kind': subject.kind,
        }
        success = copy.deepcopy(errmsg.SUCCESS)
        success.update({'data': data})
        return JsonResponse(success)

    def post(self, request):
        # 处理接收的数据
        data = parse_json(request)
        print(data)
        if not data:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)
        # 处理的方法
        method = {
            'add': self.add,
            'edit': self.edit,
            'delete': self.delete,
        }
        option = method.get(data.get('type'))
        if not option:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        return option(data)

    def add(self, data):
        """
        添加科目种类信息
        :param data:
        :return:
        """
        name = data.get('name')
        kind = data.get('kind')

        if not all([name, kind is not None]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        if kind not in [i[0] for i in SubjectInfo.CLASS_TYPE]:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        try:
            SubjectInfo(name=name, kind=kind).save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def edit(self, data):
        """
        修改科目种类信息
        :param data:
        :return:
        """
        _id = data.get('id')
        name = data.get('name')
        kind = data.get('kind')

        if not all([name, kind is not None]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        subject = SubjectInfo.objects.filter(pk=_id).first()
        if not subject:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        if kind not in [i[0] for i in SubjectInfo.CLASS_TYPE]:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        try:
            subject.name = name
            subject.kind = kind
            subject.save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def delete(self, data):
        """
        删除科目种类信息
        :param data:
        :return:
        """
        _id = data.get('id')
        subject = SubjectInfo.objects.filter(pk=_id).first()
        if not subject:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        subject.delete()
        return JsonResponse(errmsg.SUCCESS)


class StudentLessonView(View):
    """学生课程管理视图"""
    def get(self, request):
        student_list = StudentInfo.objects.all()
        subject_list = SubjectInfo.objects.all()
        student_of_lesson_list = LessonOfStudent.objects.all()
        context = {
            'title': '学生课程管理',
            'modal_title': '学生课程信息',
            'add_button': '添加学生课程',
            'student_list': student_list,
            'subject_list': subject_list,
            'student_of_lesson_list': student_of_lesson_list,
        }
        return render(request, 'lesson/studentoflesson.html', context)


class StudentLessonInfoView(View):
    """学生课程信息"""
    def get(self, request):
        _id = request.GET.get('id')
        if not _id:
            return errmsg.INCOMPLETE_PARAMETERS

        lesson_of_student = LessonOfStudent.objects.filter(pk=_id).first()
        if not lesson_of_student:
            return errmsg.NO_SUCH_DATA

        data = {
            'id': lesson_of_student.id,
            'student': lesson_of_student.student.id,
            'subject': lesson_of_student.lesson.subject.id,
            'price': lesson_of_student.price,
        }
        success = copy.deepcopy(errmsg.SUCCESS)
        success.update({'data': data})
        return JsonResponse(success)

    def post(self, request):
        # 处理接收的数据
        data = parse_json(request)
        print(data)
        if not data:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)
        # 处理的方法
        method = {
            'add': self.add,
            'edit': self.edit,
            'delete': self.delete,
        }
        option = method.get(data.get('type'))
        if not option:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        return option(data)

    def add(self, data):
        """
        添加学生课程信息
        :param data:
        :return:
        """
        student = data.get('student')
        subject = data.get('subject')
        price = data.get('price')

        if not all([student, subject, price]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        if not all([isinstance(student, int), isinstance(subject, int), isinstance(price, int)]):
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        if price < 0 or price > 9999:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        student = StudentInfo.objects.filter(pk=student).first()
        if not student:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        subject = SubjectInfo.objects.filter(pk=subject).first()
        if not subject:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        if subject.kind == subject.CLASS_TYPE[2][0]:
            name = '%s(%s)' % ('小班课', subject.name)
            lesson_info = LessonInfo.objects.filter(subject=subject).first()
            if not lesson_info:
                lesson_info = LessonInfo(name=name, subject=subject)
                lesson_info.save()
        else:
            name = '%s(%s)' % (student.name, subject.name)
            lesson_info = LessonInfo(name=name, subject=subject)
            lesson_info.save()

        try:
            LessonOfStudent(lesson=lesson_info, student=student, price=price).save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def edit(self, data):
        """
        修改学生课程信息
        :param data:
        :return:
        """
        _id = data.get('id')
        student = data.get('student')
        subject = data.get('subject')
        price = data.get('price')

        if not all([student, subject, price]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        if not all([isinstance(student, int), isinstance(subject, int), isinstance(price, int)]):
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        if price < 0 or price > 9999:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        lesson_of_student = LessonOfStudent.objects.filter(pk=_id).first()
        if not lesson_of_student:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        student = StudentInfo.objects.filter(pk=student).first()
        if not student:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        subject = SubjectInfo.objects.filter(pk=subject).first()
        if not subject:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        if subject.kind == subject.CLASS_TYPE[2][0]:
            name = '%s(%s)' % ('小班课', subject.name)
            lesson_info = LessonInfo.objects.filter(subject=subject).first()
            if not lesson_info:
                lesson_info = LessonInfo(name=name, subject=subject)
                lesson_info.save()
            if lesson_of_student.lesson != lesson_info:
                if not LessonOfStudent.objects.filter(lesson=lesson_of_student.lesson).count() - 1:
                    lesson_of_student.lesson.delete()
        else:
            name = '%s(%s)' % (student.name, subject.name)
            lesson_info = lesson_of_student.lesson
            lesson_info.name = name
            lesson_info.subject = subject
            lesson_info.save()

        try:
            lesson_of_student.student = student
            lesson_of_student.lesson = lesson_info
            lesson_of_student.price = price
            lesson_of_student.save()

            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def delete(self, data):
        """
        删除学生课程信息
        :param data:
        :return:
        """
        _id = data.get('id')
        lesson_of_student = LessonOfStudent.objects.filter(pk=_id).first()
        if not lesson_of_student:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        lesson_info = lesson_of_student.lesson
        lesson_of_student.delete()
        if lesson_info.subject.kind == SubjectInfo.CLASS_TYPE[2][0]:
            if not LessonOfStudent.objects.filter(lesson=lesson_info).count():
                lesson_info.delete()
        else:
            lesson_info.delete()
        return JsonResponse(errmsg.SUCCESS)


class TeacherLessonView(View):
    """老师课程管理页面"""
    def get(self, request):
        teacher_list = TeacherInfo.objects.all()
        lesson_list = LessonInfo.objects.all()
        lesson_of_teacher_list = LessonOfTeacher.objects.all()
        context = {
            'title': '老师课程管理',
            'modal_title': '老师课程信息',
            'add_button': '添加老师课程',
            'teacher_list': teacher_list,
            'lesson_list': lesson_list,
            'lesson_of_teacher_list': lesson_of_teacher_list,
        }
        return render(request, 'lesson/teacheroflesson.html', context)


class TeacherLessonInfoView(View):
    """老师课程管理信息"""
    def get(self, request):
        _id = request.GET.get('id')
        if not _id:
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        lesson_of_teacher = LessonOfTeacher.objects.filter(pk=_id).first()
        if not lesson_of_teacher:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        data = {
            'teacher': lesson_of_teacher.teacher.pk,
            'lesson': lesson_of_teacher.lesson.pk,
            'price': lesson_of_teacher.price,
        }
        success = copy.deepcopy(errmsg.SUCCESS)
        success.update({'data': data})
        return JsonResponse(success)

    def post(self, request):
        # 处理接收的数据
        data = parse_json(request)
        print(data)
        if not data:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)
        # 处理的方法
        method = {
            'add': self.add,
            'edit': self.edit,
            'delete': self.delete,
        }
        option = method.get(data.get('type'))
        if not option:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        return option(data)

    def add(self, data):
        """
        添加老师课程信息
        :param data:
        :return:
        """
        teacher = data.get('teacher')
        lesson = data.get('lesson')
        price = data.get('price')

        if not all([teacher, lesson, price]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        if not all([isinstance(teacher, int), isinstance(lesson, int), isinstance(price, int)]):
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        if price < 0 or price > 9999:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        teacher = TeacherInfo.objects.filter(pk=teacher).first()
        if not teacher:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        lesson_info = LessonInfo.objects.filter(pk=lesson).first()
        if not lesson_info:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        try:
            LessonOfTeacher(lesson=lesson_info, teacher=teacher, price=price).save()
            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def edit(self, data):
        """
        修改老师课程信息
        :param data:
        :return:
        """
        _id = data.get('id')
        teacher = data.get('teacher')
        lesson = data.get('lesson')
        price = data.get('price')

        if not all([teacher, lesson, price]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        if not all([isinstance(teacher, int), isinstance(lesson, int), isinstance(price, int)]):
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)

        if price < 0 or price > 9999:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        lesson_of_teacher = LessonOfTeacher.objects.filter(pk=_id).first()
        if not lesson_of_teacher:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        teacher = TeacherInfo.objects.filter(pk=teacher).first()
        if not teacher:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        lesson = LessonInfo.objects.filter(pk=lesson).first()
        if not lesson:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        try:
            lesson_of_teacher.teacher = teacher
            lesson_of_teacher.lesson = lesson
            lesson_of_teacher.price = price
            lesson_of_teacher.save()

            return JsonResponse(errmsg.SUCCESS)
        except:
            return JsonResponse(errmsg.DATA_SAVE_ERROR)

    def delete(self, data):
        """
        删除老师课程信息
        :param data:
        :return:
        """
        _id = data.get('id')
        if not _id:
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        lesson_of_teacher = LessonOfTeacher.objects.filter(pk=_id).first()
        if not lesson_of_teacher:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        lesson_of_teacher.delete()
        return JsonResponse(errmsg.SUCCESS)


class ScheduleView(View):
    """课表"""
    def get(self, request):
        # 所有的课程
        lesson_of_teacher_list = LessonOfTeacher.objects.all()
        # 获取本周第一天日期
        now = datetime.date.today()
        this_week_start = now - datetime.timedelta(days=now.weekday())
        # 本周的所有课程
        schedule = ScheduleLessonInfo.objects.filter(start__gte=this_week_start, start__lt=this_week_start+datetime.timedelta(days=7))
        lesson_info_list = []
        date_list = []
        morning_list = []
        afternoon_list = []
        night_list = []
        for day in range(7):
            date = this_week_start + datetime.timedelta(days=day)

            d = '%s月%s日 %s' % (date.month, date.day, self.get_weed_day(date))
            print(d)
            date_list.append(d)

            schedule_date = schedule.filter(start__date=date)
            morning = schedule_date.filter(start__hour__lte=11)
            afternoon = schedule_date.filter(start__hour__gte=12, start_hour_lt=17)
            night = schedule_date.filter(start__hour__gte=17)
            morning_list.append(morning)
            afternoon_list.append(afternoon)
            night_list.append(night)
        lesson_info = {
            'date_list': date_list,
            'morning': morning_list,
            'afternoon': afternoon_list,
            'night': night_list,
        }
        lesson_info_list.append(lesson_info)

        context = {
            'title': '课表',
            'modal_title': '课程安排',
            'add_button': '添加课程',
            'lesson_of_teacher_list': lesson_of_teacher_list,
            'lesson_info_list': lesson_info_list,
        }
        return render(request, 'lesson/schedule.html', context)

    def get_weed_day(self, date):
        """
        获取星期几
        :param date: 日期
        :return: 星期几
        """
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期天',
        }
        day = date.weekday()
        return week_day_dict[day]


class ScheduleInfoView(View):
    """课表信息"""
    def get(self, request):
        _id = request.GET.get('id')
        if not _id:
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        schedule_info = ScheduleLessonInfo.objects.filter(pk=_id).first()
        if not schedule_info:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        data = {
            'lesson_of_teacher': schedule_info.lesson_of_teacher.id,
            'start': schedule_info.start,
            'end': schedule_info.end,
        }
        success = copy.deepcopy(errmsg.SUCCESS)
        success.update({'data': data})
        return JsonResponse(success)

    def post(self, request):
        # 处理接收的数据
        data = parse_json(request)
        print(data)
        if not data:
            return JsonResponse(errmsg.PARAMETER_TYPE_ERROR)
        # 处理的方法
        method = {
            'add': self.add,
            'edit': self.edit,
            'delete': self.delete,
        }
        option = method.get(data.get('type'))
        if not option:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        return option(data)

    def add(self, data):
        lesson_of_teacher = data.get('lesson_of_teacher')
        start = data.get('start')
        end = data.get('end')

        if not all([lesson_of_teacher, start, end]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        lesson_of_teacher = LessonOfTeacher.objects.filter(pk=lesson_of_teacher).first()
        if not lesson_of_teacher:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        try:
            start_time = datetime.datetime.strptime(start, '%Y%m%d %S:%M')
            end_time = datetime.datetime.strptime(end, '%Y%m%d %S:%M')
        except:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        ScheduleLessonInfo(lesson_of_teacher=lesson_of_teacher, start=start_time, end=end_time).save()
        return JsonResponse(errmsg.SUCCESS)

    def edit(self, data):
        _id = data.get('id')
        lesson_of_teacher = data.get('lesson_of_teacher')
        start = data.get('start')
        end = data.get('end')

        if not all([_id, lesson_of_teacher, start, end]):
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        schedule = ScheduleLessonInfo.objects.filter(pk=_id).first()
        if not schedule:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        lesson_of_teacher = LessonOfTeacher.objects.filter(pk=lesson_of_teacher).first()
        if not lesson_of_teacher:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        try:
            start_time = datetime.datetime.strptime(start, '%Y%m%d %S:%M')
            end_time = datetime.datetime.strptime(end, '%Y%m%d %S:%M')
        except:
            return JsonResponse(errmsg.PARAMETER_ERROR)

        schedule.lesson_of_teacher = lesson_of_teacher
        schedule.start = start_time
        schedule.end = end_time
        schedule.save()
        return JsonResponse(errmsg.SUCCESS)

    def delete(self, data):
        _id = data.get('id')
        if not _id:
            return JsonResponse(errmsg.INCOMPLETE_PARAMETERS)

        schedule = ScheduleLessonInfo.objects.filter(pk=_id).first()
        if not schedule:
            return JsonResponse(errmsg.NO_SUCH_DATA)

        schedule.delete()
        return JsonResponse(errmsg.SUCCESS)


