"""
============================
Author:蓝色水汀
Time: 
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""


def assert_dict_in(expected, actual):
    """
    判断实际结果是否包含预期结果
    :param expected: 期望值
    :param actual: 实际值
    """
    for k, v in expected.items():
        if actual.get(k) == v:
            pass
        else:
            raise AssertionError("{} not in {}".format(expected, actual))
