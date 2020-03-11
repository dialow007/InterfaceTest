import requests
import json
from my_util import logHelper

logger = logHelper.Logger(__name__).get_logger()


class Request(object):
    def requests_get(self, url, headers, data):
        headers = {
            "Content-Type": headers
        }
        res = requests.get(url=url, headers=headers, params=json.loads(data))
        return res

    def requests_post(self, url, headers, data, cookies):
        headers = {
            "Content-Type": headers
        }
        res = requests.post(url=url, headers=headers, data=data, cookies=cookies)
        return res

    def request(self, method, url, data, cookies=dict(), headers='application/json' ):
        try:
            if method == 'get':
                result = self.requests_get(url, headers, data)
            elif method == 'post':
                # logger.info(url, headers, data)
                result = self.requests_post(url, headers, data.encode(), cookies)
            else:
                logger.error(f"请求的method不正确：{method=}")
            logger.info(result.text)
        except BaseException as e:
            logger.error(f"发生错误{e}")
        finally:
            return result


if __name__ == "__main__":
    pass
