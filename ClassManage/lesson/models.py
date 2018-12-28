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
    kind = models.IntegerField(verbose_name='科目类型', choices=CLASS_TYPE, default=CLASS_TYPE[1][0])

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


class LessonOfStudent(models.Model):
    lesson = models.ForeignKey(verbose_name='课程信息', to=LessonInfo, on_delete=models.CASCADE)
    student = models.ForeignKey(verbose_name='学生信息', to='student.StudentInfo', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='学生课时费', max_digits=18, decimal_places=2)

    def __str__(self):
        return self.lesson.name

    class Meta:
        verbose_name = '学生课程关系表'
        verbose_name_plural = verbose_name


class LessonOfTeacher(models.Model):
    lesson = models.ForeignKey(verbose_name='课程信息', to=LessonInfo, on_delete=models.CASCADE)
    teacher = models.ForeignKey(verbose_name='老师信息', to='teacher.TeacherInfo', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='老师课时费', max_digits=18, decimal_places=2)

    def __str__(self):
        return '%s [%s]' % (self.teacher, self.lesson)

    class Meta:
        verbose_name = '老师课程关系表'
        verbose_name_plural = verbose_name


class ScheduleLessonInfo(models.Model):
    lesson_of_teacher = models.ForeignKey(verbose_name='老师课程', to=LessonOfTeacher, on_delete=models.CASCADE)
    start = models.DateTimeField(verbose_name='开始时间')
    end = models.DateTimeField(verbose_name='结束时间')

    class Meta:
        verbose_name = '排课表'
        verbose_name_plural = verbose_name
