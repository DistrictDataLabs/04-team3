
# coding: utf-8

# In[3]:

import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import urllib
from StringIO import StringIO
import gzip


# In[4]:

#URL for primary LODES data set for 2014
url_lodes = 'http://lehd.ces.census.gov/data/lodes/LODES7/dc/od/dc_od_main_JT00_2014.csv.gz'
url_xwalk = 'http://lehd.ces.census.gov/data/lodes/LODES7/dc/dc_xwalk.csv.gz'
url_lat = 'http://www2.census.gov/geo/docs/maps-data/data/gazetteer/2014_Gazetteer/2014_Gaz_zcta_national.zip'

#Save files to active directory
urllib.urlretrieve(url_lodes,'dc_od_main_JT00_2014.csv.gz')
urllib.urlretrieve(url_xwalk,'dc_xwalk.csv.gz')
urllib.urlretrieve(url_xwalk,'2014_Gaz_zcta_national.zip')

#Unzip files to active directory
inF1 = gzip.open('dc_od_main_JT00_2014.csv.gz', 'rb')
inF2 = gzip.open('dc_xwalk.csv.gz', 'rb')
s1 = inF1.read()
s2 = inF2.read() 


# In[6]:

# Convert to data frame
dc_od_2014 = pd.read_csv(StringIO(s1))
dc_xwalk = pd.read_csv(StringIO(s2))

# Rename columns
dc_od_2014.columns = ['w_geocode','h_geocode','tot_jobs','age_29_bel_jobs',
              'age_30_54_jobs','age_55_over_jobs','sal_1250_bel_jobs','sal_1250_3333_jobs','sal_3333_over_jobs',
              'goods_prod_jobs','trade_transp_jobs','all_other_svc_jobs','createdate']


# In[18]:

# Create one list of all columns for work address path
work_join = dc_xwalk.ix[:,[0,3,5,7,9,11,12,15,17,25]]
work_join = work_join.rename(columns=lambda x: 'w_' + x)
dc_od_2014_w =pd.merge(dc_od_2014, work_join, how='left', left_on='w_geocode', right_on='w_tabblk2010')


# In[22]:

# Create one list of all columns for home address
home_join = dc_xwalk.ix[:,[0,3,5,7,9,11,12,15,17,25]]
home_join = home_join.rename(columns=lambda x: 'h_' + x)
dc_od_2014_wh =pd.merge(dc_od_2014, home_join, how='left', left_on='h_geocode', right_on='h_tabblk2010')


# In[23]:

# Stack both columns 
home_work_complete = pd.concat([dfblue, dfgreen, dforange, dfred, dfsilver, dfyellow], ignore_index=True)


# In[ ]:



