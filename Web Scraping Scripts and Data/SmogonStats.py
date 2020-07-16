import requests
import json

linkLead = "https://www.smogon.com/stats/2019-12/chaos/gen8vgc2020-"
linkEnd = ".json"

for s in ["0", "1500", "1630", "1760"]:
    response = requests.get(linkLead + s + linkEnd)
    j = json.loads(response.text)

    f = open("SmogonData/smogon-" + s + ".txt", 'w')
    f.write(json.dumps(j, indent=4, sort_keys=True))
    f.close()