import pymysql
def authme(ss1,ss2):
    try:
        cnn = pymysql.connect(host='xxx',#外网ip地址
                            user='xxx',#账号
                            password='xxx',#密码
                            database='xxx',#库名
                            port=3306)#端口
        cursor = cnn.cursor()
        sql = "SELECT account,password,id FROM authme"
        cursor.execute(sql)
        #返回数据库中的所有账号密码
        reponse = cursor.fetchall()
        #遍历返回的账号密码
        for item in reponse:
            #若账号密码相互对应则返回
            if item[0] == ss1 and item[1] == ss2:
                cursor.close()
                cnn.close()
                return item[2]#->返回该账号密码元组的【id】->对应着用户的id
        cursor.close()
        cnn.close()
        return 0#->若不对应则返回0
    except Exception:#->网络异常的报错返回值
        return 'connect is error'

def register(account,password,number):
    try:
        cnn = pymysql.connect(host='xxx',
                            user='xxx',
                            password='xxx',
                            database='xxx',
                            port=3306)
        cursor = cnn.cursor()
        #查询数据库中账号
        sql_1 = "SELECT account FROM authme WHERE BINARY account=%s"
        #插入这个账号密码
        sql_2 = "INSERT INTO authme (account,password,number) VALUES (%s,%s,%s)"
        #判断该账号是否存在
        cursor.execute(sql_1,(account,))
        reponese_1 = cursor.fetchall()
        #若长度为0->代表着不存在
        if len(reponese_1) == 0:
            cursor.execute(sql_2,(account,password,number))
            cnn.commit()
            id = cursor.lastrowid#返回刚刚插入数据的id
            #创建该用户对应的学生表的sql语句
            sql_3 = """CREATE TABLE student_{} (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        sno VARCHAR(255),
                        name VARCHAR(255),
                        gender VARCHAR(255),
                        subject VARCHAR(255),
                        num VARCHAR(20),
                        home VARCHAR(255))""".format(id)

            #id->学生表主键
            #sno->学生学号
            #name->学生姓名
            #gender->学生性别
            #subject->学生专业
            #num->学生电话号码
            #home->学生家庭住址

            try:
                cursor.execute(sql_3)
                cnn.commit()
            except Exception:
                cursor.close()
                cnn.close()
                return 1#注册失败，请检查网络
            else:
                cursor.close()
                cnn.close()
                return 2#成功注册
        else:
            cursor.close()
            cnn.close()
            return 0#该用户已经被注册了
    except Exception:
        return 'connect is error'  # ->表示网路异常