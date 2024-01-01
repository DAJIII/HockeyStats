import pandas as pd

csvdf = pd.read_csv('teamteams.csv')
csvdf['Replace'] = csvdf['Replace'].str.replace('"', '')
csvdf['Replace'] = csvdf['Replace'].str.replace(' ', '')

csvdf.to_html('teamteams.html', index= False)