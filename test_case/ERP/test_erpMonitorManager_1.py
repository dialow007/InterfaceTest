import unittest
from my_util import getConfig, excelHelper, logHelper, requestHelper, getCookies
import ddt
import json
import sys

case_data = excelHelper.ExcelHelper.get_excel_list('erp_project_case.xlsx','MonitorManager')
base_url_dict = getConfig.get_conf('HTTP')
base_url = f"{base_url_dict.get('BASE_URL')}:{base_url_dict.get('PORT')}"
logger = logHelper.Logger(__name__).get_logger()
cookies = getCookies.GetCookie.get_erp_cookie()


@ddt.ddt
class TestERP(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info(f"{__name__}开始测试")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(f"{__name__}测试结束")

    @ddt.data(*case_data)
    def test_erp_monitor_manager(self, data):
        self._testMethodDoc = data[1]
        self._testMethodName = sys._getframe().f_code.co_name
        self.case_name = data[1]
        self.url = base_url+data[2]
        self.method = data[3]
        self.headers = data[4]
        self.query_data = data[5]
        self.res_code = data[6]
        self.res_msg = data[7]
        self.res_keyword = data[8]
        res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers, data=self.query_data, cookies=cookies)
        res_json = json.loads(res.text)
        self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')
        if self.res_keyword:
            self.assertRegex(str(res_json['data']), self.res_keyword, f'未找到关键字: {self.res_keyword}')

    def test_zapi(self):
        self._testMethodDoc = "测试"
        self.assertEqual(2,3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
