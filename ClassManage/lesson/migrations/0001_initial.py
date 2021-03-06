# Generated by Django 2.0.8 on 2019-01-19 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teacher', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='课程名称')),
            ],
            options={
                'verbose_name': '课程信息',
                'verbose_name_plural': '课程信息',
            },
        ),
        migrations.CreateModel(
            name='LessonOfStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='学生课时费')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.LessonInfo', verbose_name='课程信息')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.StudentInfo', verbose_name='学生信息')),
            ],
            options={
                'verbose_name': '学生课程关系表',
                'verbose_name_plural': '学生课程关系表',
            },
        ),
        migrations.CreateModel(
            name='LessonOfTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='老师课时费')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.LessonInfo', verbose_name='课程信息')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.TeacherInfo', verbose_name='老师信息')),
            ],
            options={
                'verbose_name': '老师课程关系表',
                'verbose_name_plural': '老师课程关系表',
            },
        ),
        migrations.CreateModel(
            name='ScheduleLessonInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='开始时间')),
                ('end', models.DateTimeField(verbose_name='结束时间')),
                ('teacher_sliding_price', models.IntegerField(default=0, verbose_name='老师变动价格')),
                ('lesson_of_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.LessonOfTeacher', verbose_name='老师课程')),
            ],
            options={
                'verbose_name': '排课表',
                'verbose_name_plural': '排课表',
            },
        ),
        migrations.CreateModel(
            name='SubjectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='科目种类')),
                ('kind', models.IntegerField(choices=[(0, '晚辅'), (1, '一对一'), (2, '小班课'), (3, '兼职')], default=1, verbose_name='科目类型')),
            ],
            options={
                'verbose_name': '科目种类信息',
                'verbose_name_plural': '科目种类信息',
            },
        ),
        migrations.AddField(
            model_name='lessoninfo',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.SubjectInfo', verbose_name='科目种类'),
        ),
    ]
