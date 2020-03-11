import requests
from my_util import getConfig


class GetCookie(object):
    @staticmethod
    def get_erp_cookie():
        erp_data = getConfig.get_conf('ERP_COOKIE')
        url = erp_data.get('URL') + '/erp/login'
        username = erp_data.get('USER')
        password = erp_data.get('PWD')
        data = f'username={username}&password={password}&userName={username}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        res = requests.post(url=url, headers=headers, data=data)
        c = res.cookies['JSESSIONID']
        cookie_dict = dict(JSESSIONID=c)
        return cookie_dict
