###Python Code to Pull WMATA API Station Entrances and Save to JSON File###

import urllib3
import json

#api_key = fb7119a0d3464673825a26e94db74451

url = "https://api.wmata.com/Rail.svc/json/jStationEntrances?api_key=fb7119a0d3464673825a26e94db74451"

connection_pool = urllib3.PoolManager()
json_obj = connection_pool.request('GET', url )

data = json.loads(json_obj.data)

# Writing JSON data
with open('metrostationentrance.json', 'w') as f:
     json.dump(data, f)
