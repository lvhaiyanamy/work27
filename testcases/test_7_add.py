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
from unittestreport import ddt, list_data
from common.excel_option import ReadExcel
from common.path_option import Data_Path
from common.conf_option import conf
from common.mysql_option import OptionDB
from common.assert_option import assert_dict_in
from common.log_option import log
from testcases.fixture import BaseTest
from common.replace_option import data_replace


@ddt
class TestAdd(unittest.TestCase,BaseTest):
    excel = ReadExcel(os.path.join(Data_Path, 'cases.xlsx'), 'add')
    cases = excel.read_excel()
    base_url = conf.get('env', 'base_url')
    db = OptionDB()

    @classmethod
    def setUpClass(cls):
        # 创建测试类对象，赋值为从已封装的登录接口提取的headers_normal和member_id
        cls.user_login()

    @list_data(cases)
    def test_add(self, item):
        url_add = self.base_url + item['url']
        method = item['method']
        # item['data'] = item['data'].replace('##member_id##', str(self.member_id))
        # 调用封装的替换方法，用测试类对象的member_id值替换用例数据中的字符串
        item['data'] = data_replace(item['data'], TestAdd)
        params_add = eval(item['data'])
        expected = eval(item['expected'])
        sql = 'select * from futureloan.loan where member_id={}'.format(self.member_id)
        start_count = self.db.find_count(sql)
        response_add = requests.request(method=method, url=url_add, json=params_add, headers=self.headers)
        res_add = response_add.json()
        end_count = self.db.find_count(sql)
        try:
            assert_dict_in(expected, res_add)
            if item['flag']:
                self.assertEqual(1, end_count-start_count)
            else:
                self.assertEqual(0, end_count - start_count)
        except AssertionError as e:
            log.error('这是【{}】用例执行失败'.format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info('这是【{}】用例执行成功'.format(item['title']))



