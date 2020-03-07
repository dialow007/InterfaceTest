import unittest
from my_util import getConfig, excelHelper, logHelper, requestHelperr
import ddt
import json
from my_util import logHelper
import sys

case_data = excelHelper.ExcelHelper.get_excel_list('cese.xlsx','login')
base_url_dict = getConfig.get_conf('HTTP')
base_url = f"{base_url_dict.get('BASE_URL')}:{base_url_dict.get('PORT')}"
logger = logHelper.Logger(__name__).get_logger()

@ddt.ddt
class TestLogIn(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info(f"{__name__}开始测试")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(f"{__name__}测试结束")

    @ddt.data(*case_data)
    def test_login(self, data):
        self._testMethodDoc = data[1]
        self._testMethodName = sys._getframe().f_code.co_name
        self.case_name = data[1]
        self.url = base_url + data[2]
        self.method = data[3]
        self.query_data = data[4]
        self.res_code = data[5]
        self.res_msg = data[6]
        res = requestHelperr.Request().request(method=self.method, url=self.url, data=self.query_data)
        res_json = json.loads(res.text)
        self.assertEqual(res_json['code'], self.res_code, '返回code错误')
        self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')


if __name__ == '__main__':
    unittest.main(verbosity=2)
