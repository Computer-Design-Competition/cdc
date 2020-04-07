import pymysql
import date_fun
import createdb
class database:
    def __init__(self):
        self.db = pymysql.connect(host='118.31.41.159', user='root', passwd='12Li2969/', db='covid_data', use_unicode=1, charset='utf8')
        self.cursor = self.db.cursor()
        self.fields = ["date", "country", "province", "city", "confirmed", "cured", "death"]
        self.fields2 = ["date", "country", "confirmed", "cured", "death"]
    def get_data_accumulated(self, date, country, province='', city=''):
        """
            return the accumulated data till date time
            date: "YYYY-MM-DD"
            country: "中文"
            province: "中文"
            city: "中文"
        """
        if province != '' and city != '':
            sql = 'SELECT * from data where date = "{}" AND country = "{}" AND province = "{}" AND city = "{}"'.format(date, country, province, city)
        elif province == '' or city == '':
            sql = "SELECT date, country, confirmed, cured, death from data where date = '{}' AND country = '{}'".format(date, country)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            ans = {}
            for i in range(len(results[0])):
                if province != '' and city != '':
                    if i == 0:
                        ans[self.fields[i]] = str(results[0][i])
                    else:
                        ans[self.fields[i]] = results[0][i]
                elif province == '' or city == '':
                    if i == 0:
                        ans[self.fields2[i]] = str(results[0][i])
                    else:
                        ans[self.fields2[i]] = results[0][i]
            # print(ans)
            return ans
        except Exception as e:
            print(e)
            print("Error: unable to fetch data")

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

    def barchart(self, Type, date, country='', province=''):
        # 如果country='', province必须='',外国;如果country!='' province='',中国各省;如果country!='' province='',该省的各市
        # 外国
        if country == '':
            country_list = createdb.country_list # 所有外国国家
            # 格式 {'USA': {'date': '2020-4-1', 'country': 'USA', 'confirmed': '1', 'cured': '1', 'death': '2'}}
            all_country_date_data = {}
            if Type == 'accumulated':
                for country in country_list:
                    date_data = self.get_data_accumulated(date, country)
                    all_country_date_data[country] = date_data
                return all_country_date_data
            if Type == 'someday':
                for country in country_list:
                    pre_day = date_fun.getdate(date, 1)
                    date_data = self.get_data_accumulated(date, country)
                    if pre_day != '2020-01-21':
                        pre_data = self.get_data_accumulated(pre_day, country)
                        for i in range(len(pre_data)):
                            if i < 2:
                                continue
                            else:
                                date_data[self.fields2[i]] = date_data[self.fields2[i]] - pre_data[self.fields2[i]]
                    all_country_date_data[country] = date_data
                return all_country_date_data
        # 中国
        # 全国各省
        elif country != '':
            if province == '':
                # 格式 {'guangdong': {'date': '2020-4-1', 'country': 'China', 'province':'gd', confirmed': '1', 'cured': '1', 'death': '2'}}
                all_province_date_data = {}
                province_list = createdb.province_list
                if Type == 'accumulated':
                    for province in province_list.keys():
                        province_date_data = {'date': date, 'country': 'China', 'province': province, 'confirmed': 0, 'cured': 0, 'death': 0}
                        for city in province_list[province]:
                            # 这些数据要删除
                            if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                                continue
                            date_data = self.get_data_accumulated(date, country, province, createdb.hp(city))
                            province_date_data['confirmed'] += date_data['confirmed']
                            province_date_data['cured'] += date_data['cured']
                            province_date_data['death'] += date_data['death']
                        all_province_date_data[province] = province_date_data
                    return all_province_date_data
                if Type == 'someday':
                    pre_day = date_fun.getdate(date, 1)
                    for province in province_list.keys():
                        province_date_data = {'date': date, 'country': 'China', 'province': province, 'confirmed': 0, 'cured': 0, 'death': 0}
                        for city in province_list[province]:
                            # 这些数据要删除
                            if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                                continue
                            date_data = self.get_data_accumulated(date, country, province, createdb.hp(city))
                            if pre_day != '2020-01-21':
                                pre_data = self.get_data_accumulated(pre_day, country, province, createdb.hp(city))
                                for i in range(len(pre_data)):
                                    if i < 4:
                                        continue
                                    else:
                                        date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                            province_date_data['confirmed'] += date_data['confirmed']
                            province_date_data['cured'] += date_data['cured']
                            province_date_data['death'] += date_data['death']
                        all_province_date_data[province] = province_date_data
                    return all_province_date_data
            # 该省各市
            if province != '':
                # 格式 {'guangzhou': {'date': '2020-4-1', 'country': 'China', 'province':'gd', 'city': 'gz', confirmed': '1', 'cured': '1', 'death': '2'}}
                all_city_date_data = {}
                province_list = createdb.province_list
                if Type == 'accumulated':
                    for city in province_list[province]:
                        date_data = self.get_data_accumulated(date, country, province, createdb.hp(city))
                        all_city_date_data[createdb.hp(city)] = date_data
                    return all_city_date_data
                if Type == 'someday':
                    pre_day = date_fun.getdate(date, 1)
                    for city in province_list[province]:
                        date_data = self.get_data_accumulated(date, country, province, createdb.hp(city))
                        if pre_day != '2020-01-21':
                            pre_data = self.get_data_accumulated(pre_day, country, province, createdb.hp(city))
                            for i in range(len(pre_data)):
                                if i < 4:
                                    continue
                                else:
                                    date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                        all_city_date_data[createdb.hp(city)] = date_data
                    return all_city_date_data

    def linechart(self, Type, country, province='', city=''):
        if city != '' and province != '':
            city_date_data = {}
            if Type == 'accumulated':
                for date in createdb.date_list:
                    date_data = self.get_data_accumulated('2020-' + date, country, province, createdb.hp(city))
                    city_date_data['2020-' + date] = date_data
                return city_date_data
            if Type == 'someday':
                for date in createdb.date_list:
                    pre_day = date_fun.getdate('2020-' + date, 1)
                    date_data = self.get_data_accumulated('2020-' + date, country, province, createdb.hp(city))
                    if pre_day != '2020-01-21':
                        pre_data = self.get_data_accumulated(pre_day, country, province, createdb.hp(city))
                        for i in range(len(pre_data)):
                            if i < 4:
                                continue
                            else:
                                date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                    city_date_data['2020-' + date] = date_data
                return city_date_data
        if city == '' and province != '':
            all_province_date_data = {}
            if Type == 'accumulated':
                for date in createdb.date_list:
                    province_date_data = {'date': '2020-'+date, 'country': 'China', 'province': province, 'confirmed': 0,
                                          'cured': 0, 'death': 0}
                    province_list = createdb.province_list
                    for city in province_list[province]:
                        # 这些数据要删除
                        if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                            continue
                        date_data = self.get_data_accumulated('2020-'+date, country, province, createdb.hp(city))
                        province_date_data['confirmed'] += date_data['confirmed']
                        province_date_data['cured'] += date_data['cured']
                        province_date_data['death'] += date_data['death']
                    all_province_date_data['2020-' + date] = province_date_data
                return all_province_date_data
            if Type == 'someday':
                for date in createdb.date_list:
                    province_date_data = {'date': '2020-'+date, 'country': 'China', 'province': province, 'confirmed': 0,
                                          'cured': 0, 'death': 0}
                    pre_day = date_fun.getdate('2020-'+date, 1)
                    province_list = createdb.province_list
                    for city in province_list[province]:
                        # 这些数据要删除
                        if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                            continue
                        date_data = self.get_data_accumulated('2020-'+date, country, province, createdb.hp(city))
                        if pre_day != '2020-01-21':
                            pre_data = self.get_data_accumulated(pre_day, country, province, createdb.hp(city))
                            for i in range(len(pre_data)):
                                if i < 4:
                                    continue
                                else:
                                    date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                        province_date_data['confirmed'] += date_data['confirmed']
                        province_date_data['cured'] += date_data['cured']
                        province_date_data['death'] += date_data['death']
                    all_province_date_data['2020-' + date] = province_date_data
                return all_province_date_data
        if city == '' and province == '' and country != 'China':
            all_country_date_data = {}
            if Type == 'accumulated':
                for date in createdb.date_list:
                    date_data = self.get_data_accumulated('2020-'+date, country)
                    all_country_date_data['2020-'+date] = date_data
                return all_country_date_data
            if Type == 'someday':
                for date in createdb.date_list:
                    pre_day = date_fun.getdate('2020-'+date, 1)
                    date_data = self.get_data_accumulated('2020-'+date, country)
                    if pre_day != '2020-01-21':
                        pre_data = self.get_data_accumulated(pre_day, country)
                        for i in range(len(pre_data)):
                            if i < 2:
                                continue
                            else:
                                date_data[self.fields2[i]] = date_data[self.fields2[i]] - pre_data[self.fields2[i]]
                    all_country_date_data['2020-'+date] = date_data
                return all_country_date_data
        if city == '' and province == '' and country == 'China':
            all_country_date_data = {}
            if Type == 'accumulated':
                for date in createdb.date_list:
                    country_date_data = {'date': '2020-' + date, 'country': 'China', 'confirmed': 0, 'cured': 0, 'death': 0}
                    province_list = createdb.province_list
                    for province in province_list.keys():
                        print(province)
                        for city in province_list[province]:
                            # 这些数据要删除
                            if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                                continue
                            date_data = self.get_data_accumulated('2020-' + date, country, province, createdb.hp(city))
                            country_date_data['confirmed'] += date_data['confirmed']
                            country_date_data['cured'] += date_data['cured']
                            country_date_data['death'] += date_data['death']
                    all_country_date_data['2020-' + date] = country_date_data
                return all_country_date_data
            if Type == 'someday':
                for date in createdb.date_list:
                    country_date_data = {'date': '2020-' + date, 'country': 'China', 'confirmed': 0, 'cured': 0, 'death': 0}
                    pre_day = date_fun.getdate('2020-' + date, 1)
                    province_list = createdb.province_list
                    for province in province_list.keys():
                        for city in province_list[province]:
                            # 这些数据要删除
                            if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                                continue
                            date_data = self.get_data_accumulated('2020-' + date, country, province, createdb.hp(city))
                            if pre_day != '2020-01-21':
                                pre_data = self.get_data_accumulated(pre_day, country, province, createdb.hp(city))
                                for i in range(len(pre_data)):
                                    if i < 4:
                                        continue
                                    else:
                                        date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                            country_date_data['confirmed'] += date_data['confirmed']
                            country_date_data['cured'] += date_data['cured']
                            country_date_data['death'] += date_data['death']
                    all_country_date_data['2020-' + date] = country_date_data
                return all_country_date_data
if __name__ == "__main__":
    
    test = database()
    # print(test.barchart('someday', '2020-01-22', 'China', 'Hebei'))
    print(test.linechart('accumulated', 'China'))
    # test.get_data_date("2020-03-02", "China", "guangdong", "guangzhou")
