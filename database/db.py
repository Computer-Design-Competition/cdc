import pymysql
import date_fun
class database:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', passwd='12li2969', db='covid_data', use_unicode=1, charset='utf8')
        self.cursor = self.db.cursor()
        self.fields = ["date", "country", "province", "city", "confirmed", "cured", "death"]
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

            ans = {}
            for i in range(len(results[0])):
                if i == 0:
                    ans[self.fields[i]] = str(results[0][i])
                else:
                    ans[self.fields[i]] = results[0][i]
            # print(ans)
            return ans
        except Exception as e:
            print(e)
            print ("Error: unable to fetch data")
    def get_data_date(self, date, country, province, city):
        """
            return the accumulated data till date time
            date: "YYYY-MM-DD"
            country: "中文"
            province: "中文"
            city: "中文"
        """
        pre_day = date_fun.getdate(date, 1)
        pre_data = self.get_data_accumulated(pre_day, country, province, city)
        date_data = self.get_data_accumulated(date, country, province, city)
        for i in range(len(pre_data)):
            if i < 4:
                continue
            else:
                date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
        print(date_data)
        return date_data
if __name__ == "__main__":
    
    test = database()
    test.get_data_date("2020-03-02", "中国", "广东省", "广州")