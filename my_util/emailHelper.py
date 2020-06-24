import smtplib, arrow
from email.mime.text import MIMEText
from email.header import Header
from my_util import getConfig, logHelper,htmlTemp

# email_conf = getConfig.get_conf('EMAIL')
logger = logHelper.Logger(__name__).get_logger()

email_conf = {
      'SMTP_SERVER': 'smtp.qq.com',
      'SENDER': '314785857@qq.com',
      'PASSWORD': 'fclxoizwosnpbiea',
      'RECEIVER': ['dialow@aliyun.com','lhb@hangzhouyq.com']
}

def send_mail(email_data):
    data = email_data.get('data')
    header_name = email_data.get('header_name')
    email_conf = email_data.get('email_conf')
    smtpserver = email_conf.get('SMTP_SERVER')
    sender = email_conf.get('SENDER')
    password = email_conf.get('PASSWORD')
    receiver = email_conf.get('RECEIVER')
    text = MIMEText(data, 'html', 'utf-8')
    text['Subject'] = Header(s=header_name, charset='utf-8')
    text['From'] = sender
    text['To'] = ';'.join(receiver)
    smtp = smtplib.SMTP()
    try:
        smtp.connect(smtpserver)
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, text.as_string())
    except BaseException as e:
        logger.error(e)
    finally:
        smtp.quit()


if __name__=="__main__":
    pass
