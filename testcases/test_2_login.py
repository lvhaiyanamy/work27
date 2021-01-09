"""
============================
Author:蓝色水汀
Time:2020/12/11  10:15
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import unittest
import os
import openpyxl
import requests
from unittestreport import ddt, list_data
from openpyxl import styles
from common.log_option import log
from common.excel_option import ReadExcel
from common.path_option import Data_Path
from common.conf_option import conf
from common.assert_option import assert_dict_in


@ddt
class TestLogin(unittest.TestCase):
    # 创建一个读取Excel的对象
    excel = ReadExcel(os.path.join(Data_Path, 'cases.xlsx'), 'login')
    # 利用创建的对象调用读取Excel方法
    cases = excel.read_excel()
    # 从配置文件读取项目的基本地址
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('env', 'headers'))

    @list_data(cases)
    def test_login(self, item):
        # 接口请求地址
        url_login = self.base_url + item['url']
        # 接口请求参数
        params = eval(item['data'])
        # 请求方法,并转换为小写
        method = item['method'].lower()
        # 从配置文件获取请求头
        # 获取期望值
        expected_login = eval(item['expected'])
        # 请求接口，返回实际结果
        response_login = requests.request(method=method, url=url_login, headers=self.headers, json=params)
        actual_login = response_login.json()
        # 获取用例的行号
        # row = item['case_id'] + 1
        # 捕获异常
        try:
            assert_dict_in(expected_login, actual_login)
        except AssertionError as e:
            # 往Excel中写入执行结果
            # self.excel.write_excel(row=row, column=6, value='失败', font=openpyxl.styles.Font(color='FF0000'))
            # 往日志文件中写入执行结果
            log.error('这是【{}】用例执行失败'.format(item['title']))
            log.exception(e)
            raise e
        else:
            # self.excel.write_excel(row=row, column=6, value='通过', font=openpyxl.styles.Font(color='339966'))
            log.info('这是【{}】用例执行通过'.format(item['title']))
