from django.shortcuts import render, HttpResponse
from caseManage.models import *
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
import json
from django.db import connection
from django.http import JsonResponse


def getAllCases(request):

    return render(request, 'index.html')


def insertCase(request):
    pass

def students(request, page):
    queryset = StudentCases.objects.all()
    paginator = Paginator(queryset, 10)
    try:
        student = paginator.page(page)
    except PageNotAnInteger:
        student = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        student = paginator.page(paginator.num_pages)

    res = serializers.serialize('json', student)
    res = json.loads(res)
    return render(request, 'student.html', {"students": res, "pageNums": range(1, paginator.num_pages+1), "pageNow": int(page)})

def teachers(request, page):
    queryset = TeacherCases.objects.all()
    paginator = Paginator(queryset, 10)
    try:
        teacher = paginator.page(page)
    except PageNotAnInteger:
        teacher = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        teacher = paginator.page(paginator.num_pages)

    res = serializers.serialize('json', teacher)
    res = json.loads(res)
    return render(request, 'teacher.html', {"teachers": res, "pageNums": range(1, paginator.num_pages+1), "pageNow": int(page)})


def learns(request, page):
    queryset = LearnCases.objects.all()
    paginator = Paginator(queryset, 10)
    try:
        learn = paginator.page(page)
    except PageNotAnInteger:
        learn = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        learn = paginator.page(paginator.num_pages)

    res = serializers.serialize('json', learn)
    res = json.loads(res)
    return render(request, 'learn.html', {"learns": res, "pageNums": range(1, paginator.num_pages+1), "pageNow": int(page)})


def questions(request, page):
    queryset = QuestioCases.objects.all()
    paginator = Paginator(queryset, 10)
    try:
        question = paginator.page(page)
    except PageNotAnInteger:
        question = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        question = paginator.page(paginator.num_pages)

    res = serializers.serialize('json', question)
    res = json.loads(res)
    return render(request, 'question.html', {"questions": res, "pageNums": range(1, paginator.num_pages+1), "pageNow": int(page)})


def princpals(request, page):
    queryset = PrincipalCases.objects.all()
    paginator = Paginator(queryset, 10)
    try:
        princpal = paginator.page(page)
    except PageNotAnInteger:
        princpal = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        princpal = paginator.page(paginator.num_pages)

    res = serializers.serialize('json', princpal)
    res = json.loads(res)
    return render(request, 'princpal.html', {"princpals": res, "pageNums": range(1, paginator.num_pages+1), "pageNow": int(page)})


def others(request, page):
    queryset = OtherCases.objects.all()
    paginator = Paginator(queryset, 10)
    try:
        other = paginator.page(page)
    except PageNotAnInteger:
        other = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        other = paginator.page(paginator.num_pages)

    res = serializers.serialize('json', other)
    res = json.loads(res)
    return render(request, 'other.html', {"others": res, "pageNums": range(1, paginator.num_pages+1), "pageNow": int(page)})


def uploadCase(request):
    data = json.loads(request.body.decode("utf-8"))
    data["user"] = Users.objects.get(uid=request.session["userid"])
    case = StudentCases.objects.create(**data)
    case.save()

    return students(request, 1)


def updateCase(request):
    data = json.loads(request.body.decode("utf-8"))
    case = StudentCases.objects.filter(caseid=data['caseid'])
    for i in range(len(case)):
        case[i].caseName = data['caseName']
        case[i].casePre = data['casePre']
        case[i].caseStep = data['caseStep']
        case[i].caseResult = data['caseResult']
        case[i].needid = data['needid']
        case[i].tag = data['tag']
        case[i].grade = data['grade']
        case[i].creatorname = request.session['username']
        case[i].user_id = request.session['userid']
        case[i].save()

    return HttpResponse("修改成功")


def delCase(request):
    data = json.loads(request.body.decode("utf-8"))
    StudentCases.objects.filter(caseid=data['caseid']).delete()
    return HttpResponse("删除成功")


def searchcase(request, page):
    data = json.loads(request.body.decode("utf-8"))
    search_case = data['searchcase']
    tag_level = data['taglevel']
    if tag_level != "":
        if search_case != "":
            sql = f'select * from studentcases where (caseName="{search_case}" or tag="{search_case}") and grade="{tag_level}";'
        else:
            sql = f'select * from studentcases where grade="{tag_level}";'
    else:
        sql = f'select * from studentcases where caseName="{search_case}" or tag="{search_case}";'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        query = cursor.fetchall()
    paginator = Paginator(query, 10)
    try:
        princpal = paginator.page(page)
    except PageNotAnInteger:
        princpal = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        princpal = paginator.page(paginator.num_pages)
    res = dict()
    res["result"] = princpal.object_list
    res["pageNums"] = paginator.num_pages
    res["pageNow"] = int(page)
    return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})

