import unittest
from my_util import getConfig, excelHelper, logHelper, requestHelper, setHeaders
import ddt
import json
import sys
import os
import get_work_dir

# 日志实例，用于写日志
logger = logHelper.Logger(__name__).get_logger()
path = get_work_dir.get_base_dir()
# case_data，用于读取excel表格中的测试数据，两个参数：表格的相对路径和sheet名称，根据实际配置
case_data = excelHelper.ExcelHelper.get_excel_list('zsa_cloud\Zzd_APP_case.xlsx', '农村家宴')
# 读取配置文件，获取测试地址和端口，根据实际项目配置
config_life = os.path.join(path,'test_case_config', 'Zzd_APP.yaml')
conf = getConfig.GetConfig(config_life)
base_url = conf.get_conf("HTTP").get('SERVER')
KEY = conf.get_conf("HTTP").get('KEY')
# 微服务请求头增加了token和userId，用于获取这两个参数。需要指定测试项目的配置文件中的“KEY”，以读取指定请求头文件。不传参数则返回默认请求头。
tmp_headers = setHeaders.get_headers_info(KEY)
# 测试用例涉及到关联接口，用户获取配置文件下的接口和参数等数据，根据实际配置
path_dict = conf.get_conf("VillageParty")
# 定义全局变量，根据实际配置
method = "post"
guideId = ""  # 现场指导记录id



@ddt.ddt
class TestZzdVillageParty(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info(f"{__name__}开始测试")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(f"{__name__}测试结束")

    # 数据驱动测试方法，参考测试用例excel模板
    @ddt.data(*case_data)
    def test_zzd_village_party_1_main(self, data):
        self._testMethodDoc = f"{data[1]}\n{data[2]}"  # 测试用例名称及接口地址
        self._testMethodName = sys._getframe().f_code.co_name
        self.case_name = data[1]
        self.url = base_url + data[2]  # 测试接口地址
        self.method = data[3]  # 请求方法
        tmp_headers["Content-Type"] = data[4]
        self.headers = tmp_headers  # 请求头
        self.query_data = data[5]  # 请求参数
        self.res_code = data[6]  # 断言返回code
        self.res_msg = data[7]  # 断言返回msg
        self.key_word = data[8]  # 断言返回关键字
        # 发送http请求
        res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                              data=self.query_data)
        res_json = json.loads(res.text)  # 接口返回值，转换为json格式
        # 判断接口返回的code是否正确
        self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        # 判断接口返回的msg是否正确
        self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')
        # 判断是否设置关键字
        if self.key_word:
            # 判断是否要做列表数据数量
            if self.key_word == "test_not_empty":
                # 判断接口返回的列表长度是否大于0
                self.assertGreater(len(res_json['data']['list']), 0, '返回数据数量错误')
            else:
                # 判断接口返回的关键字是否匹配到
                self.assertRegex(str(res_json['data']), self.key_word, '关键字匹配错误')

# 涉及到接口联动，需要单独写测试用例脚本，如删除数据，需要动态获取指定数据的id
    def test_zzd_village_party_2_delete_chef(self):
        self._testMethodDoc = f"删除指定厨师\n{path_dict['deleteChef']}"  # 测试用例名称及接口地址
        self._testMethodName = sys._getframe().f_code.co_name
        self.key = 'Chef'
        self.chef_id = TestZzdVillageParty.get_object_id(self.key)  # 调用返回指定id的方法，根基实际封装方法
        self.method = "post"
        self.url = base_url + path_dict['deleteChef']  # 通过配置文件，获取该接口的接口地址
        self.headers = tmp_headers  # 使用默认请求头
        self.query_data = path_dict['delete_Chef_Family_data'] % self.chef_id  # 动态配置请求参数，根据实际接口填写
        self.res_code = "10000"  # 断言返回code
        self.res_msg = "操作成功"  # 断言返回msg
        if len(self.chef_id) > 0:  # 判断是否获取到了需要的id参数，获取在执行该用例，否则用例执行失败
            res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                                  data=self.query_data)
            res_json = json.loads(res.text)
            self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
            # self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')
        else:
            self.assertEqual(1, 2, '没有查询到指定厨师id，删除失败')

    def test_zzd_village_party_3_delete_family(self):
        self._testMethodDoc = f"删除指定家宴中心\n{path_dict['deleteFamily']}"
        self._testMethodName = sys._getframe().f_code.co_name
        self.key = 'Family'
        self.family_id = TestZzdVillageParty.get_object_id(self.key)
        self.method = "post"
        self.url = base_url + path_dict['deleteFamily']
        self.headers = tmp_headers
        self.query_data = path_dict['delete_Chef_Family_data'] % self.family_id
        self.res_code = "10000"
        self.res_msg = "操作成功"
        if len(self.family_id) > 0:
            res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                                  data=self.query_data)
            res_json = json.loads(res.text)
            self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        else:
            self.assertEqual(1, 2, '没有查询到指定家宴中心id，删除失败')
            # self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')

