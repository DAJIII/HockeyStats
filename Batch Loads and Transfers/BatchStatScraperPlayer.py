import pandas as pd
import datetime as dt
import sqlite3 
import time

conn = sqlite3.connect('HockeyStats.db')

statdate = dt.datetime(2023,10,10)
count = 0

while statdate <= dt.datetime(2023, 12, 31):
    statday = statdate.strftime('%Y-%m-%d')
    staturl = f'https://www.naturalstattrick.com/playerteams.php?fromseason=20232024&thruseason=20232024&stype=2&sit=all&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=gpdate&fd={statday}&td={statday}&tgp=410&lines=single&draftteam=ALL'
    dailydf = pd.read_html(staturl)
    dailydf = dailydf[0]
    dailydf = dailydf.drop(['Unnamed: 0'], axis = 1)
    dailydf['GameDate'] = statdate
    dailydf.to_sql('PlayerStats', con= conn, index = False, if_exists= 'append')
    statdate = statdate + dt.timedelta(days = 1)
    count += 1
    if count % 10 == 0:
        time.sleep(60)



