import unittest
from my_util import getConfig, excelHelper, logHelper, requestHelper, setHeaders, skip_case
import ddt
import json
import sys

case_data = excelHelper.ExcelHelper.get_excel_list('zsa_cloud\province_PC_case.xlsx', '农村家宴')
base_url_dict = getConfig.get_conf('HTTP')
base_url = f"{base_url_dict.get('BASE_URL')}:{base_url_dict.get('PORT')}"
logger = logHelper.Logger(__name__).get_logger()
tmp_headers = setHeaders.get_headers_info()
path_dict = getConfig.get_conf('province_PC').get("test_path")


@ddt.ddt
class TestVillageParty(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info(f"{__name__}开始测试")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(f"{__name__}测试结束")

    @ddt.data(*case_data)
    def test_pc_village_party_1_main(self, data):
        self._testMethodDoc = data[1]
        self._testMethodName = sys._getframe().f_code.co_name
        self.case_name = data[1]
        self.url = base_url + data[2]
        self.method = data[3]
        tmp_headers["Content-Type"] = data[4]
        self.headers = tmp_headers
        self.query_data = data[5]
        self.res_code = data[6]
        self.res_msg = data[7]
        logger.debug(self.headers)
        res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                              data=self.query_data)
        res_json = json.loads(res.text)
        self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        # self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')

    def test_pc_village_party_2_delete_chef(self):
        self._testMethodDoc = "删除指定厨师"
        self._testMethodName = sys._getframe().f_code.co_name
        self.key = 'Chef'
        self.chef_id = TestVillageParty.get_object_id(self.key)
        self.method = "post"
        self.url = base_url + path_dict['deleteChef']
        self.headers = tmp_headers
        self.query_data = f"id={self.chef_id}&updateUser=774750"
        self.res_code = "10000"
        self.res_msg = "操作成功"
        if self.chef_id != "":
            res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                                  data=self.query_data)
            res_json = json.loads(res.text)
            self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
            # self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')
        else:
            self.assertEqual(1, 2, '没有查询到指定厨师id，删除失败')

    def test_pc_village_party_3_delete_family(self):
        self._testMethodDoc = "删除指定家宴中心"
        self._testMethodName = sys._getframe().f_code.co_name
        self.key = 'Family'
        self.family_id = TestVillageParty.get_object_id(self.key)
        self.method = "post"
        self.url = base_url + path_dict['deleteFamily']
        self.headers = tmp_headers
        self.query_data = f"id={self.family_id}&updateUser=774750"
        self.res_code = "10000"
        self.res_msg = "操作成功"
        if self.family_id != "":
            res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                                  data=self.query_data)
            res_json = json.loads(res.text)
            self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        else:
            self.assertEqual(1, 2, '没有查询到指定家宴中心id，删除失败')
            # self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')

    @staticmethod
    def get_object_id(key):
        obj_id = ""
        if key == "Chef":
            url = base_url + path_dict['partyChef']
            query_data = path_dict['query_chef']
        else:
            url = base_url + path_dict['partyFamily']
            query_data = path_dict['query_family']
        method = "post"
        headers = tmp_headers
        res = requestHelper.Request().request(method=method, url=url, headers=headers,
                                              data=query_data)
        res_json = json.loads(res.text)
        obg_list = res_json['data']['list']
        if len(obg_list) == 1:
            obj_id = str(obg_list[0]['id'])
        else:
            logger.error(f"{key}没有查询到id或者存在多个id，请检查数据！")
        return obj_id


if __name__ == '__main__':
    unittest.main(verbosity=2)
