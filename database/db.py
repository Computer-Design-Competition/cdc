import pymysql

class database:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', passwd='12li2969', db='covid_data', use_unicode=1, charset='utf8')
        self.cursor = self.db.cursor()
    
    def get_data_accumulated(self, date, country, province, city):
        """
            return the accumulated data till date time
            date: "YYYY-MM-DD"
            country: "中文"
            province: "中文"
            city: "中文"
        """
        sql = "SELECT * FROM covid_data WHERE date = '{}' AND country = '{}' AND province = '{}' AND city = '{}'".format(date, country, province, city)
        try:
            self.cursor.execute(sql)
            
            results= self.cursor.fetchall()
            print(type(results[0][0]))
        except Exception as e:
            print(e)
            print ("Error: unable to fetch data")
    def get_data_date(self, date, country, province, city):
        pass

if __name__ == "__main__":
    
    test = database()
    test.get_data_accumulated("2020-02-21", "中国", "广东省", "广州")