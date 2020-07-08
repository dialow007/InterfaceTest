import requests
import json
from my_util import logHelper


logger = logHelper.Logger(__name__).get_logger()


class Request(object):
    def requests_get(self, url, headers, data):
        res = requests.get(url=url, headers=headers, params=json.loads(data))
        return res

    def requests_post(self, url, headers, data, cookies):
        res = requests.post(url=url, headers=headers, data=data, cookies=cookies)
        return res

    def request(self, method, url, data, headers, cookies=dict()):
        try:
            if method == 'get':
                result = self.requests_get(url, headers, data)
            elif method == 'post':
                result = self.requests_post(url, headers, data.encode(), cookies)
            else:
                logger.error(f"请求的method不正确：{method}")
            logger.info(f"请求url:{url}\n请求参数：{data}\n返回结果：{result.text}")
        except BaseException as e:
            logger.error(f"发生错误{e}")
        finally:
            return result


if __name__ == "__main__":
    pass
