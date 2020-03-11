import unittest
from my_util import getConfig, excelHelper, logHelper, requestHelper
import ddt
import json
from my_util import logHelper
import sys

case_data = excelHelper.ExcelHelper.get_excel_list('cese.xlsx','examTask')
base_url_dict = getConfig.get_conf('HTTP')
base_url = f"{base_url_dict.get('BASE_URL')}:{base_url_dict.get('PORT')}"
logger = logHelper.Logger(__name__).get_logger()


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info(f"{__name__}开始测试")
        cls.url = f"{base_url}/zsagov/educationStat/getTestedList"
        cls.method = 'post'
        cls.headers = 'application/x-www-form-urlencoded'

    def test_getCourseManage_byName(self):
        self._testMethodDoc = "按照报考姓名查询"
        self._testMethodName = sys._getframe().f_code.co_name
        data = 'applyName=章建琴&regionId=1&operatScales=&enterpriseTypes=&page=1&pageSize=10&orgName=&icard=&certNumber=&isGetCert=&isPrint=&superviseName=&startDate=&endDate=&_datetime=1583646472499&_userorganizationid=7458090&_sysuserid=587&_token=9865c6b10dfc4add6cc8c1fdc554001c&logOrganizationId=5001&logUserId=5587&node=1'
        res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers, data=data)
        res_json = json.loads(res.text)
        self.assertEqual(str(res_json['code']), '10000', '返回code错误')
        self.assertEqual(res_json['msg'], '操作成功', '返回msg错误')
        self.assertEqual(res_json['data']['rows'][0]['applyName'], '章建琴')


    @unittest.skip("功能取消")
    def test_getCourseManage_byGetCert(self):
        self._testMethodDoc = "是否领取证书"

    def test_getCourseManage_byoperatScales(self):
        self._testMethodDoc = ""

    def test_getCourseManage_byEnterpriseTypes(self):
        pass
    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(f"{__name__}测试结束")




if __name__ == '__main__':
    unittest.main(verbosity=2)
