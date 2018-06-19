from datetime import datetime
import time
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, jsonify
import requests
import json
import os
from urllib.request import Request, urlopen
from lxml import etree

app = Flask(__name__)


@app.route('/')
def home():

    return redirect(('/g'))


def jason(url):

    return json.loads(requests.get(url).text)


def virgule(amount, index):

    return float(f"{str(amount)[:-index]}.{str(amount)[-index:]}")


def renard():

    url = 'http://free.currencyconverterapi.com/api/v5/convert?q=EUR_USD&compact=y'
    eur_usd = jason(url)["EUR_USD"]["val"]

    dict_coin_all = {
                'etn': {
                        'coinmarketcap': 'https://api.coinmarketcap.com/v2/ticker/2137/',
                        'hashvault': 'https://electroneum.hashvault.pro/api/network/stats'
                    },
                'graft': {
                        'coinmarketcap': 'https://api.coinmarketcap.com/v2/ticker/2571/',
                        'hashvault': 'https://graft.hashvault.pro/api/network/stats'
                    },
                'btc': {
                        'coinmarketcap': 'https://api.coinmarketcap.com/v2/ticker/1/'
                    }
            }

    dict_coin_values = {
                'etn': {},
                'graft': {},
                'btc': {}
            }

    for k, v in dict_coin_all.items():
        for _, v2 in v.items():
            if 'coinmarketcap' in _:
                url = v2
                response_json = jason(url)
                dict_coin_values[k].update({
                    'price_usd': response_json['data']['quotes']['USD']['price'],
                    'price_eur': response_json['data']['quotes']['USD']['price']/eur_usd,
                    'percent_change_1h': response_json['data']['quotes']['USD']['percent_change_1h'],
                    'percent_change_24h': response_json['data']['quotes']['USD']['percent_change_24h'],
                    'percent_change_7d': response_json['data']['quotes']['USD']['percent_change_7d'],
                })
            else:
                url = v2 
                response_json = jason(url)
                dict_coin_values[k].update({'difficulty': response_json['difficulty']/120})
                if 'graft' in k: dict_coin_values[k].update({'block_reward': virgule(response_json['value'], 10)})
                elif 'etn' in k: dict_coin_values[k].update({'block_reward': virgule(response_json['value'], 2)})
            
    return dict_coin_values


def kultur():

    dict_wallet_values = {
            'etn': {
                    'payment': 'https://api.nanopool.org/v1/etn/paymentsday/etnk3DMAGRrEUaWweAw2zr4HBwgar9tjfHabe4a466KnSiMx2wBZ5tPBLm3NHg9uEzR39CjkZzUEq6Qss2bZux3v23VjvKf549',
                    'balance': 'https://api.nanopool.org/v1/etn/balance_hashrate/etnk3DMAGRrEUaWweAw2zr4HBwgar9tjfHabe4a466KnSiMx2wBZ5tPBLm3NHg9uEzR39CjkZzUEq6Qss2bZux3v23VjvKf549'
                },
            'graft': {
                    'payment': 'https://graft.hashvault.pro/api/miner/GDacvVUHegbPmB9Z9Db4uJPRqDCGz9kbzSBuNM89bhdxYhz1qQnHrBrfHXJF2BorVS9aeBffnwgPMQUyEgvw8zvvVEY4v6j/payments?page=0&limit=30',
                    'balance': 'https://graft.hashvault.pro/api/miner/GDacvVUHegbPmB9Z9Db4uJPRqDCGz9kbzSBuNM89bhdxYhz1qQnHrBrfHXJF2BorVS9aeBffnwgPMQUyEgvw8zvvVEY4v6j/stats'
                }
            }

    response = jason(dict_wallet_values['etn']['payment']) 
    etn_payment = sum([payment['amount'] for payment in response['data']])
        
    response = jason(dict_wallet_values['graft']['balance']) 
    graft_balance = virgule(response['amtDue'], 10)

    response = jason(dict_wallet_values['graft']['payment']) 
    graft_payment = sum([virgule(payment['amount'], 10) for payment in response if payment['ts'] > int(time.time())-86400])

    dict_wallet_all = {
            'etn': {
                    'payment': etn_payment,
                    'balance': jason(dict_wallet_values['etn']['balance'])['data']['balance']
                },
            'graft': {
                    'payment': graft_payment,
                    'balance': graft_balance
                }
          }

    print('\n... dict_wallet_all:', dict_wallet_all)

    return dict_wallet_all
    
kultur()


