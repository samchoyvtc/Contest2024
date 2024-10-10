import requests
import json
from setting import*
import GameMaster
import time

def server_get():

    url = 'http://localhost:8080/problem'
    
    headers = {
        'Procon-Token': 'token1',
    }
    
    while True:
        try:
            response = requests.get(url, headers=headers)
            match = response.json()
            width = match['board']['width']
        except:
            print("no")
            time.sleep(0.1)
        else:
            break   
    
    width = match['board']['width']
    height = match['board']['height']
    start = [[int(char) for char in item] for item in match['board']['start']]
    goal = [[int(char) for char in items] for items in match['board']['goal']]
    n = match['general']['n']
    patterns= match['general']['patterns']
    pattern_dict = {}
    for pattern in patterns:
        pattern_dict[f"{pattern['p']}"] = [[int(char) for char in items] for items in pattern['cells']]
    return width,height,start,goal,pattern_dict

def server_post(saved):
    url = 'http://localhost:8080/answer'
    
    headers = {
        'Content-Type': 'application/json',
        'Procon-Token': 'token1',
    }

    data = {
      "n":0,
      "ops":[ 
            ]
        }
    n = len(saved)
    data["n"] = n
    for long in range (n) :
        aa = saved[long]

        keys = ["p", "x", "y", "s"]
        data_dict = {key: val for key, val in zip(keys, aa)}

        data["ops"].append(data_dict)

    
    response = requests.post(url, headers=headers, json=data)
    match = response.json()


