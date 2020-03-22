import unittest
import getWorkDir
import os
from BeautifulReport import BeautifulReport
import yaml
import arrow
from my_util import emailHelper, htmlTemp, getConfig
from shutil import copyfile

"""获取配置信息"""
path = getWorkDir.get_base_dir()
test_case_dir = os.path.join(path, 'test_case')
case_list_file = os.path.join(path, 'case_list.yaml')
index_html = getConfig.get_conf('NGINX').get('INDEX_HTML')
report_url = getConfig.get_conf('NGINX').get('SERVER')
email_conf = getConfig.get_conf('EMAIL')
"""测试报告配置"""
report_dir = os.path.join(path, 'result')
report_date = arrow.now().format("YYYYMMDD")
report_name = f'report_{report_date}.html'
report_des = '测试任务描述'
report_file_path = os.path.join(report_dir,report_name)


class DoWork(object):
    @staticmethod
    def get_case_yaml():
        case_item = []
        with open(case_list_file, 'r') as file:
            data = yaml.safe_load(file)
        for cases in data.values():
            for case in cases:
                case_item.append(case)
        return case_item

    @staticmethod
    def get_case_suite():
        test_suite = unittest.TestSuite()
        case_item = DoWork.get_case_yaml()
        for case_name in case_item:
            discover = unittest.defaultTestLoader.discover(test_case_dir, pattern=case_name + '.py')
            test_suite.addTest(discover)
        return test_suite

    @staticmethod
    def copy_html_report():
        copyfile(report_file_path, index_html)

    @staticmethod
    def get_html_report_info():
        title = "测试报告"
        describe = "接口自动化测试报告"
        done_time = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        data = dict(title=title, describe=describe, done_time=done_time, report_url=report_url)
        return data

    @staticmethod
    def get_send_email_info():
        html_data = DoWork.get_html_report_info()
        data = str(htmlTemp.HtmlReport(html_data))
        header_name = "接口自动化测试报告"
        email_data = dict(data=data,header_name=header_name,email_conf=email_conf)
        return email_data

    @classmethod
    def run(cls):
        test_suite = cls.get_case_suite()
        BeautifulReport(test_suite).report(description=report_des, filename=report_name, report_dir=report_dir)
        cls.copy_html_report()
        email_data = cls.get_send_email_info()
        emailHelper.send_mail(email_data)


if __name__ == "__main__":
    DoWork.run()
