#Import Libraries
import pandas as pd
import datetime as dt
import sqlite3 

#Connect to DB
conn = sqlite3.connect('HockeyStats.db')

#Set Date Variables
statdate = dt.date.today()- dt.timedelta(days= 1)
statday = statdate.strftime('%Y-%m-%d')

#Import Abbreviations for ETL
abrev = pd.read_csv('teamteams.csv')
abrev = abrev.set_index('Team')
abrvdict = abrev.to_dict()
abrvdict = abrvdict['Replace']

#Set URL for webscrape
staturl = f'https://www.naturalstattrick.com/teamtable.php?fromseason=20232024&thruseason=20232024&stype=2&sit=all&score=all&rate=n&team=all&loc=B&gpf=410&fd={statday}&td={statday}'

#Webscrape for Stats
dailydf = pd.read_html(staturl)
dailydf = dailydf[0]

#Modifying DataFrame for DB Compatability 
dailydf = dailydf.drop(['Unnamed: 0'], axis = 1)
dailydf['GameDate'] = statdate
for key in abrvdict:
    dailydf['Team'] = dailydf['Team'].str.replace(key, abrvdict[key], regex= True)

dailydf.to_sql('TeamStats', con= conn, index = False, if_exists= 'append')