def butterfly():

    dict_rig = {}
    dict_rig_number = {
                       1: "201", 
                       2: "202",
                       3: "203",}
    dict_pool_int = {"etn": 1, "graft": 2}
    list_hashrate = []

    for x, y in dict_rig_number.items():
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

            for key in dict_pool_int.keys():
                if key in dict_rig[x]["pool"]:
                    dict_rig[x].update({"coin": dict_pool_int[key]})

            list_hashrate.append(dict_rig[x]["hashrate"])

        except requests.exceptions.RequestException:
            dict_rig[x] = dict()
            list_key = ["avg_time", "hashrate", "uptime", "pool", "url", "coin"]
            for key in list_key:
                dict_rig[x].update({key: "rig down."})

    total_hashrate = round(sum(list_hashrate), 1)

    dict_rig1 = {}
    dict_rig1_number = {
                       #1: "301",
                       #2: "302",
                       }
    list_hashrate1 = []

    for x, y in dict_rig1_number.items():
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
            list_key = ["avg_time", "hashrate", "uptime", "pool", "url"]
            for key in list_key:
                dict_rig1[x].update({key: "rig down."})

    total_hashrate1 = round(sum(list_hashrate1), 1)

    site= "https://www.cryptunit.com/?order=price1h&?filter=all"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    response = urlopen(req)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    list_coin =  ['electroneum', 'graft']
    dict_coin = {}
    dict_formula = {} 
    response = requests.get("http://free.currencyconverterapi.com/api/v5/convert?q=EUR_USD&compact=y", timeout=4)
    response_json = json.loads(response.text)

    for coin in list_coin:
        list_values = tree.xpath(f'//div[@class="{coin}"]//ul/li/a/label/text()')
        dict_coin.update({coin: {
            "price": float(list_values[0]) / response_json["EUR_USD"]["val"],
            "hashrate": float(list_values[3])*1000000,
            "reward": float(list_values[4])
        }}) 
        profitability = (total_hashrate/dict_coin[coin]["hashrate"]) * dict_coin[coin]["reward"] * dict_coin[coin]["price"] * 720
        dict_formula.update({coin: profitability})

    coin_to_mine = max(dict_formula, key=lambda key: dict_formula[key])
    dict_coin_int = {"electroneum": 1, "graft": 2}
    coin_to_mine = dict_coin_int[coin_to_mine]

    print("\n... dict_rig here:", dict_rig)
    print("\n... dict_coin here:", dict_coin)
    print("\n... dict_formula here:", dict_formula)
    print("\n... coin_to_mine:", coin_to_mine)

    dict_all = {
            'dict_rig': dict_rig,
            'dict_rig1': dict_rig1,
            'total_hashrate': total_hashrate,
            'total_hashrate1': total_hashrate,
            'dict_coin': dict_coin,
            'coin_to_mine': coin_to_mine,
            'dict_formula': dict_formula,
            'dict_rig_number': dict_rig_number
            }
    return dict_all


@app.route('/g')
def gintoki():

    dict_all = butterfly()

    return render_template('gintoki.html', 
                            dict_rig=dict_all['dict_rig'], 
                            dict_rig1=dict_all['dict_rig1'],
                            total_hashrate1=dict_all['total_hashrate1'], 
                            total_hashrate=dict_all['total_hashrate'], 
                            dict_coin=dict_all['dict_coin'], 
                            coin_to_mine = dict_all['coin_to_mine'], 
                            dict_formula=dict_all['dict_formula'],
                            dict_rig_number=dict_all['dict_rig_number'])


@app.route('/api', methods=['GET'])
def get_miner ():

    dict_all = butterfly()
    dict_rig = dict_all['dict_rig']
    coin_to_mine = dict_all['coin_to_mine']
    dict_rig_number = dict_all['dict_rig_number']
    dict_coin = {
            '1' : "Electroneum",
            '2' : "Graft"
            }
    dict_result = {}
    for rig in dict_rig_number.keys():
        dict_result.update({f'A{rig}': {
            'switch': 1 if coin_to_mine != dict_rig[rig]["coin"] and isinstance(dict_rig[rig]["coin"], int) else 0,
            'coin_to_mine': coin_to_mine,
            'coin_current': dict_rig[rig]["coin"]
            }})

    return jsonify({'Coin': dict_coin},{'dict_result': dict_result})

#dict_rig[x].update({"temperature": [device["temperature"] for device in response_json["devices"]]})

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=1000, host='0.0.0.0', threaded=True)



