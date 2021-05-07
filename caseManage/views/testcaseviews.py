from django.shortcuts import render, HttpResponse
from caseManage.models import *
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
import json


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

