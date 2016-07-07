import requests
import pandas as pd
import json
from pandas.io.json import json_normalize
import sqlite3 as lite
import numpy as np

from sqlalchemy import create_engine
sqlite_file = 'sqlite://///Users/Kruthika/Projects/DDL/04-team3/census.db'
engine = create_engine(sqlite_file)
from pandas.io import sql
home_work=pd.read_sql_table('home_work', engine)
#df=home_work.iloc[751:]
df=home_work

from time import sleep

count=0
for index, row in df.iterrows():
    #print row['home_lat'], row['home_lon'], row['work_lat'], row['work_lon']
    source_lat = row['home_lat']
    source_lon = row['home_lon']
    dest_lat= row['work_lat']
    dest_lon= row['work_lon']
    
    headers = {
        'key':'AIzaSyAUlQnrcpJkb8u6xmL2UuHyPFD5CxWdLPo'
    }
    
    params = {
    # Request parameters
    #'origin': source_lat+','+source_lon,
    #'destination':dest_lat+','+dest_lon,
    'origin': dest_lat+','+dest_lon,
    'destination':source_lat+','+source_lon,
    'alternatives':'false',
    'mode':'car',
    'traffic_model':'optimistic',
    'departure_time':'now'
    }
    
    r = requests.get('https://maps.googleapis.com/maps/api/directions/json?', params=params, headers=headers)
    
    if len(r.json()['routes']) != 0:
        if len(json_normalize(r.json()['routes'][0]['legs'][0])) != 0:
            df=json_normalize(r.json()['routes'][0]['legs'][0])
            df1=df.drop(['steps','traffic_speed_entry','via_waypoint'], axis=1)
            df1['unique_id']=source_lat+'_'+source_lon+'_'+dest_lat+'_'+dest_lon


            df1.to_sql('car_info', engine,if_exists='append')
        else:
            continue
    else:
        continue
    count += 1
    print 'Latitude and longitude count value - ',count
    print 'Source and destination pair - ', source_lat, source_lon, dest_lat, dest_lon
    
print "Successful data collection!"

