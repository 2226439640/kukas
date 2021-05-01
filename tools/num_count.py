#处理文件中的数据并进行入库
import json,xlrd,pymysql
from caseManage.models import PrincipalCases
import os
'根据文件'

#插入数据库  ""
# def insert_db(request):
#     contains = json.loads(parse(file_list))
#     people = request.POST.get("peoples", None)
#     version = request.POST.get("versions", None)
#     if contains:
#         # casefiles = CaseFiles()
#         # principal_case = PrincipalCases()
#         "这一快需要指定分哪个库"
#         pri_model= PrincipalCases(grade_choice=contains['grade_choice'], tag_choice=contains['tag_choice'],
#                                      caseid=contains['caseid'], caseName=contains['caseName'],
#                                      casePre=contains['casePre'],
#                                       caseStep=contains['caseStep'],needid=contains['needid'],
#                                      caseResult=['caseResult'],tag=['tag'],grade=['grade'],update=['update'],user=['user'])
#         pri_model.save()
#         list = PrincipalCases.objects.all()
#         return list
#     else:
#         pri_model = PrincipalCases(grade_choice=contains['grade_choice'], tag_choice=contains['tag_choice'],
#                                    caseid=contains['caseid'], caseName=contains['caseName'],
#                                    casePre=contains['casePre'],
#                                    caseStep=contains['caseStep'], needid=contains['needid'],
#                                    caseResult=['caseResult'], tag=['tag'], grade=['grade'], update=['update'],
#                                    user=['user'])
#         pri_model.save()


#读取excel数据 返回每个具体数据
def parse(file_path):
    file = xlrd.open_workbook(file_path)
    sheet_1 = file.sheet_by_index(0)
    report_name = sheet_1.row_values(0) #获取报表名称行数据
    row_num = sheet_1.nrows #获取行数
    report_num = sheet_1.ncols #获取列数
    for i in range(1,row_num): #循环每一行数据
        row = sheet_1.row_values(i) #获取行数据
        dict = {}
        dict['casename']= "".join(row[0].split()) #用例名称
        # sap_id = "".join(str(row[1]).split())
        # dict['id'] = sap_id.split('.')[0] #编号
        dict['casepre'] = "".join(row[1].split()) #前置条件
        dict['casestep'] = "".join(row[2].split()) #用例步骤
        dict['caseResult'] = "".join(row[3].split()) #预期结果
        dict['needid'] = "".join(str(row[4]).split()) #需求id
        dict['tag'] = "".join(row[5].split()) #标签
        dict['grade'] = "".join(row[6].split()) #等级
        dict['update'] = "".join(row[7].split()) #最后更新时间
        dict['user'] = "".join(row[8].split()) #用户名
        for j in range(0,report_num):
            if row[j] is not '': #如果行内没有数据，则对应报表名称无权限，设为0，否则为1
                dict[report_name[j]] = 1
            else:
                dict[report_name[j]] = 0
        print(dict)
        return dict
        # _result_list = json.dumps(dict)
        # return _result_list   #读取excel中值并对应数据库中具体字段


# 多个文件的情况
def listdir(path): #传入根目录
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file) #获取绝对路径
        if os.path.isdir(file_path): #如果还是文件夹，就继续迭代本函数
            listdir(file_path)
        elif os.path.splitext(file_path)[1] == '.xls' or os.path.splitext(file_path)[1] == '.xlsx': #判断文件是否是Excel文件
            file_list.append(file_path)
    return file_list  #返回Excel文件路径列表



# 首先再使用json.loads()方法，将字符串解析回来
def get_data(file_name):
    with open(file_name,'r') as f: #读取文件
        content = f.read()
        list = content.split('\n') #以换行符分割，每一个字典作为列表中的一项
        dict_list = []
        for item in list:
            dict_list.append(json.loads(item)) #循环恢复字典结构
        print("dic=",dict_list)
        return dict_list

def insert_db(data):
    db = pymysql.connect('localhost','root','mql123','tptcase')
    cusor = db.cursor()
    sql = """INSERT INTO 'othercases' ('caseid','caseName','casePre','caseStep','caseResult','needid','tag','grade','update','creatorname''user_id') VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    try:
        cusor.executemany(sql,data) #sql执行
        db.commit() #提交到数据库
    except Exception as e: #获取报错信息
        print(e)
    db.close()


#操作文件信息    https://blog.csdn.net/weixin_43179111/article/details/82745390
if __name__ == '__main__':
    path = r'/Users/lixiaopeng/Desktop/cases/caseManage/upload'
    file_list = listdir(path)
    f = open('portal.txt','w',encoding='utf-8')
    #print(file_list)
    for file_name in file_list:
        print('start translating',file_name)
        parse(file_name)
        print('translate complete',file_name)
    f.close()


