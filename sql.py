import pymysql
from DBUtils.PooledDB import PooledDB

class MySQL:#数据库操作类
    #类共有的连接池
    pool = None

    def __init__(self,**kwargs):#初始化
        self.pool = self._get_pool(**kwargs)

    @classmethod
    def _get_pool(cls,**kwargs):#初始化一个池子
        if cls.pool is None:
            cls.pool = PooledDB(
                creator=pymysql,
                maxconnections=5,
                mincached=3,
                maxcached=3,
                blocking=True,
                maxusage=100,
                setsession=['SET NAMES utf8mb4'],#mysql8.0版本以后默认是utf8mb4编码方式.
                **kwargs
            )
        return cls.pool

    def _execute_main(self,sql,method=None):#主页面
        cnn = self.pool.connection()
        cursor = cnn.cursor()
        try:
            if method == "sql_1":
                cursor.execute(sql)
                return cursor.fetchone()
            elif method == "sql_2":
                cursor.execute(sql)
                return cursor.fetchone()[0]
        except Exception as e:
            raise e
        finally:
            cursor.close()
            cnn.close()


    def _execute_operation_gui(self,sql,elements=None,method=None):#学生管理页面
        cnn = self.pool.connection()
        cursor = cnn.cursor()
        try:
            if method == 'sql_1':
                cursor.execute(sql)
                return cursor.fetchall()
            elif method == 'sql_2':
                cursor.execute(sql,(elements))
                cnn.commit()
            elif method == 'sql_heading':
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            cnn.close()


    def _execute_Gui_Student(self,sql,elements=None,method=None):#学生添加&删除页面
        cnn = self.pool.connection()
        cursor = cnn.cursor()
        try:
            if method == 'sql':
                cursor.execute(sql,elements)
                return cursor.fetchall()
            elif method == 'sql_additional':#修改
                cursor.execute(sql,elements)
                cnn.commit()
            elif method == 'sql_extra':#添加
                cursor.execute(sql,elements)
                cnn.commit()
            elif method == 'sql_attribute':#自定义属性的添加
                cursor.execute(sql,elements)
                cnn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            cnn.close()


    def _execute_attribute(self,sql,elements=None,method=None):#属性管理
        cnn = self.pool.connection()
        cursor = cnn.cursor()
        try:
            if method == 'add':
                cursor.execute(sql)
                cnn.commit()
            elif method == 'delete':
                cursor.execute(sql)
                cnn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            cnn.close()


    def _execute_excel(self,sql,elements=None,method=None):#excel批量上传下载
        cnn = self.pool.connection()
        cursor = cnn.cursor()
        try:
            if method == 'sql_column':
                cursor.execute(sql)
                return cursor.fetchall()
            elif method == 'sql_add':
                cursor.execute(sql,elements)
                cnn.commit()
            elif method == 'sql_query':
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            cnn.close()

    def _execute_user(self,sql,elements=None,method=None):#user信息
        cnn = self.pool.connection()
        cursor = cnn.cursor()
        try:
            if method == 'sql_read':
                cursor.execute(sql)
                return cursor.fetchall()[0]
            elif method == 'sql_write':
                cursor.execute(sql,elements)
                cnn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            cnn.close()

    def _keep_connection(self,sql):#用来定期执行简单的查询操作，保持数据库连接的正常存在
        cnn = self.pool.connection()
        cursor = cnn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            cnn.close()