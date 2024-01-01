#Import Libraries
import pandas as pd
import datetime as dt
import sqlite3 

#Connect to DB
conn = sqlite3.connect('HockeyStats.db')

#Set Date Variables
statdate = dt.date.today()- dt.timedelta(days= 1)
statday = statdate.strftime('%Y-%m-%d')

#Set URL for Scrape
staturl = f'https://www.naturalstattrick.com/playerteams.php?fromseason=20232024&thruseason=20232024&stype=2&sit=all&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=gpdate&fd={statday}&td={statday}&tgp=410&lines=single&draftteam=ALL'

#Scrape the Data to DF
dailydf = pd.read_html(staturl)
dailydf = dailydf[0]

#Modify DF for DB
dailydf = dailydf.drop(['Unnamed: 0'], axis = 1)
dailydf['GameDate'] = statdate

#Load to DB
dailydf.to_sql('PlayerStats', con= conn, index = False, if_exists= 'append')

