#candy aigle noir
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import requests
import json
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(('/g'))

@app.route('/g')
def gintoki():
   
    dict_rig = {}
    dict_rig_number = {
                       1: "201", 
                       2: "202",
                       3: "203",
                       4: "204"}
    list_hashrate = []
    
    for x,y, in dict_rig_number.items():
        try:
            response = requests.get("http://ripmundocrit.ddns.net:{0}/API.json".format(y), timeout=4)
            response_json = json.loads(response.text)
            uptime = response_json["results"]["avg_time"] * response_json["results"]["shares_good"]
            dict_rig[x] = dict()
            dict_rig[x].update({"hashrate": response_json["hashrate"]["total"][1]})
            dict_rig[x].update({"avg_time": response_json["results"]["avg_time"]})
            dict_rig[x].update({"uptime": "{0}:{1:0>2}:{2:0>2}".format(int(uptime//3600), int(uptime//60%60), int(uptime%60))})
            dict_rig[x].update({"url": "http://ripmundocrit.ddns.net:{0}/r".format(dict_rig_number[x])})
            list_hashrate.append(dict_rig[x]["hashrate"])

        except requests.exceptions.RequestException:
            dict_rig[x] = dict()
            dict_rig[x].update({"avg_time": "rig down."})
            dict_rig[x].update({"hashrate": "rig down."})
            dict_rig[x].update({"uptime": "rig down."})

    total_hashrate = sum(list_hashrate)
            
    return render_template('gintoki.html', dict_rig=dict_rig, total_hashrate=total_hashrate)
    

@app.route('/s')
def shinpachi():
        return render_template('shinpachi.html')

@app.route('/k')
def kagura():
    if not session.get('logged_in'):
        return redirect('/log')
    else:
        return render_template('kagura.html')

@app.route('/log')
def log() :
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return kagura()

@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return kagura()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=1000, host='0.0.0.0',)



