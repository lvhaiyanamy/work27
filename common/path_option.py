"""
============================
Author:蓝色水汀
Time: 
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import os

# 获取项目根目录
Base_Path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取配置文件目录
Conf_Path = os.path.join(Base_Path, 'conf')
# 获取测试数据文件目录
Data_Path = os.path.join(Base_Path, 'datas')
# 获取日志文件目录
Log_Path = os.path.join(Base_Path, 'logs')
# 获取测试用例文件目录
Cases_Path = os.path.join(Base_Path, 'testcases')
# 获取测试报告文件目录
Report_Path = os.path.join(Base_Path, 'reports')
