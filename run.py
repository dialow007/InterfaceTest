import unittest
import os
from BeautifulReport import BeautifulReport
import yaml
import arrow
from shutil import copyfile
from my_util import emailHelper, htmlTemp, getConfig, setHeaders, logHelper
import get_work_dir

logger = logHelper.Logger(__name__).get_logger()
path = get_work_dir.get_base_dir()
# 读取需要用到的配置文件，返回数据对象.根据实际配置
sys_conf_file = os.path.join(path, 'config.yaml')
sys_conf = getConfig.GetConfig(sys_conf_file)


"""通过sys_conf获取具体配置信息"""
# 获取需要用于登录项目的配置文件信息
temp_headers_list = sys_conf.get_conf("TEMP_HEADERS_LIST")
# 获取用于执行的测试用例
test_case_dir = os.path.join(path, 'test_case')  # 测试用例脚本目录
case_list_file = os.path.join(path, 'case_list.yaml')  # 测试用例执行文件目录
# 获取nginx，由于代理html测试报告
index_html = sys_conf.get_conf("NGINX").get('INDEX_HTML')
report_url = sys_conf.get_conf("NGINX").get('REPORT_URL')
# email_conf = getConfig.get_conf('EMAIL')
is_send = sys_conf.get_conf("SEND_EMAIL")

"""html测试报告配置"""
report_dir = os.path.join(path, 'result')  # 测试报告输出目录
report_date = arrow.now().format("YYYYMMDD")
report_name = f'report_{report_date}.html'
report_des = '接口自动化测试'  # 测试报告描述
report_file_path = os.path.join(report_dir, report_name)  # 测试报告文件目录


class DoWork(object):
    # 获取需要执行的测试用例脚本集合，根据实际修改配置文件：case_list.yaml
    @staticmethod
    def get_case_yaml():
        case_item = []
        with open(case_list_file, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        for cases in data.values():
            for case in cases:
                case_item.append(case)
        return case_item

    @staticmethod
    def get_case_suite():
        test_suite = unittest.TestSuite()
        case_item = DoWork.get_case_yaml()
        logger.info(f"执行的测试用例：{case_item}")
        for case_name in case_item:
            discover = unittest.defaultTestLoader.discover(test_case_dir, pattern=case_name + '.py')
            test_suite.addTest(discover)
        return test_suite

    @staticmethod
    def send_email(flag):
        if isinstance(flag, bool):
            if flag:
                copyfile(report_file_path, index_html)
                email_data = DoWork.set_email_info()
                emailHelper.send_email(email_data)

    @staticmethod
    def set_email_info():
        title = "测试报告"
        describe = "接口自动化测试报告"
        done_time = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        data = dict(title=title, describe=describe, done_time=done_time, report_url=report_url)
        html_data = str(htmlTemp.HtmlReport(data))
        email_data = dict(data=html_data, header_name=describe)
        return email_data

    @classmethod
    def run(cls):
        test_suite = cls.get_case_suite()
        BeautifulReport(test_suite).report(description=report_des, filename=report_name, report_dir=report_dir)
        cls.send_email(is_send)


if __name__ == "__main__":
    if setHeaders.is_login(temp_headers_list):
        DoWork.run()
    else:
        logger.error("存在项目登录失败，测试停止")
