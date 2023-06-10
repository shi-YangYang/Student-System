import pymysql
import random
import random

chinese_chars = ["春", "夏", "秋", "冬", "山", "水", "云", "雨", "风", "花", "草", "树", "竹", "鱼", "鸟", "虫", "犬", "猫", "马", "牛", "羊", "鸡", "鸭", "鹅", "蝴", "蝶", "蜜", "蜂", "蚂", "蚁", "熊", "猴", "兔", "狐", "狸", "獾", "豹", "虎", "狮", "象", "猪", "狗", "熊", "鹿", "麋", "鲸", "海", "岛"]

def generate_random_tuples(num):
    results = []
    for i in range(num):
        sno = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        name = ''.join(random.sample(chinese_chars, random.randint(3, 4)))
        gender = random.choice(["男", "女"])
        subject = ''.join(random.sample(chinese_chars, random.randint(2, 4)))
        num = ''.join([str(random.randint(0, 9)) for _ in range(11)])
        home = ''.join(random.sample(chinese_chars, random.randint(1, 6)))
        results.append((sno, name, gender, subject, num, home))
    return results

# 生成10个随机元组的列表
'''
result = generate_random_tuples(10)
print(result)
'''

# 连接数据库

cnn = pymysql.connect(host='xxx',
                        user='xxx',
                        password='xxx',
                        database='xxx',
                        port=3306)

cursor = cnn.cursor()

cursor.execute("SELECT name,academy,number,sno FROM authme WHERE id=12")
print(cursor.fetchall()[0])
'''
fixed_result = ['id', 'sno', 'name', 'gender', 'subject', 'num', 'home']
heading_result = [item[0] for item in p if item not in fixed_result]
print(heading_result)
'''
"""
p = cursor.fetchall()
p = [item[0] for item in p]
print(p)
"""

"""
# 插入随机排列后的数据
sql = "INSERT INTO student_1 (sno,name,gender,subject,num,home) VALUES (%s,%s,%s,%s,%s,%s)"
for item in result:
    cursor.execute(sql,item)
cnn.commit()
cnn.close()
"""