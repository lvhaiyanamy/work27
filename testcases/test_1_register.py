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
import random
import openpyxl
import requests
from unittestreport import ddt, list_data
from openpyxl import styles
from common.log_option import log
from common.excel_option import ReadExcel
from common.path_option import Data_Path
from common.conf_option import conf
from common.assert_option import assert_dict_in
from common.mysql_option import OptionDB
from common.replace_option import data_replace


@ddt
class TestRegister(unittest.TestCase):
    # 创建一个读取Excel的对象
    excel = ReadExcel(os.path.join(Data_Path, 'cases.xlsx'), 'register')
    # 利用创建的对象调用读取Excel方法
    cases = excel.read_excel()
    # 从配置文件读取项目的基本地址
    base_url = conf.get('env', 'base_url')
    # 请求头
    headers = eval(conf.get('env', 'headers'))
    # 创建操作数据库对象
    db = OptionDB()

    def random_phone(self):
        phone = random.randint(15300000000, 15399999999)
        return phone

    @list_data(cases)
    def test_register(self, item):
        # 第一步：准备用例数据
        # 1、接口请求地址
        url_register = self.base_url + item['url']
        # 2、接口请求参数
        if '##mobile_phone##' in item['data']:
            # 给测试类TestRegister动态设置对象mobile_phone,且对象值为随机方法生成的数值
            setattr(TestRegister, 'mobile_phone', self.random_phone())
            # 调用封装的替换方法，用测试类对象的mobile_phone值替换用例数据中的字符串
            item['data'] = data_replace(item['data'], TestRegister)
        # phone = self.random_phone()
        # item['data'] = item['data'].replace('##mobile_phone##', str(phone))
        params = eval(item['data'])
        print(params)
        # 3、请求方法,并转换为小写
        method = item['method'].lower()
        # 4、从配置文件获取请求头
        # 5、获取期望值
        expected_register = eval(item['expected'])
        # 第二步：请求接口，获取返回实际结果
        response_register = requests.request(method, url_register, headers=self.headers, json=params)
        actual_register = response_register.json()
        # 从数据库中查询注册数据数量,字典的get方法，在参数中查找键mobile_phone，找不到时用""替代
        sql = 'select * from futureloan.member where mobile_phone="{}"'.format(params.get('mobile_phone', ""))
        res1 = self.db.find_count(sql)

        # 第三步：断言，捕获异常
        try:
            # 断言实际结果是否包含预期结果
            assert_dict_in(expected_register, actual_register)
            # 判断用例是否需要进行数据库校验
            if item['flag']:
                # 从数据库中查询出的数据条数和1对比，如果有1条，则注册成功
                self.assertEqual(1, res1)

        except AssertionError as e:
            # 往日志文件中写入执行结果
            log.error('这是【{}】用例执行失败'.format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info('这是【{}】用例执行通过'.format(item['title']))
