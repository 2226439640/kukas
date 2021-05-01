from django.shortcuts import render, HttpResponse
from caseManage.updateFile import updateFile
from tools.forms import FileForm
from caseManage.models import Users,CaseFiles
from django.http import HttpResponse, HttpResponseRedirect,FileResponse
import datetime,os
from django.contrib import messages
from django.utils.http import urlquote
from threading import Thread
import _thread as thread


#TODO
def getAllFiles(request):
    pass

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

def upload(request):

    # t1 = Thread(target=up,args=(request))
    # t1.start()
#     return thread.start_new_thread(up,(request,))
#
# def up(request):
    """
            上传文件
            :param request:
            :return:
            """
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            # 选择的文件
            files = request.FILES.getlist('file')
            use= Users()
            us=Users.objects.filter(uid=1)
            # us = request.user
            # 遍历写入到数据库中
            for file in files:
                # 写入到数据库中

                file_model = CaseFiles(filename=file.name, filepath=os.path.join('../upload', file.name),
                                        user=us.name) #updatev =datetime.datetime.now(),user=""
                file_model.save()

                # 写入到服务器本地
                destination = open(os.path.join("../upload", file.name), 'wb+')
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()

            # 提示上传成功
            return HttpResponse('上传成功!')
    else:
        form = FileForm()
        return render(request, "upload.html", locals())


def download(request):
    '''
    通过搜索 标签/用例名称/风险等级/创建人/时间 导出excel
    '''

    pass



    # file_result = CaseFiles.objects.filter(id=id)
    #
    # # 如果文件存在，就下载文件
    # if file_result:
    #
    #     file = list(file_result)[0]
    #
    #     # 文件名称及路径
    #     name = file.filename
    #     path = file.filepath
    #
    #     # 读取文件
    #     file = open(path, 'rb')
    #     response = FileResponse(file)
    #
    #     # 使用urlquote对文件名称进行编码
    #     response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(name)
    #
    #     return response
    # else:
    #     return HttpResponse('文件不存在!')
