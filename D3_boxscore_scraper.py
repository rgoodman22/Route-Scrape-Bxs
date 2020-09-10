#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 18:04:26 2019

@author: rgoodman
"""

from selenium import webdriver
import time
#bs4 html decomposer#
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys
import string
import lxml
import socket
import os
import csv

#from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

chromedriver = "/Users/rgoodman/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"]


### Create Text file and structure the headers to which we will write the roster data ##
passing = open("/Users/rgoodman/Desktop/ROUTE/2017/passing.csv", 'wt', encoding='utf-8-sig')
writer_passing= csv.writer(passing, lineterminator = '\n')
writer_passing.writerow(('name', 'C-A', 'pass_yards','pass_long','pass_tds','pass_ints','player_team','opponent','date','location'))

rushing = open("/Users/rgoodman/Desktop/ROUTE/2017/rushing.csv", 'wt')
writer_rushing= csv.writer(rushing, lineterminator = '\n')
writer_rushing.writerow(('name', 'rush_att', 'rush_yards','rush_avg','rush_lng','rush_tds','player_team','opponent','date','location'))

receiving = open("/Users/rgoodman/Desktop/ROUTE/2017/receiving.csv", 'wt')
writer_receiving= csv.writer(receiving, lineterminator = '\n')
writer_receiving.writerow(('name', 'receptions', 'rec_yards','rec_avg','rec_lng','rec_tds','player_team','opponent','date','location'))

kicking = open("/Users/rgoodman/Desktop/ROUTE/2017/kicking.csv", 'wt')
writer_kicking= csv.writer(kicking, lineterminator = '\n')
writer_kicking.writerow(('name', 'fgbyatt', 'fg_long','xpbyatt','kicking_pts','player_team','opponent','date','location'))

punting = open("/Users/rgoodman/Desktop/ROUTE/2017/punting.csv", 'wt')
writer_punting= csv.writer(punting, lineterminator = '\n')
writer_punting.writerow(('name', 'punts', 'punt_yards','punt_avg','punt_long','punt_tbs','punt_insidetwenty','player_team','opponent','date','location'))

kick_offs = open("/Users/rgoodman/Desktop/ROUTE/2017/kickoffs.csv", 'wt')
writer_kick_offs= csv.writer(kick_offs, lineterminator = '\n')
writer_kick_offs.writerow(('name', 'ko_att', 'ko_yds','ko_avg','ko_tbs','ko_ob','player_team','opponent','date','location'))

returns = open("/Users/rgoodman/Desktop/ROUTE/2017/returns.csv", 'wt')
writer_returns= csv.writer(returns, lineterminator = '\n')
writer_returns.writerow(('name', 'ret_number', 'ret_yards','ret_avg','ret_long','player_team','opponent','date','location'))

intreturns = open("/Users/rgoodman/Desktop/ROUTE/2017/intreturns.csv", 'wt')
writer_intreturns= csv.writer(intreturns, lineterminator = '\n')
writer_intreturns.writerow(('name', 'ints', 'int_yards','intret_avg','intret_long','int_tds','player_team','opponent','date','location'))

fumbles = open("/Users/rgoodman/Desktop/ROUTE/2017/returns.csv", 'wt')
writer_fumbles= csv.writer(fumbles, lineterminator = '\n')
writer_fumbles.writerow(('name', 'fumb_number', 'fumb_lost','player_team','opponent','date','location'))

def_tackle = open("/Users/rgoodman/Desktop/ROUTE/2017/def_tackle.csv", 'wt')
writer_def = csv.writer(def_tackle, lineterminator = '\n')
writer_def.writerow(('number','name','solo','ast','total','sack-yards','tfl-yds','ff','fr-yrds','int-yds','brup','blks','qbh','player_team','opponent','date','location'))

gameinfo = open("/Users/rgoodman/Desktop/ROUTE/2017/gameinfo.csv", 'wt')
writer_gameinfo= csv.writer(gameinfo, lineterminator = '\n')
writer_gameinfo.writerow(('game_information', 'refs','player_team','opponent','date','location'))

## initiate driver, get the base url, start box score list ##
driver = webdriver.Chrome(chromedriver)
delay=5
url = "https://www.d3football.com/scoreboard/2017/composite?view="
box_score, playbyplay = [],[]

def play_by_play_function(pbp_url, away=None, home=None, location=None, date=None):
    try:
        pbp_driver.get(pbp_url)
        pbp_html = pbp_driver.page_source
        pbp_soup = BeautifulSoup(pbp_html, "lxml", from_encoding="utf-8")
        
        list_of_dds, list_of_plays = [],[]
        for i in pbp_soup.find_all('div', {'class':'stats-fullbox clearfix'}):
            for row in i.findAll('tr'): 
                cell = row.findAll('td')
                
                if 'Quarters' in str(cell) or 'back to top' in str(cell):
                    pass
                else:
                    try:
                        down_dist = cell[0].text.strip().replace('\n',' ')
                    except IndexError:
                        down_dist = ' '
                    try:
                        play = cell[1].text.strip().replace('\n',' ')
                    except IndexError:
                        play = ' '
                    list_of_dds.append(down_dist)
                    list_of_plays.append(play)
        
        pbp = pd.DataFrame(list(zip(list_of_dds, list_of_plays)),columns=['down_distance','play'])
        pbp = pbp[pbp['down_distance'].apply(lambda x: len(str(x)) > 1)]
        pbp['location'], pbp['date'], pbp['away_team'], pbp['home_team'] = loc, date, away, home

        return pbp
    except UnboundLocalError:
        pass


##  Loop through all college football weeks (17) ##
for i in range(1,17,1):
    url_combo = url+str(i)
    driver.get(url_combo)
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "schedule tabular-data")))
        print("Page is ready!")
        time.sleep(5)
    except TimeoutException:
        print("Loading took too much time!")
            
    html = driver.page_source
    time.sleep(3)
    
    ### Once ingested into Selenium, use bs4 to decipher html using lxml library ##
    soup = BeautifulSoup(html, "lxml", from_encoding="utf-8")
    tab = soup.find_all('div', {'class':'schedule tabular-data'})
    for i in tab:
        a = i.find_all('a')
        for i in a:
            if 'xml' in str(i):
                link = i.get('href')
                full_link = "https://www.d3football.com/"+link
                print(full_link)
                box_score.append(full_link)
            else:
                pass

##  Quit the first instance after urls are extract for all schools ##

driver = webdriver.Chrome(chromedriver)
pbp_driver = webdriver.Chrome(chromedriver)

for i in box_score:
    url = str(i)
    pbp_url = url+'?view=plays'
    driver.get(url)
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "stats-fullbox clearfix")))
        print("Page is ready!")
        time.sleep(5)
    except TimeoutException:
        print("Loading took too much time!")
    
    
    ##  Now get box score ##
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml", from_encoding="utf-8")
    tab = soup.find_all('table')
    div = soup.find_all('div', {'class':'align-center'})
    div_pbp = pbp_soup.find_all('div', {'class':'stats-fullbox clearfix'})
    ##stats-fullbox clearfix
    for i in div:
        div = i.find_all('div')
        away, home = div[0].text.split(' vs. ')[0], div[0].text.split(' vs. ')[1]
        date = div[1].text
        loc = div[2].text
    
        ##  Get PlaybyPlay data ##
    playbyplay.append(play_by_play_function(pbp_url, away=away, home=home, location=loc, date=date))

    for num in range(5,27,1):
        list_of_rows = []
        try:
            for row in tab[num].findAll('tr')[1:]:
                list_of_cells = []
                for cell in row.findAll(["td"]):
                    text = cell.text.strip('\n')
                    list_of_cells.append(text)
                list_of_rows.append(list_of_cells)
            print(list_of_rows)
        except IndexError:
            pass
        awayz = 0
        for item in list_of_rows:
            ## pass over empty lists ##
            if len(item) <= 0:
                pass
            else:
                item = [re.sub(r'[^\x00-\x7f]',r'', i) for i in item]
                ## QB Away ##
                if num == 5:
                    item.extend((away, home, date, loc))
                    writer_passing.writerow(item)
                ## QB Home ##
                elif num == 6:
                    item.extend((home, away, date, loc))
                    writer_passing.writerow(item) 
                    
                ## Rushing Away ##
                elif num == 7:
                    item.extend((away, home, date, loc))
                    writer_rushing.writerow(item)
                ## Rushing Home ##
                elif num == 8:
                    item.extend((home, away, date, loc))
                    writer_rushing.writerow(item) 
                    
                ## Receiving Away ##
                elif num == 9:
                    item.extend((away, home, date, loc))
                    writer_receiving.writerow(item)
                ## Receiving Home ##
                elif num == 10:
                    item.extend((home, away, date, loc))
                    writer_receiving.writerow(item) 
                    
                ## Kicking Away ##
                elif num == 11:
                    item.extend((away, home, date, loc))
                    writer_kicking.writerow(item)
                ## Kicking Home ##
                elif num == 12:
                    item.extend((home, away, date, loc))
                    writer_kicking.writerow(item) 
                    
                ## Punting away ##
                elif num == 13:
                    item.extend((away, home, date, loc))
                    writer_punting.writerow(item)
                ## Punting Home ##
                elif num == 14:
                    item.extend((home, away, date, loc))
                    writer_punting.writerow(item)
                    
                ## KOs away ##                    
                elif num == 15:
                    item.extend((away, home, date, loc))
                    writer_kick_offs.writerow(item)
                ## KOs home ## 
                elif num == 16:
                    item.extend((home, away, date, loc))
                    writer_kick_offs.writerow(item)
                    
                ## KO returns away ##
                elif num == 17:
                    item.extend((away, home, date, loc))
                    writer_returns.writerow(item)
                ## KO returns home ##
                elif num == 18:
                    item.extend((home, away, date, loc))
                    writer_returns.writerow(item)
                    
                ## returns away ##
                elif num == 19:
                    item.extend((away, home, date, loc))
                    writer_returns.writerow(item)
                ## returns home ##
                elif num == 20:
                    item.extend((home, away, date, loc))
                    writer_returns.writerow(item)
                
                ## int returns away ##
                elif num == 21:
                    item.extend((away, home, date, loc))
                    writer_intreturns.writerow(item)                    
                ## int returns home ##
                elif num == 22:
                    item.extend((home, away, date, loc))
                    writer_intreturns.writerow(item)
                 ## int fumbles away ##
                elif num == 23:
                    item.extend((away, home, date, loc))
                    writer_fumbles.writerow(item)                    
                ## int fumbles home ##
                elif num == 24:
                    item.extend((home, away, date, loc))
                    writer_fumbles.writerow(item)
                    
                ## Tackles table ##
                elif num == 25:
                    if 'TOTALS' in str(item):
                        awayz = 1
                    else:
                        pass
                    if awayz == 0:
                        item.extend((away, home, date, loc))
                        if 'TOTALS' in str(item) or 'TM' in str(item):
                            pass
                        else:
                            #csvRow.append(item)
                            writer_def.writerow(item)
                    elif awayz == 1:
                        item.extend((home, away, date, loc))
                        if 'TOTALS' in str(item) or 'TM' in str(item):
                            pass
                        else:
                            #csvRow.append(item)
                            writer_def.writerow(item)
                    else:
                        pass
                elif num == 26:
                    item.extend((home, away, date, loc))
                    writer_gameinfo.writerow(item)
                else:
                    pass
        
        
passing.close()
rushing.close()
receiving.close()
kicking.close()
punting.close()
kick_offs.close()
returns.close()
intreturns.close()
fumbles.close()
def_tackle.close()
gameinfo.close()

