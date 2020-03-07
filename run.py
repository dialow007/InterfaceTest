import unittest
import getWorkDir
import os
from BeautifulReport import BeautifulReport
import yaml

path = getWorkDir.get_base_dir()
test_case_dir = os.path.join(path, 'test_case')
case_list_file = os.path.join(path, 'case_list.yaml')
###测试报告
report_dir = os.path.join(path, 'result')
report_name = 'report.html'
report_des = '测试用例描述'


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

    def run(self):
        test_suite = DoWork.get_case_suite()
        BeautifulReport(test_suite).report(description=report_des, filename=report_name, report_dir=report_dir)


if __name__ == "__main__":
    DoWork().run()
