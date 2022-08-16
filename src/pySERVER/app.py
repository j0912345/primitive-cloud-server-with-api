from time import time
from tokenize import Triple
from flask import Flask, jsonify, render_template, request, make_response, Response, redirect
import sys
import json
import secrets as secr
from os import path as osPath
from requests import get as HTTPgetREQ
import random as rand

def key_stuff(app, json_name=f"{__file__}/../key_dont_share_with_others.json", json_base_data = {"WARNING!!": "do NOT share this file, it has a secret key inside"}):
    if not osPath.exists(json_name):
        json_base_data["secret_key"] = secr.token_urlsafe(1024)
        with open(json_name, "w") as jf:
            jf.write(json.dumps(json_base_data))
    else:
        with open(json_name, "r") as jf:
            app.config["SECRET_KEY"] = json.loads(jf.read())["secret_key"]

app = Flask(__name__)
key_stuff(app=app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"


# cookie stuff
def get_uid_cookie(req):
    print(request.cookies.get("user_api_id"))
    if request.cookies.get("user_api_id") != None:
        return request.cookies.get("user_api_id")
    else:
        seed = good_random()
        uid = create_long_random_string(seed)
        print(uid)
        return uid


# helpful functions
# 512 because that looks like the cookie size limit
def create_long_random_string(seed, leng=512):
    rand.seed(seed)
    rand_string = ""
    char_list = "1234567890!$#%^&*()_-=+[]{}\\|*/;:'\"<>,.?`~qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    char_list_len = len(char_list)-1
    for i in range(0, leng):
        rand_string += char_list[rand.randint(0, char_list_len)]
    return rand_string


def good_random():
    respon = HTTPgetREQ("https://www.random.org/integers/?num=1&max=100000000&min=0&col=1&base=10&format=plain&rnd=new")
    statcode = respon.status_code
    if statcode >= 400 and statcode < 500:
        print(f"couldn't get random.org data. error:\n{respon.text}")
        return secr.randbelow(100_000_000)
    else:
        return respon.text


# views
@app.route("/")
def index_page():
    return render_template("/index.html")

@app.route("/get_user_id")
def cookie_page():
    cookie = 'click the button to get the id'
    args = request.args

    if args.get('get_uid'):
        cookie = get_uid_cookie(request)
        resp = make_response(render_template("get_user_id.html", c_uid=cookie))
        resp.set_cookie('user_api_id', cookie, expires=32523383054)
    
        return resp
    return render_template("get_user_id.html", c_uid=cookie)


@app.route("/generate_api_keys", methods=["get", "post"])
def gen_api_keys_page():
    if request.method.lower() == "post":
        api_key_file = __file__+"/../../../api_keys/test.txt"
#        with open(api_key_file, "w") as tf:
#            tf.write("TEST TEXT STRING")
        args = request.args
        print(args)
        print(request.form.to_dict(flat=False))
        print(request.data)
        if args.get('gen_key') and args.get('gen_key') == "true":
            pass

    return render_template("generate_api_keys.html")

argv = sys.argv
if __name__ == '__main__' or (len(argv) > 2 and argv[2] == True):
    server_port = 8003
    # boiled plate code
    # (boilerplate code)
    if len(argv) > 1:
        server_port = argv[1]
        
    app.run(debug=True, port=server_port, host='0.0.0.0')
