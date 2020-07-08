import requests
import os
import json
import get_work_dir
from my_util import getConfig, logHelper

path = get_work_dir.get_base_dir()
logger = logHelper.Logger(__name__).get_logger()


def set_tmp_headers(sys_conf):
    url = sys_conf.get('SERVER') + sys_conf.get('login_path')
    data = sys_conf.get("login_data")
    project = sys_conf.get("KEY")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # 根据参数，设置指定的请求头文件名称用于针对不同用户
    tmp_josn = os.path.join(path, f'temp_headers_{project}.json')
    try:
        res = requests.post(url=url, data=data, headers=headers)
        res_json = res.json()
        userId = str(res_json['data']['user']['id'])  # 获取userId
        token = str(res_json['data']['user']['token'])  # 获取token
        orgId = str(res_json['data']['organizations'][0]['id'])
        get_headers = dict(userId=userId, token=token, orgId=orgId)
        temp_headers(get_headers, tmp_josn)  # 写入到配置文件
        return True
    except BaseException as e:
        logger.error(e)
        return False


# 定义把请求头信息写入到json文件
def temp_headers(msg, tmp_josn):
    if os.path.exists(tmp_josn):
        os.remove(tmp_josn)
    with open(tmp_josn, 'w', encoding='utf-8') as file:
        json.dump(msg, file)


# 根据项目名称读取指定请求头文件
def get_headers_info(project=None):
    tmp_headers = dict()
    tmp_headers["Content-Type"] = "application/x-www-form-urlencoded"
    if project:
        tmp_josn = os.path.join(path, f'temp_headers_{project}.json')
        if os.path.exists(tmp_josn):
            with open(tmp_josn, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                tmp_headers = dict(userId=json_data['userId'],
                                   token=json_data['token'])
    return tmp_headers


def is_login(conf):
    flag = True
    if conf:
        for tmp_name in conf:
            conf_path = os.path.join(path, 'test_case_config', tmp_name)
            conf = getConfig.GetConfig(conf_path).get_conf("HTTP")
            if not set_tmp_headers(conf):
                flag = False
                logger.error(f"登录失败: {conf}")
                break
    return flag