import os
import getWorkDir
from my_util import getConfig, logHelper
import requests
import json

path = getWorkDir.get_base_dir()
logger = logHelper.Logger(__name__).get_logger()
conf_file = os.path.join(path, 'config.yaml')
base_data = getConfig.get_conf("HTTP")
form_data = getConfig.get_conf("province_PC")
url = base_data.get("BASE_URL") + form_data.get("path")
loginName = form_data.get("user")
password = form_data.get("passwd")
data = f"loginName={loginName}&password={password}"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
tmp_josn = os.path.join(path, 'temp_headers.json')


def set_tmp_headers():
    try:
        res = requests.post(url=url, data=data, headers=headers)
        res_json = res.json()
        userId = str(res_json['data']['user']['id'])
        token = str(res_json['data']['user']['token'])
        orgId = str(res_json['data']['organizations'][0]['id'])
        get_headers = dict(userId=userId, token=token, orgId=orgId)
        temp_headers(get_headers)
        return True
    except BaseException as e:
        logger.error(e)
        return False


def temp_headers(msg):
    if os.path.exists(tmp_josn):
        os.remove(tmp_josn)
    with open(tmp_josn, 'w', encoding='utf-8') as file:
        json.dump(msg, file)


def get_headers_info():
    if os.path.exists(tmp_josn):
        with open(tmp_josn, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            tmp_headers = dict(userId=json_data['userId'],
                               token=json_data['token'])
        tmp_headers["Content-Type"] = "application/x-www-form-urlencoded"
        return tmp_headers
