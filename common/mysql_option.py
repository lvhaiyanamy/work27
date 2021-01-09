"""
============================
Author:蓝色水汀
Time:2020/12/25  10:57
E-mail:826926575@qq.com
Company:陕西伟业医药有限公司
============================
"""
import pymysql
from common.conf_option import conf


class OptionDB:
    def __init__(self):
        self.con = pymysql.connect(
            host=conf.get('database', 'host'),
            port=conf.getint('database', 'port'),
            user=conf.get('database', 'user'),
            password=conf.get('database', 'password'),
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )

    def find_all(self, sql):
        """查询到的所有数据"""
        with self.con as cur:
            cur.execute(sql)
        res_all = cur.fetchall()
        cur.close()
        return res_all

    def find_one(self, sql):
        """查询第一条数据"""
        with self.con as cur:
            cur.execute(sql)
        res_one = cur.fetchone()
        cur.close()
        return res_one

    def find_count(self, sql):
        """查询数据条数"""
        with self.con as cur:
            res_count = cur.execute(sql)
        cur.close()
        return res_count

    def update(self, sql):
        """更新数据库"""
        with self.con as cur:
            cur.execute(sql)
        self.con.commit()

    def __del__(self):
        self.con.close()
