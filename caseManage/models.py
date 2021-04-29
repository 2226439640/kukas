from django.db import models
import django.utils.timezone as timezone
# Create your models here.

#用户表
class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=20, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    phone = models.CharField(verbose_name='手机', max_length=20, null=True)
    email = models.CharField(verbose_name='邮箱', max_length=64, null=True)
    limit = models.BooleanField(verbose_name='权限')

    "定义数据库名"
    class Meta():
        db_table = "users"

#其他用例表
class OtherCases(models.Model):
    grade_choice = (('high', '高'),
                  ('middle', '中'),
                  ('low', '低'))
    tag_choice = (('teacher', '教师端'), ('student', '学生端'),('principal','校区运营系统'),
                  ('question','题库'),('learn','学习系统'),('rest','其他'))
    caseid = models.AutoField(primary_key=True)
    caseName = models.CharField(verbose_name='用例名称',max_length=100)
    casePre = models.CharField(verbose_name='前置条件',max_length=100)
    caseStep = models.CharField(verbose_name='步骤',max_length=200)
    caseResult = models.CharField(verbose_name='预期结果',max_length=200)
    needid = models.IntegerField(verbose_name='需求id')
    tag = models.CharField(verbose_name='标签', max_length=100,choices=tag_choice)
    grade = models.CharField(verbose_name='等级',max_length=100, choices=grade_choice)
    update = models.DateTimeField(verbose_name='最后更新时间', default=timezone.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')

    "定义数据库名"
    class Meta():
        db_table = "othercases"

#教师端用例表
class TeacherCases(models.Model):
    grade_choice = (('high', '高'),
                    ('middle', '中'),
                    ('low', '低'))
    tag_choice = (('teacher', '教师端'), ('student', '学生端'), ('principal', '校区运营系统'),
                  ('question', '题库'), ('learn', '学习系统'), ('rest', '其他'))
    caseid = models.AutoField(primary_key=True)
    caseName = models.CharField(verbose_name='用例名称', max_length=100)
    casePre = models.CharField(verbose_name='前置条件', max_length=100)
    caseStep = models.CharField(verbose_name='步骤', max_length=200)
    caseResult = models.CharField(verbose_name='预期结果', max_length=200)
    needid = models.IntegerField(verbose_name='需求id')
    tag = models.CharField(verbose_name='标签', max_length=100, choices=tag_choice)
    grade = models.CharField(verbose_name='等级', max_length=100, choices=grade_choice)
    update = models.DateTimeField(verbose_name='最后更新时间', default=timezone.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')
    "定义数据库名"
    class Meta():
        db_table = "teachercases"

#学生端用例表
class StudentCases(models.Model):
    grade_choice = (('high', '高'),
                    ('middle', '中'),
                    ('low', '低'))
    tag_choice = (('teacher', '教师端'), ('student', '学生端'), ('principal', '校区运营系统'),
                  ('question', '题库'), ('learn', '学习系统'), ('rest', '其他'))
    caseid = models.AutoField(primary_key=True)
    caseName = models.CharField(verbose_name='用例名称', max_length=100)
    casePre = models.CharField(verbose_name='前置条件', max_length=100)
    caseStep = models.CharField(verbose_name='步骤', max_length=200)
    caseResult = models.CharField(verbose_name='预期结果', max_length=200)
    needid = models.IntegerField(verbose_name='需求id')
    tag = models.CharField(verbose_name='标签', max_length=100, choices=tag_choice)
    grade = models.CharField(verbose_name='等级', max_length=100, choices=grade_choice)
    update = models.DateTimeField(verbose_name='最后更新时间', default=timezone.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')
    "定义数据库名"
    class Meta():
        db_table = "studentcases"

#学生系统用例表
class LearnCases(models.Model):
    grade_choice = (('high', '高'),
                    ('middle', '中'),
                    ('low', '低'))
    tag_choice = (('teacher', '教师端'), ('student', '学生端'), ('principal', '校区运营系统'),
                  ('question', '题库'), ('learn', '学习系统'), ('rest', '其他'))
    caseid = models.AutoField(primary_key=True)
    caseName = models.CharField(verbose_name='用例名称', max_length=100)
    casePre = models.CharField(verbose_name='前置条件', max_length=100)
    caseStep = models.CharField(verbose_name='步骤', max_length=200)
    caseResult = models.CharField(verbose_name='预期结果', max_length=200)
    needid = models.IntegerField(verbose_name='需求id')
    tag = models.CharField(verbose_name='标签', max_length=100, choices=tag_choice)
    grade = models.CharField(verbose_name='等级', max_length=100, choices=grade_choice)
    update = models.DateTimeField(verbose_name='最后更新时间', default=timezone.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')
    "定义数据库名"
    class Meta():
        db_table = "learncases"

#题库用例表
class QuestioCases(models.Model):
    grade_choice = (('high', '高'),
                    ('middle', '中'),
                    ('low', '低'))
    tag_choice = (('teacher', '教师端'), ('student', '学生端'), ('principal', '校区运营系统'),
                  ('question', '题库'), ('learn', '学习系统'), ('rest', '其他'))
    caseid = models.AutoField(primary_key=True)
    caseName = models.CharField(verbose_name='用例名称', max_length=100)
    casePre = models.CharField(verbose_name='前置条件', max_length=100)
    caseStep = models.CharField(verbose_name='步骤', max_length=200)
    caseResult = models.CharField(verbose_name='预期结果', max_length=200)
    needid = models.IntegerField(verbose_name='需求id')
    tag = models.CharField(verbose_name='标签', max_length=100, choices=tag_choice)
    grade = models.CharField(verbose_name='等级', max_length=100, choices=grade_choice)
    update = models.DateTimeField(verbose_name='最后更新时间', default=timezone.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')
    "定义数据库名"
    class Meta():
        db_table = "questioncases"

#校区运营系统用例表
class PrincipalCases(models.Model):
    grade_choice = (('high', '高'),
                    ('middle', '中'),
                    ('low', '低'))
    tag_choice = (('teacher', '教师端'), ('student', '学生端'), ('principal', '校区运营系统'),
                  ('question', '题库'), ('learn', '学习系统'), ('rest', '其他'))
    caseid = models.AutoField(primary_key=True)
    caseName = models.CharField(verbose_name='用例名称', max_length=100)
    casePre = models.CharField(verbose_name='前置条件', max_length=100)
    caseStep = models.CharField(verbose_name='步骤', max_length=200)
    caseResult = models.CharField(verbose_name='预期结果', max_length=200)
    needid = models.IntegerField(verbose_name='需求id')
    tag = models.CharField(verbose_name='标签', max_length=100, choices=tag_choice)
    grade = models.CharField(verbose_name='等级', max_length=100, choices=grade_choice)
    update = models.DateTimeField(verbose_name='最后更新时间', default=timezone.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')
    "定义数据库名"
    class Meta():
        db_table = "principalcases"

#文件表.
class CaseFiles(models.Model):
    fid = models.AutoField(primary_key=True)
    filename = models.CharField(verbose_name='文件名',max_length=100)
    filepath = models.CharField(verbose_name='文件路径',max_length=200)
    update = models.DateTimeField(verbose_name='最后更新时间', default=timezone.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')
    "定义数据库名"
    class Meta():
        db_table = "casefiles"

