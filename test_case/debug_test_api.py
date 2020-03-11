import unittest
import requests,json


class MyTestCase(unittest.TestCase):
    def test_something(self):
        data = {
            "user":"admin",
            "pwd":"123456"
        }
        res = requests.post(url='http://127.0.0.1:5000/login', data=json.dumps(data))
        data = res.json()
        re = '管理1员'
        if re: self.assertRegex(str(data),re)


def request():
    url = 'http://www.zhonshian.com/erp/login'
    url2 = 'http://www.zhonshian.com/erp/erpMonitorManager/list'
    url3 = 'http://www.zhonshian.com/zsagov/educationStat/getCourseManage'
    data = 'username=test01&password=000000&userName=test01'
    data2 = 'pageNum=1&pageSize=10&sysOrganizationName=&sysOrganizationId=&superviseName='
    data3 = 'page=1&pageSize=10&courseName=&regionId=1&courseType=&startDate=&endDate=&superviseOrganizationId=1&_datetime=1583725108270&_userorganizationid=7458090&_sysuserid=587&_token=1f9ecd1b5c191ea81edda906d88cb2d6&logOrganizationId=5001&logUserId=5587&node=1'
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    # res = requests.post(url=url, headers=headers, data=data)
    # r = res.cookies['JSESSIONID']
    # cookie_dict = dict(JSESSIONID=r)
    # res2 = requests.post(url=url2, headers=headers, data=data2, cookies=cookie_dict)
    c = {"JSESSIONID":"312313"}
    res3 = requests.post(url=url3, headers=headers, data=data3,cookies=dict(c))
    print(res3.json())

if __name__ == '__main__':
    # unittest.main()
    request()
