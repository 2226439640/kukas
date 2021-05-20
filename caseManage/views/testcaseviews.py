import json, os
from django.shortcuts import render, HttpResponse
from xlwt import Workbook
from caseManage.models import *
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db import connection
from django.http import JsonResponse
from threading import Thread, Lock


mylock = Lock()

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


def downcases(request):
    search_case = request.GET.get('searchcase')
    tag_level = request.GET.get('taglevel')
    searchs = ""
    if ',' in search_case:
        for c in search_case.split(','):
            searchs += f'find_in_set("{c}", tag) or '
        searchs = searchs[:-4]
    else:
        searchs = f"find_in_set('{search_case}', tag)"
    if tag_level != "":
        if search_case != "":
            sql = f'select * from studentcases where (caseName="{search_case}" or {searchs}) and grade="{tag_level}";'
        else:
            sql = f'select * from studentcases where grade="{tag_level}";'
    else:
        sql = f'select * from studentcases where caseName="{search_case}" or {searchs};'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        query = cursor.fetchall()
    ws = Workbook(encoding='utf-8')

    def saveFile(query):
        mylock.acquire()
        if query:
            w = ws.add_sheet(u"用例列表")
            w.write(0, 0, u"用例名称")
            w.write(0, 1, u"前置条件")
            w.write(0, 2, u"步骤")
            w.write(0, 3, u"预期结果")
            w.write(0, 4, u"需求id")
            w.write(0, 5, u"标签")
            w.write(0, 6, u"等级")
            w.write(0, 7, u"创建人")
            # 写入数据

            excel_row = 1
            for obj in query:
                data_casename = obj[1]
                data_casepre = obj[2]
                data_casestep = obj[3]
                data_caseresult = obj[4]
                data_needid = obj[5]
                data_tag = obj[6]
                data_grade = obj[7]
                data_creator = obj[9]
                w.write(excel_row, 0, data_casename)
                w.write(excel_row, 1, data_casepre)
                w.write(excel_row, 2, data_casestep)
                w.write(excel_row, 3, data_caseresult)
                w.write(excel_row, 4, data_needid)
                w.write(excel_row, 5, data_tag)
                w.write(excel_row, 6, data_grade)
                w.write(excel_row, 7, data_creator)
                excel_row += 1

    thread = Thread(target=saveFile, args=(query,))
    thread.start()
    thread.join()
    ws.save("测试用例.xlsx")
    with open("测试用例.xlsx", "rb") as fp:
        response = HttpResponse(fp, content_type='application/vnd.ms-excel')
        from urllib import parse
        name = parse.quote("测试用例.xlsx")
        response['Content-Disposition'] = f'attachment;filename={name}'
        mylock.release()
    os.remove("测试用例.xlsx")
    return response

