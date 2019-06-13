import json
import sys
data = json.loads(open('swiss3.json').read())


with open('swiss18.json', 'r') as f:
    itero = json.load(f)
    distros_dict =  itero.copy()
#print(distros_dict["features"][2225])
for i,mcp in enumerate(itero["features"]):
    if mcp["properties"]["shapeid"] == sys.argv[1]:
      distros_dict["features"][i]["properties"]["shapeid"] = sys.argv[2]
      print(distros_dict["features"][i]["properties"])

with open('swiss18.json', 'w') as outfile:
    json.dump(distros_dict, outfile)