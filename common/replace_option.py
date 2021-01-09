"""
============================
Author:蓝色水汀
Time:2020/12/30  14:20
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import re
from common.conf_option import conf


def data_replace(data, cls):
    """
    替换数据方法
    :param data: 要进行替换的用例数据（字符串）
    :param cls: 测试类
    :return: 返回用例数据
    """
    while re.search('##(.+?)##', data):
        # 扫描整个data字符串，返回第一个成功匹配的字符串
        res = re.search('##(.+?)##', data)
        # 显示匹配到的第一个字符串内容
        item = res.group()
        # 显示匹配到的第一个字符串第一个括号里面的内容
        attr = res.group(1)
        try:
            # 从用例数据中获取值
            value = getattr(cls, attr)
        except AttributeError:
            # 从配置文件中获取值
            value = conf.get('test_data', attr)
        # 用获取的值替换字符串
        data = data.replace(item, str(value))
    return data
