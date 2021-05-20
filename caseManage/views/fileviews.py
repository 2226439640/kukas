from django.shortcuts import render, HttpResponse
from caseManage.updateFile import updateFile
from tools.forms import FileForm
from caseManage.models import Users,CaseFiles, StudentCases
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.utils.http import urlquote
from django.db import connection
from threading import Thread
import json,shutil
import os
from datetime import datetime


def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')


#删除文件
def delfileCase(request):
    fiid = request.GET.get('fileid')
    CaseFiles.objects.filter(fid=fiid).delete()
    return HttpResponseRedirect("/file/fileall/1/")


#dir_path是文件的存放地目录，tar_path是文件下载的目的地
def downFile(request):
    fid = request.GET.get('fileid')
    res = CaseFiles.objects.get(fid=fid)
    file = open(os.path.join(res.filepath, res.filename), "rb")
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    from urllib import parse
    name = parse.quote(res.filename)
    response['Content-Disposition'] = f"attachment;filename={name}"
    return response


#TODO
def getAllFiles(request, page):
    sql = "select c.fid, c.filename, c.endupdate, u.`name` from casefiles AS c, users AS u where c.user_id = u.uid;"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        query = cursor.fetchall()
    print(query)
    paginator = Paginator(query, 10)
    try:
        casefiles = paginator.page(page)
    except PageNotAnInteger:
        casefiles = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        casefiles = paginator.page(paginator.num_pages)
    return render(request, 'file.html', {"casefiles": casefiles, "pageNums": range(1, paginator.num_pages+1), "pageNow": int(page)})


def upload1(request,class_id):
    # 判断是否有session
    username = request.session.get("username")
    if username:
        if request.method == "POST":
            File = FileForm(request.POST, request.FILES)
            if File.is_valid():
                file_name = File.cleaned_data["file_name"]

                # 向数据库中新增用例文件数据
                case_file = CaseFiles()
                case_file.fid = int(class_id)
                case_file.filename = file_name
                case_file.filepath = os.path.join('../upload', file_name)
                case_file.save()

                # 返回上传成功
                messages.add_message(request, messages.INFO, u"上传成功!")
            else:
                ff = FileForm()
                messages.add_message(request, messages.INFO, u"请选择文件!")
                return HttpResponseRedirect("/caseList/" + class_id, {"ff": ff})
        else:
            ff = FileForm()
            return HttpResponseRedirect("/caseList/" + class_id, {"ff": ff})
    else:
        # 如果没有session,重定向到路由 /login/, 返回表单
        uf = Users(request.POST)
        #重定向
        return HttpResponseRedirect("/login/", {"uf": uf})


def synDB(filename, username, id):
    update = updateFile()
    update(fileFlag=False, filename=filename)
    for row in range(1, update.cases.nrows):
        if update.cases.cell(row, update.cases.ncols-1).value == 1:
            case = StudentCases.objects.get(caseid=update.cases.cell(row, 0).value)
            if case:
                case.caseName = update.cases.cell(row, 1).value
                case.casePre = update.cases.cell(row, 2).value
                case.caseStep = update.cases.cell(row, 3).value
                case.caseResult = update.cases.cell(row, 4).value
                case.needid = update.cases.cell(row, 5).value
                case.tag = update.cases.cell(row, 6).value
                case.grade = update.cases.cell(row, 7).value
                case.creatorname = username
                case.user_id = id
                case.save()
            else:
                caseNew = dict()
                caseNew["caseName"] = update.cases.cell(row, 1).value
                caseNew["casePre"] = update.cases.cell(row, 2).value
                caseNew["caseStep"] = update.cases.cell(row, 3).value
                caseNew["caseResult"] = update.cases.cell(row, 4).value
                caseNew["needid"] = update.cases.cell(row, 5).value
                caseNew["tag"] = update.cases.cell(row, 6).value
                caseNew["grade"] = update.cases.cell(row, 7).value
                caseNew["creatorname"] = username
                caseNew["user_id"] = id
                case = StudentCases.objects.create(**caseNew)
                case.save()


def upload(request):
    """
    上传文件
    :param request:
    :return:
    """
    if request.method == 'POST':
        file = request.FILES.get("file")
        if ".xls" not in file.name:
            return render(request, "file.html", {"message": "上传文件格式不对!"})
        def save(obj, dirpath):
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            fp = open(os.path.join(dirpath, obj.name), "wb")
            for chunk in obj.chunks():
                fp.write(chunk)
            fp.close()
            synDB(os.path.join(dirpath, obj.name), request.session['username'], request.session['userid'])
        data = dict()
        data['filename'] = file.name
        data['filepath'] = os.path.join(r'../upload', datetime.strftime(datetime.now(), "%Y%m%d-%H%M%S"))
        data['user_id'] = request.session['userid']
        files = CaseFiles.objects.create(**data)
        files.save()
        th = Thread(target=save, args=(file, data["filepath"],))
        th.start()
        th.join()
        messages.add_message(request, messages.INFO, u"上传成功!")
        return HttpResponse('上传成功!')
    else:
        return render(request, "upload.html")


if __name__ == '__main__':
    pass
