"""
============================
Author:蓝色水汀
Time:2020/12/26  14:22
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import unittest
import os
import requests
from unittestreport import ddt, list_data
from common.excel_option import ReadExcel
from common.path_option import Data_Path
from common.conf_option import conf
from common.assert_option import assert_dict_in
from common.log_option import log
from common.mysql_option import OptionDB
from testcases.fixture import BaseTest
from common.replace_option import data_replace


@ddt
class TestUpdate(unittest.TestCase, BaseTest):
    excel = ReadExcel(os.path.join(Data_Path, 'cases.xlsx'), 'update')
    cases = excel.read_excel()
    base_url = conf.get('env', 'base_url')
    db = OptionDB()

    @classmethod
    def setUpClass(cls):
        # 创建测试类对象，赋值为从已封装的登录接口提取的headers和member_id
        cls.user_login()

    @list_data(cases)
    def test_update(self, item):
        url_update = self.base_url + item['url']
        method_update = item['method'].lower()
        # item['data'] = item['data'].replace('##member_id##', str(self.member_id))
        # 调用封装的替换方法，用测试类对象的member_id值替换用例数据中的字符串
        item['data'] = data_replace(item['data'], TestUpdate)
        params_update = eval(item['data'])
        response_update = requests.request(method=method_update, url=url_update, json=params_update,
                                           headers=self.headers)
        res_update = response_update.json()
        sql = 'select * from futureloan.member where reg_name="{}"'.format(params_update.get('reg_name', ""))
        count = self.db.find_count(sql)
        expected_update = eval(item['expected'])
        try:
            assert_dict_in(expected_update, res_update)
            if item['flag']:
                self.assertEqual(1, count)
        except AssertionError as e:
            log.error('这是【{}】用例执行失败'.format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info('这是【{}】用例执行成功'.format(item['title']))
