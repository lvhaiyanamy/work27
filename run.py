"""
============================
Author:蓝色水汀
Time:2020/12/11  13:11
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
from unittestreport import TestRunner
import unittest
from common.path_option import Cases_Path, Report_Path


# 创建测试套件
suite = unittest.defaultTestLoader.discover(Cases_Path)
# 设置报告名称、存放地址、报告的模版
runner = TestRunner(suite,
                    filename='report.html',
                    report_dir=Report_Path,
                    templates=1)
# 调用run方法执行用例
runner.run()

# -------------------------发送测试报到至邮箱，没有邮件名称和内容-------------------------
# runner.send_email(host='smtp.qq.com',
#                   # port=465,
#                   # user='826926575@qq.com',
#                   # password='nlbcuzloxezqbchj',
#                   # to_addrs='826926575@qq.com',
#                   # is_file=True)

# -------------------------发送测试报到至邮箱，有邮件名称和内容-------------------------
from unittestreport.core.sendEmail import SendEmail
em = SendEmail(
    host='smtp.qq.com',
    port=465,
    user='826926575@qq.com',
    password='nlbcuzloxezqbchj')
# filename为报告文件的完整路径
em.send_email(subject="前程贷项目接口测试报告",
              content="各位领导好，第一阶段接口自动化已测试完成，请查收结果！",
              filename=r"C:\Users\Administrator\Desktop\work27\reports\report.html",
              to_addrs='826926575@qq.com'
              )

# -------------------------发送测试报到至钉钉群-------------------------
# 钉钉机器人的Webhook地址
webhook="https://oapi.dingtalk.com/robot/send?access_token=697292f60b029261de2379561f4010da91d3c1f46b5532bea7efa602d5cf93a4"
# 如果钉钉机器人安全设置了关键字，则需要传入对应的关键字
runner.dingtalk_notice(url=webhook,
                       key='测试',
                       isatall=True)

# -------------------------发送测试报到企业微信群-------------------------
"""
包含以下参数：
chatid： 企业微信群id
access_token：调用企业微信API接口的凭证
corpid：企业ID
corpsecret：应用的凭证密钥
"""
# 方式一：
# runner.weixin_notice(chatid="企业微信群id", access_token="调用企业微信API接口的凭证")
# 方式二：
# runner.weixin_notice(chatid="企业微信群id",corpid='企业ID', corpsecret='应用的凭证密钥')
