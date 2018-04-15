#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 12:54:32 2018

@author: jdf972
"""


from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# HTML FROM CRAIGSLIST PERSONALS


# START WITH 3 RECORDS TO GET CODEW WORKING
# clhtml_txt = '/Users/jdf972/Documents/HACKATHON_TRAF/craigslist_00_top3.txt'

# OK, READY TO SCALE TO FULL HTML (WITH HTML FROM 1731 CRAIGSLIST ADS)
clhtml_txt = '/Users/jdf972/Documents/HACKATHON_TRAF/craigslist_00.txt'

clhtml = open(clhtml_txt,'r')
soup = BeautifulSoup( clhtml, 'html.parser')

# print(soup.prettify())



### TITLES ###

titles2 = list(soup.find_all("title"))

titles2_str = []
for obj in titles2:
    titles2_str.append(str(obj)[7:-8])

titles2_series = pd.Series(titles2_str)



### CITY SUB-AREAS ###

breadcrumbs = list(soup.find_all(class_="breadcrumbs"))

breadcrumbs2 = breadcrumbs[0::2]

subareas_str = []
for obj in breadcrumbs2:
    if str(obj).find('crumb subarea') == -1:
        subareas_str.append('NOT_LISTED')
    else:
        subareas_str.append(str(obj).split('/">', 2)[2].split('<', 1)[0])

subareas_str[0:9]

subareas_series = pd.Series(subareas_str)



### CITIES ("AREAS") ###

areas = list(soup.find_all(class_="crumb area"))
areas[0:9]
areas_str = []
for obj in areas:
    areas_str.append(str(obj).split('/">', 1)[1].split('<', 1)[0])
areas_str[0:9]
areas_series = pd.Series(areas_str)



### MAIN BODIES OF ADS ###

adbodies = soup.find_all(id="postingbody")

adbodies_str = []
#for obj in adbodies:
#    adbodies_str.append(str(obj.contents[2]).split('\n', 1)[1])
for obj in adbodies:
    adbodies_str.append(obj.contents[2].encode('utf-8').split('\n', 1)[1])
adbodies_str[0:9]
adbodies_series = pd.Series(adbodies_str)



### POST ID ###

postids = soup.find_all(class_="postinginfos")

postids_str = []
for obj in postids:
    postids_str.append(str(obj.contents[1]).split('post id: ', 1)[1].split('<', 1)[0])
postids_str[0:9]
postids_series = pd.Series(postids_str)



### DATE INFO ###

dates_str = []
for obj in postids:
    dates_str.append(str(obj.contents[3]).split('datetime="', 1)[1].split('T', 1)[0])
dates_str[0:9]
dates_series = pd.Series(dates_str)



### TIMESTAMP ###

times_str = []
for obj in postids:
    times_str.append(str(obj.contents[3]).split('T', 1)[1].split('-', 1)[0])
times_str[0:9]
times_series = pd.Series(times_str)
    


### COMBINE INTO SINGLE DATAFRAME ###

titles2_series.shape
subareas_series.shape
areas_series.shape
adbodies_series.shape
postids_series.shape
dates_series.shape
times_series.shape

allcombined = pd.DataFrame({'Title': titles2_series,
                            'SubArea': subareas_series,
                            'Area': areas_series,
                            'AdBody': adbodies_series,
                            'PostID': postids_series,
                            'Date': dates_series,
                            'Time': times_series},
                           index=range(len(titles2_series)))

allcombined.shape
allcombined.head

allcombined.to_csv('/Users/jdf972/Documents/HACKATHON_TRAF/craigslist_formatted.csv')
