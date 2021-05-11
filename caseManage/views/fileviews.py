from django.shortcuts import render, HttpResponse
from caseManage.updateFile import updateFile
from tools.forms import FileForm
from caseManage.models import Users,CaseFiles
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
import datetime,os,pymysql
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.utils.http import urlquote
from caseManage.models import CaseFiles
from django.db import connection
from threading import Thread
import json


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


def upload(request):
    """
    上传文件
    :param request:
    :return:
    """
    if request.method == 'POST':
        file = request.FILES.get("file")
        def save(obj):
            import os
            fp = open(os.path.join('../upload', obj.name), "wb")
            for chunk in obj.chunks():
                fp.write(chunk)
            fp.close()
        th = Thread(target=save, args=(file,))
        th.start()
        th.join()
        messages.add_message(request, messages.INFO, u"上传成功!")
        return HttpResponse('上传成功!')
    else:
        return render(request, "upload.html")


def download(request):
    file = open('crm/models.py','rb')
    response =FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="models.py"'
    return response


def download1(table_name):  #tag,creatorname,update
    '''
    通过搜索 标签/用例名称/风险等级/创建人/时间 导出excel
    '''
    # 连接数据库，查询数据
    host, user, passwd, db = '127.0.0.1', 'root', 'mql123', 'tptcase'
    conn = pymysql.connect(user=user, host=host, port=3306, passwd=passwd, db=db, charset='utf8')
    cur = conn.cursor()
    sql = 'select * from %s' % table_name
    cur.execute(sql)  # 返回受影响的行数

    fields = [field[0] for field in cur.description]  # 获取所有字段名
    all_data = cur.fetchall()  # 所有数据

    # 写入excel
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')

    for col, field in enumerate(fields):
        sheet.write(0, col, field)

    row = 1
    for data in all_data:
        for col, field in enumerate(data):
            sheet.write(row, col, field)
        row += 1
    book.save("caseManage/upload/%s.xls" % table_name)


if __name__ == '__main__':
    t1 = Thread(target=download, args=('users',))
    t1.start()
    # download('users')
#xxxxx
    from io import BytesIO
    import xlwt


    # 导出查询的数据
    def export_data(request):
        print("--导出请求到后台--")
        dict_data = {}
        data = []
        if request.method == "POST":
            # 获取前台页面参数
            case_name = request.POST.get("case_name")
            print("case_name", case_name)
            need_id = request.POST.get("need_id")
            print("need_id", need_id)
            tag = request.POST.get("tag")
            print("tag", tag)
            grade = request.POST.get("grade")
            print("grade", grade)
            creatorname = request.POST.get("creatorname")
            print("creatorname", creatorname)

            dict_param = {}
            if case_name:
                # print("1")
                dict_param["case_name_icontains"] = case_name
            if need_id:
                # print("2")
                dict_param["need_id_icontains"] = need_id
            if tag:
                # print("3")
                dict_param["tag_icontains"] = tag
            if grade:
                # print("4")
                dict_param["grade_icontains"] = grade
            if creatorname:
                # print("4")
                dict_param["creatorname_icontains"] = creatorname

            # 去数据库查询数据
            if case_name or need_id or tag or grade or creatorname:
                print("--按条件查--")
                products = TeacherCases.objects.filter(**dict_param)
            else:
                print("--全部查--")
                products = TeacherCases.objects.all()

            data = list(products)

            row_num = len(data)
            # 查询为空
            if row_num <= 0:
                data = []
                page_total = 0
                brand_list = []
                model_list = []
                message = "查询为空，不能导出Excel。"
                dict_data = {"row_num": row_num, "data": data, "msg": message}
                dict_data = json.dumps(dict_data)
                print(dict_data)
                return HttpResponse(dict_data)
            else:
                print("--导出--")
                ezxf = xlwt.easyxf
                # 可编辑,horz center:水平居中,vert center:垂直居中,还可以在这里设置其他样式,颜色,边框等
                edit_able = ezxf("protection: cell_locked false;align: horz center,vert center;")
                # 不可編輯,horz center:水平居中,vert center:垂直居中,还可以在这里设置其他样式,颜色,边框等
                read_only = ezxf("protection: cell_locked true;align: horz center,vert center;")
                # 导出excel表
                if data:
                    # 创建工作簿
                    ws = xlwt.Workbook(encoding='utf-8')
                    # 添加第一页数据表
                    w = ws.add_sheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
                    w.protect = True  # 設置保護
                    w.password = "railor123456789"  # 設置密碼
                    # 写入表头
                    w.write(0, 0, u'用例id', style=read_only)  # case_id
                    w.write(0, 1, u'用例名称', style=read_only)  # caseName
                    w.col(1).width = 256 * 20

                    w.write(0, 2, u'前置条件', style=read_only)  # casePre
                    w.col(2).width = 256 * 40

                    w.write(0, 3, u'用例步骤', style=read_only)  # caseStep
                    w.col(3).width = 256 * 40

                    w.write(0, 4, u'预期结果', style=read_only)  # caseResult
                    w.col(4).width = 256 * 40

                    w.write(0, 5, u'需求id', style=read_only)  # needid
                    w.col(5).width = 256 * 25

                    w.write(0, 6, u'标签', style=read_only)  # tag
                    w.col(6).width = 256 * 30

                    w.write(0, 7, u'等级', style=read_only)  # grade
                    w.col(7).width = 256 * 30

                    w.write(0, 8, u'最后更新时间', style=read_only)  # endupdate
                    w.write(0, 9, u'创建人', style=read_only)  # creatorname
                    w.write(0, 10, u'用户名', style=read_only)  # userid
                    # 写入数据

                    for i in range(len(data)):
                        excel_row = data[i]
                        n = i + 1
                        # 写入每一行对应的数据
                        w.write(n, 0, data[i].product_id, style=read_only)  # case_id
                        w.write(n, 1, data[i].product_code, style=read_only)  # caseName
                        w.write(n, 2, data[i].product_name, style=read_only)  # casePre
                        w.write(n, 3, data[i].product_brand, style=edit_able)  # caseStep

                        w.write(n, 4, data[i].product_model, style=read_only)  # caseResult
                        w.write(n, 5, data[i].product_place, style=edit_able)  # needid
                        w.write(n, 6, data[i].product_desc, style=edit_able)  # tag
                        w.write(n, 7, data[i].product_size, style=edit_able)  # grade
                        w.write(n, 8, data[i].product_length, style=edit_able)  # endupdate
                        w.write(n, 9, data[i].product_width, style=edit_able)  # creatorname
                        w.write(n, 10, data[i].product_height, style=edit_able)  # userid
                    # 写出到IO
                    output = BytesIO()
                    ws.save(output)
                    # 重新定位到开始
                    output.seek(0)
                    # 设置HTTPResponse的类型
                    response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment;filename=' + excel_file_name + '.xls'
                    response.write(output.getvalue())

                return response
