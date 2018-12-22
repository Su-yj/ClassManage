from django.db import models


# Create your models here.
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


class ScheduleLessonInfo(models.Model):
    lesson = models.ForeignKey(verbose_name='课程', to=TeacherOfLesson, on_delete=models.CASCADE)
    start = models.DateTimeField(verbose_name='开始时间')
    end = models.DateTimeField(verbose_name='结束时间')

    class Meta:
        verbose_name = '排课表'
        verbose_name_plural = verbose_name
