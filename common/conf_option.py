"""
============================
Author:蓝色水汀
Time:2020/12/11  10:14
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
from configparser import ConfigParser
import os
from common.path_option import Conf_Path


# 创建配置文件类Config，继承父类ConfigParser


class Config(ConfigParser):
    def __init__(self, conf_file):
        # 子类和父类的方法重名，使用super().方法名()调用父类方法
        super().__init__()
        # 读取配置文件
        self.read(conf_file, encoding='utf-8')

# 创建config对象，读取指定路径的配置文件


conf = Config(os.path.join(Conf_Path, 'conf.ini'))
