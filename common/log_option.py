"""
============================
Author:蓝色水汀
Time:2020/12/11  10:14
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import logging
from common.conf_option import conf
import os
from common.path_option import Log_Path


def creat_log(name='mylog', level='DEBUG', filename='log', fh_level='DEBUG', sh_level='DEBUG',):
    """
    定义一个创建日志的方法，包含以下参数：
    :param name: 日志收集器的名称，默认值为“mylog”
    :param level: 日志收集器的level，默认值为“DEBUG”
    :param filename: 输出的日志文件名称，默认值为“log”
    :param fh_level: 输出到文件的日志level，默认值为“DEBUG”
    :param sh_level: 输出到控制台的日志level，默认值为“DEBUG”
    :return: 返回一个日志文件
    """
    # 创建日志收集器
    log = logging.getLogger(name)
    # 设置收集器level
    log.setLevel(level)
    # 第一种方式将日志输出到指定目录：
    # logging.basicConfig(filename=r'./logs/'+filename+'.log',
    #                     format='%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s',
    #                     level=fh_level
    #                     )
    # 第二种方式将日志输出到指定目录：
    # 创建一个输出到文件的输出渠道
    fh = logging.FileHandler(filename, encoding='utf-8')
    # 设置输出到文件的日志level
    fh.setLevel(fh_level)
    # 将日志输出渠道绑定到日志收集器上
    log.addHandler(fh)
    # 输出日志到控制台
    # 创建一个输出到控制台的输出渠道
    sh = logging.StreamHandler()
    # 设置输出到控制台的日志level
    sh.setLevel(sh_level)
    # 将日志输出渠道绑定到日志收集器上
    log.addHandler(sh)
    # 设置输出的日志格式
    formats = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
    # 创建格式对象
    log_format = logging.Formatter(formats)
    # 为输出渠道设置输出格式
    sh.setFormatter(log_format)
    fh.setFormatter(log_format)
    # 返回一个日志收集器
    return log

# 创建日志对象，加载配置文件中的日志配置


log = creat_log(
    name=conf.get('logging', 'name'),
    level=conf.get('logging', 'level'),
    # 将日志保存至指定的目录中
    filename=os.path.join(Log_Path, conf.get('logging', 'filename')),
    fh_level=conf.get('logging', 'fh_level'),
    sh_level=conf.get('logging', 'sh_level')
)
