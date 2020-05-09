# -*- coding: UTF-8 -*- 
from flask import Flask
from flask import request
import db
import json
import os
application = Flask(__name__)

@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
@application.route('/hotspotmap_json/',methods=["GET"])
def hotspotmap_json():
    try:
        db_ = db.database()
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        # print(params_dict)
        if "type" in params_dict.keys() and "date" in params_dict.keys():
            if params_dict["type"] == "someday":
                # get someday data
                if "country" in params_dict.keys():
                    if "province" in params_dict.keys():
                        # return the data of every city in the province of a particular day
                        data = db_.barchart(Type = params_dict["type"], date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                        return_data = dict()
                        return_data["country"] = params_dict["country"]
                        return_data["province"] = params_dict["province"]
                        return_data["detail"] = list()
                        for city_detail in data.values():
                            return_data["detail"].append({"name" : city_detail["city"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                        return json.dumps(return_data)
                    else:
                        if params_dict["country"] == "china":
                            # return the data of every province in the world of a particular day
                            data = db_.barchart(Type = params_dict["type"], date = params_dict["date"], country = params_dict["country"])
                            return_data = dict()
                            return_data["country"] = params_dict["country"]
                            return_data["detail"] = list()
                            for city_detail in data.values():
                                return_data["detail"].append({"name" : city_detail["province"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                            return json.dumps(return_data)
                        else:
                            return json.dumps({"code":0, "message":"失败"})
                else:
                    # return the data of every country in the world of a particular day
                    data = db_.barchart(Type = params_dict["type"], date = params_dict["date"])
                    return_data = dict()
                    return_data["detail"] = list()
                    for city_detail in data.values():
                        return_data["detail"].append({"name" : city_detail["country"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                    return json.dumps(return_data)
                
            elif params_dict["type"] == "accumulated":
                # get accumulated data
                if "country" in params_dict.keys():
                    if "province" in params_dict.keys():
                        # return the data of every city in the province of a particular day
                        data = db_.barchart(Type = params_dict["type"], date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                        return_data = dict()
                        return_data["country"] = params_dict["country"]
                        return_data["province"] = params_dict["province"]
                        return_data["detail"] = list()
                        for city_detail in data.values():
                            return_data["detail"].append({"name" : city_detail["city"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                        return json.dumps(return_data)
                    else:
                        if params_dict["country"] == "china":
                            # return the data of every province in the world of a particular day
                            data = db_.barchart(Type = params_dict["type"], date = params_dict["date"], country = params_dict["country"])
                            return_data = dict()
                            return_data["country"] = params_dict["country"]
                            return_data["detail"] = list()
                            for city_detail in data.values():
                                return_data["detail"].append({"name" : city_detail["province"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                            return json.dumps(return_data)
                        else:
                            return json.dumps({"code":0, "message":"失败"})
                else:
                    # return the data of every country in the world of a particular day
                    data = db_.barchart(Type = params_dict["type"], date = params_dict["date"])
                    return_data = dict()
                    return_data["detail"] = list()
                    for city_detail in data.values():
                        return_data["detail"].append({"name" : city_detail["country"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                    return json.dumps(return_data)
            else:
                ##################################################################
                # error param handling return a json explictly informs the error #
                ##################################################################
                return json.dumps({"code":0, "message":"失败"})
        else:
            return json.dumps({"code":0, "message":"失败"})
    except KeyError as e:
        print(e)
        return json.dumps({"code":0, "message":"失败"})






@application.route('/linechart_json/',methods=["GET"])
def linechart_json():
    try:
        db_ = db.database()
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)
        if "date" not in params_dict.keys() or "type" not in params_dict.keys():
            return json.dumps({{"code":0, "message":"失败"}})
        else:
            if params_dict["type"] == "someday":
                if params_dict["country"] == "china":
                    if "province" in params_dict.keys():
                        if "city" in params_dict.keys():
                            # return the data of specific city
                            data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"], province = params_dict["province"], city= params_dict["city"])
                            return_data = dict()
                            return_data["date"] = list()
                            return_data["detail"] = list()
                            for date_detail in data.values():
                                return_data["date"].append(date_detail["date"])
                                return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                            return json.dumps(return_data)
                        else:
                            # return the data of specific province
                            data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                            print(data)
                            return_data = dict()
                            return_data["date"] = list()
                            return_data["detail"] = list()
                            for date_detail in data.values():
                                return_data["date"].append(date_detail["date"])
                                return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                            return json.dumps(return_data)
                    else:
                        # return the data of china
                        data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"])
                        return_data = dict()
                        return_data["date"] = list()
                        return_data["detail"] = list()
                        for date_detail in data.values():
                            return_data["date"].append(date_detail["date"])
                            return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                        return json.dumps(return_data)
                else:
                    if "city" in params_dict.keys() or "province" in params_dict.keys():       
                        return json.dumps({"code":0, "message":"失败"})
                    
                    # return the data of specific country
                    data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"])
                    return_data = dict()
                    return_data["date"] = list()
                    return_data["detail"] = list()
                    for date_detail in data.values():
                        return_data["date"].append(date_detail["date"])
                        return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                    return json.dumps(return_data)
            elif params_dict["type"] == "accumulated":
                if params_dict["country"] == "china":
                    if "province" in params_dict.keys():
                        if "city" in params_dict.keys():
                            # return the data of specific city
                            data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"], province = params_dict["province"], city= params_dict["city"])
                            return_data = dict()
                            return_data["date"] = list()
                            return_data["detail"] = list()
                            for date_detail in data.values():
                                return_data["date"].append(date_detail["date"])
                                return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                            return json.dumps(return_data)
                        else:
                            # return the data of specific province
                            data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                            return_data = dict()
                            return_data["date"] = list()
                            return_data["detail"] = list()
                            for date_detail in data.values():
                                return_data["date"].append(date_detail["date"])
                                return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                            return json.dumps(return_data)
                    else:
                        # return the data of china
                        data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"])
                        return_data = dict()
                        return_data["date"] = list()
                        return_data["detail"] = list()
                        for date_detail in data.values():
                            return_data["date"].append(date_detail["date"])
                            return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                        return json.dumps(return_data)
                else:
                    if "city" in params_dict.keys() or "province" in params_dict.keys():       
                        return json.dumps({"code":0, "message":"失败"})
                    else: 
                        # return the data of specific country
                        data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"])
                        return_data = dict()
                        return_data["date"] = list()
                        return_data["detail"] = list()
                        for date_detail in data.values():
                            return_data["date"].append(date_detail["date"])
                            return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                        return json.dumps(return_data)
            else:
                return json.dumps({"code":0, "message":"失败"})
    except KeyError as e:
        print(e)
        return json.dumps({"code":0, "message":"失败"})





@application.route('/barchart_json/',methods=["GET"])
def barchart_json():
    try:
        db_ = db.database()
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)

        if "type" in params_dict.keys() and "date" in params_dict.keys():
            if params_dict["type"] == "someday":
                # get someday data
                if "country" in params_dict.keys():
                    if "province" in params_dict.keys():
                        # return the data of every city in the province of a particular day
                        data = db_.barchart(Type = params_dict["type"], date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                        return_data = dict()
                        return_data["country"] = params_dict["country"]
                        return_data["province"] = params_dict["province"]
                        return_data["detail"] = list()
                        for city_detail in data.values():
                            return_data["detail"].append({"name" : city_detail["city"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                        return json.dumps(return_data)
                    else:
                        if params_dict["country"] == "china":
                            # return the data of every province in the world of a particular day
                            data = db_.barchart(Type = params_dict["type"], date = params_dict["date"], country = params_dict["country"])
                            return_data = dict()
                            return_data["country"] = params_dict["country"]
                            return_data["detail"] = list()
                            for city_detail in data.values():
                                return_data["detail"].append({"name" : city_detail["province"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                            return json.dumps(return_data)
                        else:
                            return json.dumps({"code":0, "message":"失败"})
                else:
                    # return the data of every country in the world of a particular day
                    data = db_.barchart(Type = params_dict["type"], date = params_dict["date"])
                    return_data = dict()
                    return_data["detail"] = list()
                    for city_detail in data.values():
                        return_data["detail"].append({"name" : city_detail["country"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                    return json.dumps(return_data)
                
            elif params_dict["type"] == "accumulated":
                # get accumulated data
                if "country" in params_dict.keys():
                    if "province" in params_dict.keys():
                        # return the data of every city in the province of a particular day
                        data = db_.barchart(Type = params_dict["type"], date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                        return_data = dict()
                        return_data["country"] = params_dict["country"]
                        return_data["province"] = params_dict["province"]
                        return_data["detail"] = list()
                        for city_detail in data.values():
                            return_data["detail"].append({"name" : city_detail["city"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                        return json.dumps(return_data)
                    else:
                        if params_dict["country"] == "china":
                            # return the data of every province in the world of a particular day
                            data = db_.barchart(Type = params_dict["type"], date = params_dict["date"], country = params_dict["country"])
                            return_data = dict()
                            return_data["country"] = params_dict["country"]
                            return_data["detail"] = list()
                            for city_detail in data.values():
                                return_data["detail"].append({"name" : city_detail["province"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                            return json.dumps(return_data)
                        else:
                            return json.dumps({"code":0, "message":"失败"})
                else:
                    # return the data of every country in the world of a particular day
                    data = db_.barchart(Type = params_dict["type"], date = params_dict["date"])
                    return_data = dict()
                    return_data["detail"] = list()
                    for city_detail in data.values():
                        return_data["detail"].append({"name" : city_detail["country"], "confirmed" : city_detail["confirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                    return json.dumps(return_data)
            else:
                ##################################################################
                # error param handling return a json explictly informs the error #
                ##################################################################
                return json.dumps({"code":0, "message":"失败"})
        else:
            return json.dumps({"code":0, "message":"失败"})
    except KeyError as e:
        print(e)
        return json.dumps({"code":0, "message":"失败"})




# the above is correctly structured
# the following has not been correctly structured yet

@application.route('/login/', methods=['GET'])
def login():
    if request.method == 'GET':
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)
        if valid_login(params_dict['username'], params_dict['password']):
            return json.dumps({"code":1, "message":"成功"})
        else:
            return json.dumps({"code":0, "message":"失败"})
    else:
        return json.dumps({"code":0, "message":"失败"})

def valid_login(username, password):
    db_ = db.database()
    return db_.login(username, password)


@application.route('/data_update/', methods=['POST'])
def data_update():
    db_ = db.database()
    if request.method == 'POST':
        data = json.dumps(request.get_json())
        print(data)
        try:
            data = data["data"]
            for piece in data:
                year = piece["date"]["year"]
                month = piece["date"]["month"]
                day = piece["date"]["day"]
                area = piece["area"]# a dict with key country, maybe province and city
                detail = piece["datail"]# a dict with key "confirmed", "deaths", "recovered"
                
                date = str(year) + '-' + str(month) + '-' + str(day)
            if db_.update(date, area, detail):
                return json.dumps({"code":1, "message":"成功"})
            else:
                return json.dumps({"code":0, "message":"失败"})
        except Exception as e:
            print(e)
            return json.dumps({"code":0, "message":"失败"})
        
    
    else:
        return json.dumps({"code" : 0, "message":"失败"})


@application.route('/register/', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            print("get username and password")
            username = request.form['username']
            password = request.form['password']
            print("start registering")
            if register_(username, password):
                return json.dumps({"code":1, "message":"成功"})
            else:
                print("fail to register")
                return json.dumps({"code":0, "message":"失败"})
        except Exception as e:
            print(e)
            print("exception occurs")
            return json.dumps({"code":0, "message":"失败"})
    else:
        return json.dumps({"code":0, "message":"失败"})


def register_(username, password):
    db_ = db.database()
    return db_.register(username, password)
if __name__ == "__main__":
    application.run(host='0.0.0.0')  