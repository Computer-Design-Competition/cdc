# import pymysql
# import random
# db = pymysql.connect(host='localhost', user='root', passwd='12li2969', db='covid_data', use_unicode=1, charset='utf8')
# cursor = db.cursor()
# # sql = "INSERT INTO covid_data(date, country, province, city, confirmed, cured, death) VALUES ('2020-3-{}', '中国', '广东省', '广州', {}, {}, {});"

# try:
# #    # 执行sql语句
# #     confirmed = 821 + random.randint(0,30)
# #     cured = 868 + random.randint(0,30)
# #     death = 879 + random.randint(0,30)
# #     for i in range(1, 30):
# #         sql_ = sql.format(i, confirmed, cured, death)
# #         cursor.execute(sql_)
# #         db.commit()
# #         confirmed += random.randint(0,30)
# #         cured += random.randint(0,30)
# #         death += random.randint(0,30)
#     sql_ = "INSERT INTO covid_data(date, country, confirmed, cured, death) VALUES ('2020-3-2', '美国', 24, 214, 23);"
#     cursor.execute(sql_)
#     db.commit()
# except Exception as e:
#     print(e)
#     # 如果发生错误则回滚
#     db.rollback()
 
# # 关闭数据库连接
# db.close()

# import datetime
# # 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
# def getdate(date, beforeOfDay):
#     date_ = date.split('-')
#     date_ = [int(i) for i in date_]
#     print(date_)
#     today = datetime.date(date_[0], date_[1], date_[2])
#     print(today)
#     # 计算偏移量
#     offset = datetime.timedelta(days=-beforeOfDay)
#     # 获取想要的日期的时间
#     pre_date = (today + offset).strftime('%Y-%m-%d')
#     return pre_date
# if __name__ == "__main__":
#     print(getdate("2020-02-01", 1))

from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker


v = Faker.choose()
print(v)
print(Faker.values())
c = (
    Pie()
    .add(
        "",
        [list(z) for z in zip(v, Faker.values())],
        radius=["30%", "75%"],
        center=["75%", "50%"],
        rosetype="area",
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Pie-玫瑰图示例"))
    .render("pie_rosetype.html")
)