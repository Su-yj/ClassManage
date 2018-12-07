import random
import base64
import hashlib

from django.db import models


def random_username():
    """
    获取随机用户名
    :return: 随机用户名
    """
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
    password = models.CharField(verbose_name='密码', max_length=40, default=encrypt_password('666666'))

    def __str__(self):
        return self.name

    def show_gender(self):
        if self.gender:
            return '男'
        else:
            return '女'

    @staticmethod
    def encrypt_password(password):
        """
        加密密码
        :param password: 明文密码
        :return: 加密后的密码
        """
        m = hashlib.md5(password.encode()).hexdigest()
        b = base64.b64encode(m.encode())
        return hashlib.sha1(b).hexdigest()

    class Meta:
        verbose_name = '老师信息'
        verbose_name_plural = verbose_name


class SubjectInfo(models.Model):
    """
    课程种类，仅用于显示有多少种课程
    """
    CLASS_TYPE = (
        (0, '晚辅'),
        (1, '一对一'),
        (2, '小班课'),
        (3, '兼职'),
    )
    name = models.CharField(verbose_name='科目种类', max_length=50)
    class_type = models.IntegerField(verbose_name='科目类型', choices=CLASS_TYPE, default=CLASS_TYPE[1][0])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '科目种类信息'
        verbose_name_plural = verbose_name


class LessonInfo(models.Model):
    name = models.CharField(verbose_name='课程名称', max_length=50)
    subject = models.ForeignKey(verbose_name='科目种类', to=SubjectInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name


class StudentOfLesson(models.Model):
    lesson = models.ForeignKey(verbose_name='课程信息', to=LessonInfo, on_delete=models.CASCADE)
    student = models.ForeignKey(verbose_name='学生信息', to=StudentInfo, on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='学生课时费', max_digits=18, decimal_places=2)

    def __str__(self):
        return self.lesson.name

    class Meta:
        verbose_name = '学生课程关系表'
        verbose_name_plural = verbose_name


class TeacherOfLesson(models.Model):
    # lesson = models.ForeignKey(verbose_name='学生课程信息', to=StudentOfLesson, on_delete=models.CASCADE)
    lesson = models.ForeignKey(verbose_name='课程信息', to=LessonInfo, on_delete=models.CASCADE)
    teacher = models.ForeignKey(verbose_name='老师信息', to=TeacherInfo, on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='老师课时费', max_digits=18, decimal_places=2)

    def __str__(self):
        return '%s[%s]' % (self.teacher, self.lesson)

    class Meta:
        verbose_name = '老师课程关系表'
        verbose_name_plural = verbose_name


class ScheduleLessonInfo(models.Model):
    lesson = models.ForeignKey(verbose_name='课程', to=TeacherOfLesson, on_delete=models.CASCADE)
    schedule = models.DateTimeField(verbose_name='上课时间')
    hour = models.DecimalField(verbose_name='课时', default=2)

    class Meta:
        verbose_name = '排课表'
        verbose_name_plural = verbose_name
