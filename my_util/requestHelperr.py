import requests
import json
from my_util import logHelper
logger = logHelper.Logger(__name__).get_logger()

class Request(object):
    def requests_get(self, url, data):
        res = requests.get(url=url, params=json.loads(data))
        return res

    def requests_post(self, url, data):
        # data = json.dumps(data)
        res = requests.post(url=url, data=data)
        return res

    def request(self, method, url, data):
        try:
            if method == 'get':
                result = self.requests_get(url, data)
            elif method == 'post':
                result = self.requests_post(url, data)
            else:
                logger.error(f"请求的method不正确：{method=}")
            # print(result.text)
            logger.info(result.json())
        except BaseException as e:
            logger.error(f"发生错误{e}")
        finally:
            return result


if __name__ == "__main__":
    data = {"uid": "123"}
    r = Request().requests_get('http://127.0.0.1:5000/user/query', data)
