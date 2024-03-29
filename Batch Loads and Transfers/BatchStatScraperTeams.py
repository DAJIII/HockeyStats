import pandas as pd
import datetime as dt
import sqlite3 
import time

conn = sqlite3.connect('HockeyStats.db')

#Import Abbreviations for ETL
abrev = pd.read_csv('teamteams.csv')
abrev = abrev.set_index('Team')
abrvdict = abrev.to_dict()
abrvdict = abrvdict['Replace']

statdate = dt.datetime(2023,10,10)
count = 0

while statdate <= dt.datetime(2024, 1, 1):
    statday = statdate.strftime('%Y-%m-%d')
    staturl = f'https://www.naturalstattrick.com/teamtable.php?fromseason=20232024&thruseason=20232024&stype=2&sit=all&score=all&rate=n&team=all&loc=B&gpf=410&fd={statday}&td={statday}'
    dailydf = pd.read_html(staturl)
    dailydf = dailydf[0]
    dailydf = dailydf.drop(['Unnamed: 0'], axis = 1)
    dailydf['GameDate'] = statdate
    for key in abrvdict:
        dailydf['Team'] = dailydf['Team'].str.replace(key, abrvdict[key], regex= True)
    dailydf.to_sql('TeamStats', con= conn, index = False, if_exists= 'append')
    statdate = statdate + dt.timedelta(days = 1)
    count += 1
    if count % 10 == 0:
        time.sleep(60)

