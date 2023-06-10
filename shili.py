import pymysql
try:
    print("数据库连接中.....")
    cnn = pymysql.connect(host='xxx',  # 外网ip地址
                          user='xxx',  # 账号
                          password='xxx',  # 密码
                          database='xxx',  # 库名
                          port=3306)  # 端口
    cursor = cnn.cursor()
    print("连接成功！！！")
except Exception:
    print("连接失败!!!")
try:
    print("数据库创建中.....")
    sql = """CREATE TABLE authme(
            id INT PRIMARY KEY AUTO_INCREMENT,
            account VARCHAR(255) DEFAULT '',
            password VARCHAR(255) DEFAULT '',
            number VARCHAR(255) DEFAULT '',
            name VARCHAR(255) DEFAULT '',
            academy VARCHAR(255) DEFAULT '',
            sno VARCHAR(255) DEFAULT '',
            gender VARCHAR(255) DEFAULT '')"""
    cursor.execute(sql)
    print("创建成功！！！")
except Exception:
    print("创建失败!!!")