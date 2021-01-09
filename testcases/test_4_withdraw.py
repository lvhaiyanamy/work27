"""
============================
Author:蓝色水汀
Time:2020/12/23  16:47
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import unittest
import os
import requests
from common.excel_option import ReadExcel
from common.path_option import Data_Path
from unittestreport import ddt, list_data
from common.conf_option import conf
from common.assert_option import assert_dict_in
from common.log_option import log
from common.mysql_option import OptionDB
from common.replace_option import data_replace
from testcases.fixture import BaseTest


@ddt
class TestWithdraw(unittest.TestCase,BaseTest):
    # 从Excel读取用例数据
    excel = ReadExcel(os.path.join(Data_Path, 'cases.xlsx'), 'withdraw')
    cases = excel.read_excel()
    # 从配置文件获取基础路径和请求头
    base_url = conf.get('env', 'base_url')
    # 创建操作数据库对象
    db = OptionDB()

    @classmethod
    def setUpClass(cls):
        # 创建测试类对象，赋值为从已封装的登录接口提取的headers和member_id
        cls.user_login()

    @list_data(cases)
    def test_withdraw(self, item):
        url_withdraw = self.base_url + item['url']
        method = item['method'].lower()
        # 用上面得到的用户id替换测试用例中的用户id
        # item['data'] = item['data'].replace('##member_id##', str(self.member_id))
        # 调用封装的替换方法，用测试类对象的member_id值替换用例数据中的字符串
        item['data']=data_replace(item['data'],TestWithdraw)
        # 请求参数
        params_withdraw = eval(item['data'])
        # %%%%%%%%%%%%%%%%%%%请求接口之前查询用户的余额%%%%%%%%%%%%%%%%
        sql = 'SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}'.format(conf.get('test_data',
                                                                                                 'mobile_phone'))
        # %%%%%%%%%%%%%%%%%%%请求接口之前查询用户的余额%%%%%%%%%%%%%%%%
        start_amount = self.db.find_one(sql)['leave_amount']
        # 请求接口，获得返回值
        response_withdraw = requests.request(method, url=url_withdraw, json=params_withdraw, headers=self.headers)
        actual_withdraw = response_withdraw.json()
        # %%%%%%%%%%%%%%%%%%%请求接口之前查询用户的余额%%%%%%%%%%%%%%%%
        end_amount = self.db.find_one(sql)['leave_amount']
        expected_withdraw = eval(item['expected'])
        try:
            assert_dict_in(expected_withdraw, actual_withdraw)
            # 运行成功的用例中，判断提现前的金额减去提现后的金额是否等于用例中的提现金额
            if item['flag']:
                self.assertEqual(params_withdraw['amount'], float(start_amount - end_amount))
        except AssertionError as e:
            log.error('这是【{}】用例执行失败'.format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info('这是【{}】用例执行通过'.format(item['title']))
