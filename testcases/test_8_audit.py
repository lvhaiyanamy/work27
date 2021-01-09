"""
============================
Author:蓝色水汀
Time:2020/12/26  14:23
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.excel_option import ReadExcel
from common.path_option import Data_Path
from common.conf_option import conf
from common.log_option import log
from common.mysql_option import OptionDB
from testcases.fixture import BaseTest
from common.replace_option import data_replace

"""
审核接口：管理员去审核
审核的前置条件：
1、管理员登录（类级别的前置）
2、普通用户添加项目
  1）普通用户登录（类级别的前置）
  2）创建一个项目（用例级别前置）
"""


@ddt
class TestAudit(unittest.TestCase,BaseTest):
    excel = ReadExcel(os.path.join(Data_Path, 'cases.xlsx'), 'audit')
    cases = excel.read_excel()
    base_url = conf.get('env', 'base_url')
    db = OptionDB()

    @classmethod
    def setUpClass(cls):
        # 创建测试类对象，赋值为从已封装的登录接口提取的普通用户headers_normal和member_id
        # 封装的登录接口提取的管理员headers_admin和member_id_admin
        cls.user_login()
        cls.admin_login()

    def setUp(self):
        self.add_project()

    @list_data(cases)
    def test_audit(self, item):
        url_audit = self.base_url + item['url']
        method = item['method']
        expected = eval(item['expected'])
        item['data'] = data_replace(item['data'], TestAudit)
        params = eval(item['data'])
        response_audit = requests.request(method=method, url=url_audit, json=params, headers=self.headers_admin)
        res_audit = response_audit.json()
        print(res_audit)
        if res_audit['msg'] == 'OK' and item['title'] == "审核通过":
            TestAudit.pass_loan_id = params['loan_id']
            # setattr(TestAudit,'pass_loan_id',params['loan_id'])
        try:
            self.assertEqual(expected['code'], res_audit['code'])
            self.assertEqual(expected['msg'], res_audit['msg'])
            if item['flag']:
                sql = 'SELECT status FROM  futureloan.loan WHERE id={}'.format(self.loan_id)
                status = self.db.find_one(sql)['status']
                self.assertEqual(expected['status'], status)
        except AssertionError as e:
            log.error('这是【{}】用例执行失败'.format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info('这是【{}】用例执行成功'.format(item['title']))
