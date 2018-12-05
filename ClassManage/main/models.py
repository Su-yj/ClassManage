import random
import hashlib

from django.db import models


def random_username():
    word = '1234567890qwertyuiopasdfghjklzxcvbnm'
    username = ''.join(random.sample(word, 8))
    return username


class StudentInfo(models.Model):
    name = models.CharField(verbose_name='学生姓名', max_length=20)
    gender = models.BooleanField(verbose_name='性别', default=False)
    age = models.IntegerField(verbose_name='年龄', null=False, blank=True)

    def __str__(self):
        return self.name

    def show_gender(self):
        if self.gender:
            return '男'
        else:
            return '女'

    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = verbose_name


class TeacherInfo(models.Model):
    name = models.CharField(verbose_name='老师姓名', max_length=50)
    gender = models.BooleanField(verbose_name='性别', default=False)
    user = models.CharField(verbose_name='账号', max_length=50, default=random_username)
    password = models.CharField(verbose_name='密码', max_length=40, default='1411678a0b9e25ee2f7c8b2f7ac92b6a74b3f9c5')

    def __str__(self):
        return self.name

    def show_gender(self):
        if self.gender:
            return '男'
        else:
            return '女'

    def encrypt_passwd(self, passwd):
        return hashlib.sha1(passwd.encode()).hexdigest()

    class Meta:
        verbose_name = '老师信息'
        verbose_name_plural = verbose_name


class SubjectInfo(models.Model):
    CLASS_TYPE = (
        (0, '晚辅'),
        (1, '一对一'),
        (2, '小班课'),
        (3, '兼职'),
    )
    name = models.CharField(verbose_name='科目名称', max_length=50)
    class_type = models.IntegerField(verbose_name='科目类型', choices=CLASS_TYPE, default=CLASS_TYPE[1][0])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '科目信息'
        verbose_name_plural = verbose_name


class LessonInfo(models.Model):
    name = models.CharField(verbose_name='课程名称', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name


class StudentToLesson(models.Model):
    lesson = models.ForeignKey(verbose_name='课程', to=LessonInfo, on_delete=models.CASCADE)
    student = models.ForeignKey(verbose_name='学生', to=StudentInfo, on_delete=models.CASCADE)

    def __str__(self):
        return '%s的%s' % (self.student.name, self.lesson.name)

    class Meta:
        verbose_name = '学生课程关系表'
        verbose_name_plural = verbose_name


class ClassPrice(models.Model):
    lesson = models.ForeignKey(verbose_name='课程', to=LessonInfo, on_delete=models.CASCADE)
    student = models.ForeignKey(verbose_name='学生', to=StudentInfo, on_delete=models.CASCADE)
    teacher = models.ForeignKey(verbose_name='老师', to=TeacherInfo, on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='价格', max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = '课程价格'
        verbose_name_plural = verbose_name