# 提交现场指导信息，会返回一个guideId，后面的获取模板、提交指导表和处理结果均会用到这个id
    def test_zzd_village_party_4_save_guide(self):
        global guideId
        self._testMethodDoc = f"新增现场指导-指导信息\n{path_dict['save_guide']}"
        self._testMethodName = sys._getframe().f_code.co_name
        self.method = "post"
        self.url = base_url + path_dict['save_guide']
        self.headers = tmp_headers
        self.query_data = path_dict['save_guide_data']
        self.res_code = "10000"
        self.res_msg = "操作成功"
        res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                              data=self.query_data)
        res_json = json.loads(res.text)
        self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')
        guideId = str(res_json['data']['id'])

    def test_zzd_village_party_5_educate_module(self):
        global guideId
        self._testMethodDoc = f"新增现场指导-获取现场指导表\n{path_dict['educate_module']}"
        self._testMethodName = sys._getframe().f_code.co_name
        self.method = "post"
        self.url = base_url + path_dict['educate_module']
        self.headers = tmp_headers
        self.query_data = path_dict['educate_module_data'] % guideId
        self.res_code = "10000"
        self.res_msg = "操作成功"
        res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                              data=self.query_data)
        res_json = json.loads(res.text)
        self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')

    def test_zzd_village_party_6_save_answer(self):
        global guideId
        self._testMethodDoc = f"新增现场指导-现场指导表\n{path_dict['save_answer']}"
        self._testMethodName = sys._getframe().f_code.co_name
        self.method = "post"
        self.url = base_url + path_dict['save_answer']
        self.headers = tmp_headers
        self.query_data = path_dict['save_answer_data'] % guideId
        self.res_code = "10000"
        self.res_msg = "操作成功"
        res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                              data=self.query_data)
        res_json = json.loads(res.text)
        self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')

    def test_zzd_village_party_7_submit_guide(self):
        global guideId
        self._testMethodDoc = f"新增现场指导-结果处理\n{path_dict['submit_guide']}"
        self._testMethodName = sys._getframe().f_code.co_name
        self.method = "post"
        self.url = base_url + path_dict['submit_guide']
        self.headers = tmp_headers
        self.query_data = path_dict['submit_guide_data'] % guideId
        self.res_code = "10000"
        self.res_msg = "操作成功"
        res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                              data=self.query_data)
        res_json = json.loads(res.text)
        self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')

    def test_zzd_village_party_8_record_delete(self):
        self._testMethodDoc = f"删除未指导备案\n{path_dict['party_record_delete']}"
        self._testMethodName = sys._getframe().f_code.co_name
        self.method = "post"
        self.url = base_url + path_dict['party_record_delete']
        self.headers = tmp_headers
        self.recordId = TestZzdVillageParty.get_record_id()
        self.query_data = path_dict['party_record_delete_data'] % self.recordId
        self.res_code = "10000"
        self.res_msg = "操作成功"
        res = requestHelper.Request().request(method=self.method, url=self.url, headers=self.headers,
                                              data=self.query_data)
        res_json = json.loads(res.text)
        self.assertEqual(str(res_json['code']), self.res_code, '返回code错误')
        self.assertEqual(res_json['msg'], self.res_msg, '返回msg错误')


# 封装用于动态获取id信息方法，根据实际测试需求编写方法，不同的接口方法可能不一样
    @staticmethod
    def get_object_id(key):  # 以此方法为例，通过key这个参数判断是查询厨师还是家宴中心的id
        obj_id = ""
        if key == "Chef":  # 如果是厨师，执行查询指定厨师的接口
            url = base_url + path_dict['partyChef']
            query_data = path_dict['query_chef']
        else:  # 否则就执行查询家宴中心的id
            url = base_url + path_dict['partyFamily']
            query_data = path_dict['query_family']
        res = requestHelper.Request().request(method=method, url=url, headers=tmp_headers,
                                              data=query_data)
        res_json = json.loads(res.text)
        obj_list = res_json['data']['list']
        if len(obj_list) == 1:
            obj_id = str(obj_list[0]['id']) # 根据json格式，获取需要的id信息
        else:
            logger.error(f"{key}没有查询到id或者存在多个id，请检查数据！")
        return obj_id

# zzd不支持关键字查询备案，按照先查询未指导的备案，再遍历列表，根据applicantName（村社区）的关键字匹配,返回该备案的id
# 注意：不参与统计的测试用例方法名称不要以test开头
    @staticmethod
    def get_record_id():
        obj_id = ""
        url = base_url + path_dict['party_record_all']
        query_data = path_dict['party_record_all_data']
        res = requestHelper.Request().request(method=method, url=url, headers=tmp_headers,
                                              data=query_data)
        res_json = json.loads(res.text)
        obj_list = res_json['data']['list']
        for obj in obj_list:
            if obj['applicantName'] == "浙政钉删除备案":
                obj_id = str(obj['id'])
                break
        return obj_id


if __name__ == '__main__':
    unittest.main(verbosity=2)
