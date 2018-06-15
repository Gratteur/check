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

    total_hashrate = round(sum(list_hashrate), 1)

    dict_rig1 = {}
    dict_rig1_number = {
                       #1: "301",
                       #2: "302",
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

    total_hashrate1 = round(sum(list_hashrate1), 1)

    site= "https://www.cryptunit.com/?order=price3h"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    response = urlopen(req)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    list_coin =  ['electroneum', 'graft']
    dict_coin = {}
    for coin in list_coin:
        list_values = tree.xpath(f'//div[@class="{coin}"]//ul/li/a/label/text()')
        dict_coin.update({coin: {
            "price": float(list_values[0]),
            "hashrate": float(list_values[3])*1000000,
            "reward": float(list_values[4])
        }}) 

    dict_formula = {} 
    for coin in list_coin:
        dict_formula.update({coin: (total_hashrate/dict_coin[coin]["hashrate"]) *
                                    dict_coin[coin]["reward"] *
                                    dict_coin[coin]["price"] *
                                    720
                                    })

    coin_to_mine = max(dict_formula, key=lambda key: dict_formula[key])
    dict_coin_int = {"electroneum": 1, "graft": 2}
    coin_to_mine = dict_coin_int[coin_to_mine]

    print("\n... dict_coin here:", dict_coin)
    print("\n... dict_formula here:", dict_formula)
    print("\n... coin_to_mine:", coin_to_mine)

    return render_template('gintoki.html', dict_rig=dict_rig, dict_rig1=dict_rig1,
                            total_hashrate1=total_hashrate1, total_hashrate=total_hashrate, 
                            dict_coin=dict_coin, coin_to_mine = coin_to_mine)

#dict_rig[x].update({"temperature": [device["temperature"] for device in response_json["devices"]]})

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=1000, host='0.0.0.0', threaded=True)



