"""
============================
Author:蓝色水汀
Time:2020/12/23  13:12
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
class TestRecharge(unittest.TestCase,BaseTest):
    # 从Excel读取用例数据
    excel = ReadExcel(os.path.join(Data_Path, 'cases.xlsx'), 'recharge')
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
    def test_register(self, item):
        url_recharge = self.base_url + item['url']
        method = item['method'].lower()
        # 用上面得到的用户id替换测试用例中的用户id
        # item['data'] = item['data'].replace('##member_id##', str(self.member_id))
        # 调用封装的替换方法，用测试类对象的member_id值替换用例数据中的字符串
        item['data']=data_replace(item['data'], TestRecharge)
        params_recharge = eval(item['data'])
        # %%%%%%%%%%%%%%%%%%%请求接口之前查询用户的余额%%%%%%%%%%%%%%%%
        sql = 'SELECT leave_amount FROM futureloan.member WHERE id={}'.format(self.member_id)
        # %%%%%%%%%%%% 执行sql查询充值前余额%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        start_amount = self.db.find_one(sql)['leave_amount']
        # 请求接口，获得返回值
        response_recharge = requests.request(method, url=url_recharge, json=params_recharge, headers=self.headers)
        actual_recharge = response_recharge.json()
        print(actual_recharge)
        # %%%%%%%%%%%% 执行sql查询充值后余额%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        end_amount = self.db.find_one(sql)['leave_amount']
        expected_recharge = eval(item['expected'])
        try:
            assert_dict_in(expected_recharge, actual_recharge)
            # 运行成功的用例中，判断充值后的金额减去充值前的金额是否等于用例中的充值金额
            if item['flag']:
                self.assertEqual(params_recharge['amount'], float(end_amount - start_amount))
        except AssertionError as e:
            log.error('这是【{}】用例执行失败'.format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info('这是【{}】用例执行通过'.format(item['title']))
