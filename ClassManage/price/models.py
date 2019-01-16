from django.db import models


# Create your models here.
class PriceInfo(models.Model):
    schedule = models.ForeignKey(verbose_name='课程', to='lesson.ScheduleLessonInfo', on_delete=models.CASCADE)
    teacher = models.ForeignKey(verbose_name='老师', to='teacher.TeacherInfo', on_delete=models.CASCADE)
    student = models.ForeignKey(verbose_name='学生', to='student.StudentInfo', on_delete=models.CASCADE)
    more_price = models.IntegerField(verbose_name='额外的价格', default=0)

    class Meta:
        verbose_name = '价格表'
        verbose_name_plural = verbose_name
