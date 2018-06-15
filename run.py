#candy aigle noir
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import requests
import json
import os
from urllib.request import Request, urlopen
from lxml import etree
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
                       3: "203",}
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
            dict_rig[x].update({"pool" : response_json["connection"]["pool"]})
            dict_rig[x].update({"url": "http://ripmundocrit.ddns.net:{0}/r".format(dict_rig_number[x])})
            list_hashrate.append(dict_rig[x]["hashrate"])

        except requests.exceptions.RequestException:
            dict_rig[x] = dict()
            list_key = ["avg_time", "hashrate", "uptime", "pool"]
            for key in list_key:
                dict_rig[x].update({key: "rig down."})

    total_hashrate = round(sum(list_hashrate),1)

    dict_rig1 = {}
    dict_rig1_number = {
                       1: "301",
                       2: "302",
                       }
    list_hashrate1 = []
    
    for x,y, in dict_rig1_number.items():
        try:
            response = requests.get("http://ripmundocrit.ddns.net:{0}/API.json".format(y), timeout=4)
            response_json = json.loads(response.text)
            uptime = response_json["results"]["avg_time"] * response_json["results"]["shares_good"]
            dict_rig1[x] = dict()
            dict_rig1[x].update({"hashrate": response_json["hashrate"]["total"][1]})
            dict_rig1[x].update({"avg_time": response_json["results"]["avg_time"]})
            dict_rig1[x].update({"uptime": "{0}:{1:0>2}:{2:0>2}".format(int(uptime//3600), int(uptime//60%60), int(uptime%60))})
            dict_rig1[x].update({"pool" : response_json["connection"]["pool"]})
            dict_rig1[x].update({"url": "http://ripmundocrit.ddns.net:{0}/r".format(dict_rig1_number[x])})
            list_hashrate1.append(dict_rig1[x]["hashrate"])

        except requests.exceptions.RequestException:
            dict_rig1[x] = dict()
            list_key = ["avg_time", "hashrate", "uptime", "pool"]
            for key in list_key:
                dict_rig1[x].update({key: "rig down."})

    total_hashrate1 = round(sum(list_hashrate1),1)

    site= "https://www.cryptunit.com/?order=price3h"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    response = urlopen(req)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    list_coin =  ['electroneum', 'graft']
    dict_coin = {}
 
    for coin in list_coin:
        list_values = tree.xpadth(f'//div[@class="{coin}"]//ul/li/a/label/text()')
        dict_coin.update("coin": coin)
        dict_coin.update("price": list_values[0])
        dict_coin.update("hashrate": list_values[3])
        dict_coin.update("reward": list_values[4])

    return render_template('gintoki.html', dict_rig=dict_rig, dict_rig1=dict_rig1, total_hashrate1=total_hashrate1, total_hashrate=total_hashrate, dict_coin=dict_coin)

#dict_rig[x].update({"temperature": [device["temperature"] for device in response_json["devices"]]})

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=1000, host='0.0.0.0', threaded=True)



