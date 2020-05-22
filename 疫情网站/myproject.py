# -*- coding: UTF-8 -*- 

from flask_cors import *
import db
import json
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import pandas as pd
import numpy as np
import datetime
UPLOAD_FOLDER = '/home/myproject/uploaddata'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])
application = Flask(__name__)
CORS(application, supports_credentials = True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_data/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            postfix = file.filename.rsplit('.', 1)[1]
            filename = secure_filename(file.filename)
            addr = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            file.save(addr)
            if load_in_db(addr, postfix):
                return json.dumps({"code":1, "message":"成功"})
    return json.dumps({"code":0, "message":"失败"})

def _time_helper(date):
    date = date.split('/')
    for i in range(len(date)):
        date[i] = int(date[i])
    year, month, day = date
    return datetime.date(year, month, day).isoformat()
def load_in_db(file, postfix):
    headers = ["date", "country", "province", "city", "confirmed", "cured", "death"]
    db_ = db.database()
    if postfix == "csv":
        f = pd.read_csv(file)
    else:
        f = pd.read_excel(file)
    for i in range(f.shape[0]):
        if not db_.upload(_time_helper(f.loc[i][headers[0]]), f.loc[i][headers[1]], f.loc[i][headers[2]], f.loc[i][headers[3]], f.loc[i][headers[4]], f.loc[i][headers[5]], f.loc[i][headers[6]]):
            return False
    return True

@application.route('/download_data/',methods=["GET"])
def request_for_data_handle():
    try:
        db_ = db.database()
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)
        file_name = 'a'+ str(hash(str(params_dict)))
        addr = "/home/myproject/cache/" + file_name + ".csv"
        if check_cache(addr):
            download_file(file_name + ".csv")
        else:
            db_.request_for_csv(params_dict, addr)
            download_file(file_name + ".csv")
    except Exception as e:
        print("error occurs")
        print(e)
def check_cache(addr):
    return os.path.exists(addr)

def download_file(filename):
    return send_from_directory("/home/myproject/cache", filename, as_attachment=True)


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

@application.route('/login/', methods=['POST', "OPTIONS"])
def login():
    if request.method == 'POST':
        print("get username and password")
        username = request.json['username']
        password = request.json['password']
        if valid_login(username, password):
            return json.dumps({"code":1, "message":"成功"})
        else:
            return json.dumps({"code":0, "message":"失败"})
    else:
        return json.dumps({"code":0, "message":"失败"})

def valid_login(username, password):
    db_ = db.database()
    return db_.login(username, password)


@application.route('/data_update/', methods=['POST', "OPTIONS"])
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


@application.route('/register/', methods=['POST', "OPTIONS"])
def register():
    if request.method == 'POST':
        try:
            print("get username and password")
            username = request.json['username']
            password = request.json['password']
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


@application.route('/data_upload/', methods=['POST', "OPTIONS"])
def register():
    if request.method == 'POST':
        db_ = db.database()
        try:
            print("get data")
            date = request.json['date']
            country = request.json['country']
            province = request.json['province']
            city = request.json['city']
            confirmed = request.json['confirmed']
            cured = request.json['cured']
            death = request.json['death']
            print("start writing")
            if db_.upload(date, country, province, city, confirmed, cured, death):
                return json.dumps({"code":1, "message":"成功"})
            else:
                print("fail to write in ")
                return json.dumps({"code":0, "message":"失败"})
        except Exception as e:
            print(e)
            print("exception occurs")
            return json.dumps({"code":0, "message":"失败"})
    else:
        return json.dumps({"code":0, "message":"失败"})
if __name__ == "__main__":
    application.run(host='0.0.0.0')  