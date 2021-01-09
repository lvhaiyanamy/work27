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
  3) 审核项目（用例级别）
"""


@ddt
class TestInvest(unittest.TestCase, BaseTest):
    """
    继承父类unittest.TestCase和BaseTest
    """
    excel = ReadExcel(os.path.join(Data_Path, 'cases.xlsx'), 'invest')
    cases = excel.read_excel()
    base_url = conf.get('env', 'base_url')
    db = OptionDB()

    @classmethod
    def setUpClass(cls):
        # 用例的类前置，继承了父类BaseTest的方法和对象
        cls.user_login()
        cls.admin_login()
        # 定义一个类属性计数，用来判断哪些用例需要执行某个条件，哪些用例不需要
        cls.casecnt = 0

    def setUp(self):
        # -----------------------通过继承的父类BaseTest调用添加项目方法---------------------------------
        self.add_project()
        # -------------------------------审核项目——————————————————————
        url_audit = conf.get('env', 'base_url') + '/loan/audit'
        # 判断当运行第5条用例时，审核不通过
        if TestInvest.casecnt == 4:
            params_audit = {
                "loan_id": self.loan_id,
                "approved_or_not": False,
            }
        else:
            params_audit = {
                "loan_id": self.loan_id,
                "approved_or_not": True,
            }
        requests.patch(url=url_audit, json=params_audit, headers=self.headers_admin)

        # 判断当运行第11条用例时，手动更新项目的状态，将状态设置为3
        if TestInvest.casecnt == 10:
            sql1 = 'update futureloan.loan set status=3 where id={}'.format(self.loan_id)
            self.db.update(sql1)
        TestInvest.casecnt += 1

    @list_data(cases)
    def test_invest(self, item):
        url_invest = self.base_url + item['url']
        method = item['method']
        expected = eval(item['expected'])
        item['data'] = data_replace(item['data'], TestInvest)
        params = eval(item['data'])
        # 在投资表里查询该项目投资前的数量
        sql_invest = 'select * from futureloan.invest where loan_id={}'.format(self.loan_id)
        count_start = self.db.find_count(sql_invest)

        # 在用户表里查询投资用户投资前的可用余额
        sql_amount = "select leave_amount from futureloan.member where id='{}'".format(self.member_id)
        amount_start = self.db.find_one(sql_amount)['leave_amount']

        # 在流水表中查询投资人在投资该项目前的数据数量
        sql_finance = 'select * from futureloan.financelog where pay_member_id={}'.format(self.member_id)
        cnt_start = self.db.find_count(sql_finance)

        # 请求接口，获取响应值
        response_invest = requests.request(method=method, url=url_invest, json=params, headers=self.headers)
        res_invest = response_invest.json()

        # 当用例数据的flag有值时，从投资响应结果中提取投资id，然后在回款列表查询回款记录数量
        if item['flag']:
            invest_id = jsonpath(res_invest, '$..id')[0]
            sql_repay = 'select * from futureloan.repayment where invest_id={}'.format(invest_id)
            self.count_repay = self.db.find_count(sql_repay)

        # 在投资表里查询该项目投资后的数量
        count_end = self.db.find_count(sql_invest)

        # 在用户表里查询投资用户投资后的可用余额
        amount_end = self.db.find_one(sql_amount)['leave_amount']

        # 在流水表中查询投资人在投资该项目后的数据数量
        cnt_end = self.db.find_count(sql_finance)

        # 在项目表中，查询该项目的当前状态
        sql_status = 'select status from futureloan.loan where id={}'.format(self.loan_id)
        actual_status = self.db.find_one(sql_status)['status']
        try:
            self.assertEqual(expected['code'], res_invest['code'])
            self.assertIn(expected['msg'], res_invest['msg'])

            # 当运行第一条用例时，判断回款记录数是否和预期的数量一致
            if self.casecnt == 1:
                self.assertEqual(6, self.count_repay)

            # 当用例数据的flag有值时，进行以下断言
            if item['flag']:
                # 断言投资成功后，投资表里有没有多1条数据
                self.assertEqual(1, count_end - count_start)

                # 断言投资成功后，用户投资前可用余额减去投资后可用余额是否等于投资金额
                self.assertEqual(params['amount'], float(amount_start - amount_end))

                # 断言投资成功后，流水表是不是多了一条数据
                self.assertEqual(1, cnt_end - cnt_start)

                # 断言投资成功后，项目的实际状态和预期状态是否一致
                self.assertEqual(expected['status'], actual_status)

        except AssertionError as e:
            log.error('这是【{}】用例执行失败'.format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info('这是【{}】用例执行成功'.format(item['title']))
