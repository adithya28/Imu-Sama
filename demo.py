import json
import itertools


with open("gamedata.json", "r") as game_data:
    data = json.load(game_data)

list1=data["Admin"]
data1=dict()
data1=list1[0]
data1['Charlist']={"Goku","Vegeta","Trunks"}
print(data)

with open("gamedata.json","a") as wmode:
    json.dumps(data)

    