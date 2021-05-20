import xlwt, xlrd, os
from django.db import connection
from datetime import datetime
from caseManage.models import CaseFiles


class updateFile():
    def __init__(self):
        self.dateNow = None
        self.cases = None

    def __call__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs: fileFlag, Flase update DB, True update file
                       filename
        :return:
        """
        self.update(**kwargs)

    def _saveDB(self, filename, filepath, user_id):
        data = dict()
        data['filename'] = filename
        data['filepath'] = filepath
        data['endupdate'] = self.dateNow
        data['user_id'] = user_id
        files = CaseFiles.objects.create(**data)
        files.save()

    def update(self, fileFlag=None, filename=None, user_id=None):
        if fileFlag:
            sql = "select * from studentcases order by tag;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                query = cursor.fetchall()
            casefile = xlwt.Workbook()
            sheet = casefile.add_sheet('测试用例')
            title = ["id","用例名称","前置条件","用例步骤","预期结果","需求ID","标签","等级","最后更新时间","创建者","是否修改"]
            for i in range(len(title)):
                sheet.write(0, i, title[i])
            for row in range(len(query)):
                for col in range(len(query[row])-1):
                    if col == 8:
                        sheet.write(row + 1, col, datetime.strftime(query[row][col], "%Y%m%d %H:%M:%S"))
                    else:
                        sheet.write(row+1, col, query[row][col])
                sheet.write(row+1, col+1, 0)
            sheet.first_visible_col = 1
            self.dateNow = datetime.now()
            dirPath = os.path.join('../upload', datetime.strftime(self.dateNow, "%Y%m%d-%H%M%S"))
            if not os.path.exists(dirPath):
                os.mkdir(dirPath)
            casefile.save(f"{dirPath}/测试用例.xlsx")
            self._saveDB("测试用例.xlsx", f"{dirPath}", user_id)
        else:
            file = xlrd.open_workbook(filename)
            self.cases = file.sheet_by_name(file.sheet_names()[0])