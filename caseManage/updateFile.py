import xlwt, xlrd, os
from django.db import connection
from datetime import datetime


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
        if fileFlag:
            sql = "select * studentcases from order by tag;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                query = cursor.fetchall()
            casefile = xlwt.Workbook()
            sheet = casefile.add_sheet('测试用例')
            for case in query:
                sheet.write(case[:-1])
            dirPath = os.path.join('../upload', datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
            if not os.path.exists(dirPath):
                os.mkdir(dirPath)
            casefile.save(f"{dirPath}/测试用例.xlsx")
        else:
            file = xlrd.open_workbook(filename)
            self.cases = file.sheet_by_name(file.sheet_names()[0])