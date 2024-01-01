import pandas as pd


teamdf = pd.read_csv('games.csv')
abrev = pd.read_csv('gameteams.csv')

abrev = abrev.set_index('Team')

abrvdict = abrev.to_dict()
abrvdict = abrvdict['Replace']

for key in abrvdict:
    teamdf['Team'] = teamdf['Team'].str.replace(key, abrvdict[key])
    teamdf['Opponent'] = teamdf['Opponent'].str.replace(key, abrvdict[key])

print(teamdf.head())