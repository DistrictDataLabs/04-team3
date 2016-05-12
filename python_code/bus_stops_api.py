###Python Code to Pull WMATA Bus Stops###

import urllib3
import json

#api_key = fb7119a0d3464673825a26e94db74451

url = "https://api.wmata.com/Bus.svc/json/jStops?api_key=fb7119a0d3464673825a26e94db74451"

connection_pool = urllib3.PoolManager()
json_obj = connection_pool.request('GET', url )

data = json.loads(json_obj.data)

print data

# Writing JSON data
with open('busstops.json', 'w') as f:
     json.dump(data, f)

	


