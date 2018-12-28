import json
import copy

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
        return render(request, 'lesson/subject.html')


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

        # subject = SubjectInfo.objects.filter(pk=_id).last()
        # if not subject:
        #     return JsonResponse(errmsg.NO_SUCH_DATA)

        # data = {
        #     'id': subject.pk,
        #     'name': subject.name,
        #     'kind': subject.kind,
        # }
        data = {
            'id': 1,
            'name': 'ddddd',
            'kind': 1,
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

        if not all([name, kind]):
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

        if not all([_id, name, kind]):
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
        return render(request, 'lesson/studentoflesson.html')


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
            name = subject.name
        else:
            name = '%s(%s)' % (student.name, subject.name)

        try:
            lesson_info = LessonInfo(name=name, subject=subject)
            lesson_info.save()
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
            name = subject.name
        else:
            name = '%s(%s)' % (student.name, subject.name)

        try:
            lesson_info = lesson_of_student.lesson
            lesson_info.name = name
            lesson_info.subject = subject
            lesson_info.save()

            lesson_of_student.student = student
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
        lesson_info.delete()
        return JsonResponse(errmsg.SUCCESS)


class TeacherLessonView(View):
    """老师课程管理页面"""
    def get(self, request):
        return render(request, 'lesson/teacheroflesson.html')


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
