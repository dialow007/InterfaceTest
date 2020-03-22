HTML_TEMP = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>%(title)s</title>
</head>
<body >
<div style="margin:0px auto;text-align:center">
  <h1>%(describe)s</h1>
  <p>各位同事，大家好，测试项目已在<strong>%(done_time)s</strong>完成测试，测试报告详见：</p>
    <button style="background-color: #7ED321 ; width:150px;height:40px">
        <a href="%(report_url)s"  target="view_window">查看测试报告</a>
    </button>
    <hr>
    <p>本邮件由系统自动发出，无需回复！</p>
</div>
</body>
</html>
    """


class HtmlReport(object):
    def __init__(self, html_data):
        self.title = html_data.get('title')
        self.describe = html_data.get('describe')
        self.done_time = html_data.get('done_time')
        self.report_url = html_data.get('report_url')

    def __str__(self):
        email_data = HTML_TEMP % dict(title=self.title,
                                     describe=self.describe,
                                     done_time=self.done_time,
                                     report_url=self.report_url)
        return email_data
