"""
============================
Author:蓝色水汀
Time:2021/1/6  10:38
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import requests
from jsonpath import jsonpath
from common.conf_option import conf


class BaseTest:
    # --------------------------------管理员登录-------------------------------------
    @classmethod
    def admin_login(cls):
        url = conf.get('env', 'base_url') + '/member/login'
        params = {
            'mobile_phone': conf.get('test_data', 'admin_phone'),
            'pwd': conf.get('test_data', 'admin_pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        print(res)
        admin_token = jsonpath(res, '$..token')[0]
        headers['Authorization'] = 'Bearer ' + admin_token
        cls.headers_admin = headers
        cls.member_id_admin = jsonpath(res, '$..id')[0]

    # --------------------------------普通用户登录-------------------------------------
    @classmethod
    def user_login(cls):
        url = conf.get('env', 'base_url') + '/member/login'
        # 从配置文件读取登录接口所需要的参数mobile_phone和pwd
        params = {
            'mobile_phone': conf.get('test_data', 'mobile_phone'),
            'pwd': conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        # 请求登录接口
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        # 从接口响应信息里面提取token和member_id
        token = jsonpath(res, '$..token')[0]
        cls.member_id = jsonpath(res, '$..id')[0]
        # 将提取出来的token存储在对象headers中
        headers['Authorization'] = 'Bearer ' + token
        cls.headers = headers

    # --------------------------------添加项目-------------------------------------
    @classmethod
    def add_project(cls):
        url_add = conf.get('env', 'base_url') + '/loan/add'
        params_add = {
            "member_id": cls.member_id,
            "title": "蓝色水汀的项目",
            "amount": 2000,
            "loan_rate": 12.0,
            "loan_term": 6,
            "loan_date_type": 1,
            "bidding_days": 5
        }
        response_add = requests.post(url=url_add, json=params_add, headers=cls.headers)
        res_add = response_add.json()
        cls.loan_id = jsonpath(res_add, '$..id')[0]
