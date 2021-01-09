"""
============================
Author:蓝色水汀
Time:2020/12/26  14:22
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import unittest
import requests
from common.conf_option import conf
from common.assert_option import assert_dict_in
from common.log_option import log
from testcases.fixture import BaseTest


class TestGetInfo(unittest.TestCase,BaseTest):
    base_url = conf.get('env', 'base_url')

    @classmethod
    def setUpClass(cls):
        cls.user_login()

    def test_getinfo(self):
        url_getinfo = self.base_url + '/member/{}/info'.format(self.member_id)
        response = requests.get(url=url_getinfo, headers=self.headers)
        actual = response.json()
        expected = {"code": 0, "msg": "OK"}
        try:
            assert_dict_in(expected, actual)
        except AssertionError as e:
            log.error('获取用户信息失败')
            log.exception(e)
            raise e
        else:
            log.info('获取用户信息成功')
