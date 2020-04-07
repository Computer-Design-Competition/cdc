from flask import Flask
from flask import request
import db
import json
app = Flask(__name__)

@app.route("/hello/")
def hello():
    return "Hello world!"

@app.route('/hotspotmap_json/',methods=["GET"])
def hotspotmap_json():
    try:
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
                        # return the data of every city in the world of a particular day
                        pass
                    else:
                        if params_dict["country"] == "china":
                            # return the data of every province in the world of a particular day
                            pass
                        else:
                            return json.dumps({{"code":0, "message":"失败"}})
                else:
                    # return the data of every country in the world of a particular day
                    pass
                
                ###########################
                # need to complete
                ##########################
            else if params_dict["type"] == "accumulated":
                pass
                ###########################
                # need to complete
                ##########################
            else:
                ##################################################################
                # error param handling return a json explictly informs the error #
                ##################################################################
                return json.dumps({{"code":0, "message":"失败"}})
        else:
            return json.dumps({{"code":0, "message":"失败"}})
        

    except KeyError as e:
        print(e)
        return json.dumps({{"code":0, "message":"失败"}})


@app.route('/linechart_json/',methods=["GET"])
def linechart_json():
    try:
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)
        if "date" not in params_dict.keys():
            return json.dumps({{"code":0, "message":"失败"}})
        else:
            if "city" in params_dict.keys() and params_dict["country"] == "china":
                # return the data of specific city
                pass
            if "province" in params_dict.keys() and params_dict["country"] == "china":
                # return the data of specific province
                pass
                
            if "country" in params_dict.keys():
                # return the data of specific country
                pass
            else:
                return json.dumps({{"code":0, "message":"失败"}})
    except KeyError as e:
        print(e)
        return json.dumps({{"code":0, "message":"失败"}})





@app.route('/barchart_json/',methods=["GET"])
def barchart_json():
    try:
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)

        if "type" in params_dict.keys() and "date" in params_dict.keys():
            
            if "country" in params_dict.keys():
                if params_dict["country"] == "china":
                    if "province" not in params_dict.keys():
                        pass
                        ###############################################
                        # return the data of provinces in the country #
                        ###############################################
                    else:
                        #############################################
                        # return the data of cities in the province #
                        #############################################
                        pass
                else:
                    return json.dumps({{"code":0, "message":"失败"}})
            else:
                # return the data of every country in the world
                pass
        else:
            return json.dumps({{"code":0, "message":"失败"}})
    except KeyError as e:
        print(e)
        return json.dumps({{"code":0, "message":"失败"}})




# the above is correctly structured
# the following has not been correctly structured yet

@app.route('/login/', methods=['GET'])
def login():
    if request.method == 'GET':
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)
        if valid_login(params_dict['username'], params_dict['password']):
            return json.dumps({{"code":1, "message":"成功"}})
        else:
            return json.dumps({{"code":0, "message":"失败"}})
    else:
        return json.dumps({{"code":0, "message":"失败"}})

def valid_login(username, password):
    ################################
    # search in db to see if valid
    ###################################
    pass


@app.route('/data_update/', methods=['POST'])
def data_update():
    error = None
    if request.method == 'POST':
        data = json.dumps(request.get_json())
        try:
            data = data["data"]
            for piece in data:
                year = piece["date"]["year"]
                month = piece["date"]["month"]
                day = piece["date"]["day"]
                area = piece["area"]# a dict with key country, maybe province and city
                detail = piece["datail"]# a dict with key "confirmed", "deaths", "recovered", "male", "female", "age1", "age2"
                ######################################
                # insert into db
                #####################################
        except Exception as e:
            print(e)
            return json.dumps({{"code":0, "message":"失败"}})
        
    
    else:
        return json.dumps({"code" : 0, "message":"失败"})


@app.route('/register/', methods=['POST'])
def register():
    if request.method == 'POST':
        data = json.dumps(request.get_json())
        try:
            username = data['username']
            password = data['password']
        except Exception as e:
            print(e)
            json.dumps({{"code":0, "message":"失败"}})
        if register_(username, password):
            return json.dumps({{"code":1, "message":"成功"}})
        else:
            return json.dumps({{"code":0, "message":"失败"}})
    else:
        return json.dumps({{"code":0, "message":"失败"}})


def register_(username, password):
    pass
    #########################################
    # register in db, return True if succeed
    ###########################################

if __name__ == "__main__":
    app.run()