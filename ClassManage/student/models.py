from django.db import models


# Create your models here.
class StudentInfo(models.Model):
    GRADE = (
        (0, '其他'),
        (1, '一年级'),
        (2, '二年级'),
        (3, '三年级'),
        (4, '四年级'),
        (5, '五年级'),
        (6, '六年级'),
        (7, '初一'),
        (8, '初二'),
        (9, '初三'),
        (10, '高一'),
        (11, '高二'),
        (12, '高三'),
    )
    name = models.CharField(verbose_name='学生姓名', max_length=20)
    gender = models.BooleanField(verbose_name='性别', default=False)
    age = models.IntegerField(verbose_name='年龄', null=True, blank=True)
    grade = models.IntegerField(verbose_name='年级', choices=GRADE, default=GRADE[4][0], null=True, blank=True)

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


class StudentOfLesson(models.Model):
    lesson = models.ForeignKey(verbose_name='课程信息', to='lesson.LessonInfo', on_delete=models.CASCADE)
    student = models.ForeignKey(verbose_name='学生信息', to=StudentInfo, on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='学生课时费', max_digits=18, decimal_places=2)

    def __str__(self):
        return self.lesson.name

    class Meta:
        verbose_name = '学生课程关系表'
        verbose_name_plural = verbose_name
