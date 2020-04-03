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
        print(params_dict)
        if params_dict["type"] == "someday":
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
            pass
            ##################################################################
            # error param handling return a json explictly informs the error #
            ##################################################################
        return """hello world"""

    except KeyError as e:
        print(e)


@app.route('/linechart_json/',methods=["GET"])
def linechart_json():
    try:
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)
        if "city" in params_dict.keys():
            pass
            ###########################
            # need to complete
            ##########################
        else if "province" in params_dict.keys():
            pass
            ###########################
            # need to complete
            ##########################
        else if "country" in params_dict.keys():
            pass
            ###########################
            # need to complete
            ##########################
        else:
            pass
            ##################################################################
            # error param handling return a json explictly informs the error #
            ##################################################################
    except KeyError as e:
        print(e)

@app.route('/barchart_json/',methods=["GET"])
def barchart_json():
    try:
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)
        if "province" in params_dict.keys():
            pass
            #############################################
            # return the data of cities in the province #
            #############################################
        else if "country" in params_dict.keys():
            pass
            ###############################################
            # return the data of provinces in the country #
            ###############################################
        else:
            pass
            ###############################################
            # return the data of countries in the globe   #
            ###############################################
    except KeyError as e:
        print(e)

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