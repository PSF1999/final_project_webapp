from dotenv import load_dotenv
import os
import requests
load_dotenv()


def getBatsmenStats(name):
    key = os.getenv("KEY")
    r1 = requests.get("https://cricapi.com/api/playerFinder?apikey="+key+"&name="
+name)
    data1 = r1.json()
    if len(data1['data']) == 0:
        return -1
    pid = data1['data'][0]['pid']
    r2 = requests.get("https://cricapi.com/api/playerStats?apikey="+key+"&pid="+str(pid))
    data2 = r2.json()['data']['batting']
    sr = data2['T20Is']['SR']
    return sr

def getBowlerStats(name):
    key = os.getenv("KEY")
    r1 = requests.get("https://cricapi.com/api/playerFinder?apikey="+key+"&name="
+name)
    data1 = r1.json()
    if len(data1['data']) == 0:
        return -1
    pid = data1['data'][0]['pid']
    r2 = requests.get("https://cricapi.com/api/playerStats?apikey="+key+"&pid="+str(pid))
    data2 = r2.json()['data']['bowling']
    econ = data2['T20Is']['Econ']
    return econ

