from django.db import models
import django.utils.timezone as timezone
# Create your models here.


class Users(models):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=20, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    phone = models.CharField(verbose_name='手机', max_length=20, null=True)
    email = models.CharField(verbose_name='邮箱', max_length=64, null=True)
    limit = models.BooleanField(verbose_name='权限')


class TestCases(models):
    grade_choice = (('high', '高'),
                  ('middle', '中'),
                  ('low', '低'))
    tag_choice = (('teacher', '教师端'), ('student', '学生端'),('principal','校区运营系统'),
                  ('question','题库'),('learn','学习系统'),('rest','其他'))
    caseid = models.AutoField(primary_key=True)
    caseName = models.CharField(verbose_name='用例名称')
    casePre = models.CharField(verbose_name='前置条件')
    caseStep = models.CharField(verbose_name='步骤')
    caseResult = models.CharField(verbose_name='预期结果')
    needid = models.IntegerField(verbose_name='需求id')
    tag = models.CharField(verbose_name='标签', choices=tag_choice)
    grade = models.CharField(verbose_name='等级', choices=grade_choice)
    update = models.DateTimeField(verbose_name='最后更新时间', default=timezone.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')


class CaseFiles(models):
    fid = models.AutoField()
    filename = models.CharField(verbose_name='文件名')
    filepath = models.CharField(verbose_name='文件路径')
    update = models.DateTimeField(verbose_name='最后更新时间', default=timezone.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')