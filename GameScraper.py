#Import Libraries
import pandas as pd
import datetime as dt
import sqlite3 

#Connect to DB
conn = sqlite3.connect('HockeyStats.db')

#URL for scraping
url = 'https://www.hockey-reference.com/leagues/NHL_2024_games.html'

#Importing Abbreviations for ETL
abrev = pd.read_csv('gameteams.csv')
abrev = abrev.set_index('Team')
abrvdict = abrev.to_dict()
abrvdict = abrvdict['Replace']

#Scraping Data to DF
df = pd.read_html(url)
df= df[0]

#Modifiying Data for DB Usage
homedf = df[['Date', 'Home', 'Visitor', 'G', 'G.1']]

awaydf = df[['Date', 'Visitor', 'Home', 'G', 'G.1']]

homedf = homedf.rename(columns={'Date': 'Date', 'Home': 'Team', 'Visitor': 'Opponent', 'G': 'GF', "G.1": 'GA'})

awaydf= awaydf.rename(columns={'Date': 'Date', 'Visitor': 'Team', 'Home': 'Opponent', 'G': 'GA', "G.1": 'GF'})

homedf['HomeAway'] = 'Home'
awaydf['HomeAway'] = 'Away'

gamedf = pd.concat([homedf, awaydf])

for key in abrvdict:
    gamedf['Team'] = gamedf['Team'].str.replace(key, abrvdict[key], regex= True)
    gamedf['Opponent'] = gamedf['Opponent'].str.replace(key, abrvdict[key], regex= True)

gamedf = gamedf[gamedf['GF'].notna()]

#Exporting Data to DB
if len(gamedf) > 0:
    gamedf.to_sql('GameStats', con= conn, index = False, if_exists= 'append')
else:
    print('No Games Today')



