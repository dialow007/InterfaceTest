import os
import xlrd
import getWorkDir

path = getWorkDir.get_base_dir()


class ExcelHelper(object):
    @staticmethod
    def get_excel_dict(filename, sheet_name):
        file = os.path.join(path, "test_data", filename)
        file = xlrd.open_workbook(file)
        sheet = file.sheet_by_name(sheet_name)
        nrows = sheet.nrows  # 行数
        colnames = sheet.row_values(0)  # 某一行数据
        cls = []
        for colnameindex in range(1, nrows):
            row = sheet.row_values(colnameindex)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = str(row[i])
                cls.append(app)
        return cls

    @staticmethod
    def get_excel_list(filename, sheet_name):
        """
        @param filename: 测试用例表格文件名
        @param sheet_name:
        @return:
        """
        cls = []
        skip_col = 9 #是否执行的列号
        file = os.path.join(path, "test_data",  filename)
        data = xlrd.open_workbook(file)
        sheet = data.sheet_by_name(sheet_name)
        nrows = sheet.nrows
        for i in range(1, nrows):
            if sheet.row_values(i)[skip_col] == 'Y' or sheet.row_values(i)[skip_col] == '':
                cls.append(sheet.row_values(i, end_colx=skip_col))
        return cls


if __name__=="__main__":
    res = ExcelHelper.get_excel_list('erp_project_case.xlsx', 'login')
    print(res)