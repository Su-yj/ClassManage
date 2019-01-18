from django.db import models


# Create your models here.
class PriceInfo(models.Model):
    schedule = models.ForeignKey(verbose_name='课程', to='lesson.ScheduleLessonInfo', on_delete=models.CASCADE)
    student = models.ForeignKey(verbose_name='学生', to='student.StudentInfo', on_delete=models.CASCADE)
    student_sliding_price = models.IntegerField(verbose_name='学生变动价格', default=0)

    def get_lesson(self):
        """获取课程的信息"""
        return self.schedule.lesson_of_teacher.lesson

    def get_hour(self):
        """获取上课时长"""
        schedule = self.schedule
        hour = schedule.end - schedule.start
        hour = hour.seconds / 3600
        return hour

    def get_student_price(self):
        """获取学生课时费"""
        lesson = self.get_lesson()
        lesson_of_student = lesson.lessonofstudent_set.filter(student=self.student).first()
        return lesson_of_student.price

    class Meta:
        verbose_name = '价格表'
        verbose_name_plural = verbose_name
