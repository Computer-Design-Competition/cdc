import pymysql
import random
db = pymysql.connect(host='localhost', user='root', passwd='12li2969', db='covid_data', use_unicode=1, charset='utf8')
cursor = db.cursor()
sql = "INSERT INTO covid_data(date, country, province, city, confirmed, cured, death) VALUES ('2020-3-{}', '中国', '广东省', '广州', {}, {}, {});"

try:
   # 执行sql语句
    confirmed = 393 + random.randint(0,30)
    cured = 453 + random.randint(0,30)
    death = 442 + random.randint(0,30)
    for i in range(1, 30):
        sql_ = sql.format(i, confirmed, cured, death)
        cursor.execute(sql_)
        db.commit()
        confirmed += random.randint(0,30)
        cured += random.randint(0,30)
        death += random.randint(0,30)
except Exception as e:
    print(e)
    # 如果发生错误则回滚
    db.rollback()
 
# 关闭数据库连接
db.close()