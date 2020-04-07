from flask import Flask
from flask import request
import db
import json
app = Flask(__name__)

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

@app.route('/login/', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)



@app.route('/data_update/', methods=['POST'])
def data_update():
    error = None
    if request.method == 'POST':
        request.form['data']
        
    
    else:
        error = "invalid method"
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    return json.dumps({"error":error})

if __name__ == "__main__":
    app.run()