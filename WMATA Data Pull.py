
# coding: utf-8

# In[1]:

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
from urllib2 import urlopen


# In[2]:

#Get station-level descriptive data from WMATA API, including latitude and longitude of stations and line codes


# In[3]:

r = requests.get('https://api.wmata.com/Rail.svc/json/jStations?api_key=fb7119a0d3464673825a26e94db74451')


# In[4]:

r.json()


# In[6]:

data_list = []
for entrances in r.json()['Stations']:
    for e in entrances.keys():
        if e not in data_list:
            data_list.append(e)
print data_list


# In[7]:

df = json_normalize(r.json()['Stations'])
df.head(5)


# In[8]:

df.to_csv('stations.csv')


# In[9]:

#Get bus route descriptive data from WMATA API, including latitude and longitude of stations and route codes


# In[10]:

r1 = requests.get('https://api.wmata.com/Bus.svc/json/jStops?api_key=fb7119a0d3464673825a26e94db74451')


# In[11]:

r1.json()


# In[12]:

r1.json().keys()


# In[13]:

r1.json()['Stops']


# In[14]:

stops_list = []
for stops in r1.json()['Stops']:
    for s in stops.keys():
        if s not in stops_list:
            stops_list.append(s)
print stops_list


# In[15]:

df1 = json_normalize(r1.json()['Stops'])
df1.head(5)


# In[16]:

#Get path-level train  data from WMATA API, including latitude and longitude of stations and line codes


# In[17]:

rblue = requests.get('https://api.wmata.com/Rail.svc/json/jPath?FromStationCode=J03&ToStationCode=G05&api_key=fb7119a0d3464673825a26e94db74451')
rgreen = requests.get('https://api.wmata.com/Rail.svc/json/jPath?FromStationCode=F11&ToStationCode=E10&api_key=fb7119a0d3464673825a26e94db74451')
rorange = requests.get('https://api.wmata.com/Rail.svc/json/jPath?FromStationCode=K08&ToStationCode=D13&api_key=fb7119a0d3464673825a26e94db74451')
rred = requests.get('https://api.wmata.com/Rail.svc/json/jPath?FromStationCode=A15&ToStationCode=B11&api_key=fb7119a0d3464673825a26e94db74451')
rsilver = requests.get('https://api.wmata.com/Rail.svc/json/jPath?FromStationCode=N06&ToStationCode=G05&api_key=fb7119a0d3464673825a26e94db74451')
ryellow = requests.get('https://api.wmata.com/Rail.svc/json/jPath?FromStationCode=C15&ToStationCode=E06&api_key=fb7119a0d3464673825a26e94db74451')


# In[18]:

data_list = []
for paths in rblue.json()['Path']:
    for p in paths.keys():
        if p not in data_list:
            data_list.append(p)
print data_list

dfblue = json_normalize(rblue.json()['Path'])
dfgreen = json_normalize(rgreen.json()['Path'])
dforange = json_normalize(rorange.json()['Path'])
dfred = json_normalize(rred.json()['Path'])
dfsilver = json_normalize(rsilver.json()['Path'])
dfyellow = json_normalize(ryellow.json()['Path'])


# In[19]:

df2 = pd.concat([dfblue, dfgreen, dforange, dfred, dfsilver, dfyellow], ignore_index=True)


# In[20]:

df2.head(5)


# In[21]:

metro_combined = pd.merge(df2, df, how='left', left_on='StationCode', right_on='Code')


# In[22]:

metro_combined.head(5)


# In[25]:

metro_combined.to_csv('trainandroute.csv')


# In[ ]:



