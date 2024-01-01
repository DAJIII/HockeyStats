from airflow import DAG 
from airflow.operators.bash import BashOperator 
from datetime import datetime 

default_args = {
    'owner': 'Alan Johnston',
    'email': 'ajohnston.bh@gmail.com',
    'start_date': datetime(2023, 10, 11),
    'end_date': datetime(2024, 4, 18),
    'retries': 3,
}

dag = DAG(
    'DailyHockeyStats',
    default_args = default_args,
    description= 'Daily Web Scrape of Hockey Stats to a sqlite DB',
    catchup= False,
    schedule= '0 7 * * *',
)

GameData = BashOperator(
    task_id = 'GameData',
    bash_command = 'python3 /Users/DAJIII/HockeyStats/GameScraper.py',
    dag= dag, 
)

TeamData = BashOperator(
    task_id = 'TeamData',
    bash_command = 'python3 /Users/DAJIII/HockeyStats/DailyStatScraperTeams.py',
    dag= dag, 
)

PlayerData = BashOperator(
    task_id = 'PlayerData',
    bash_command = 'python3 /Users/DAJIII/HockeyStats/DailyStatScraperPlayer.py',
    dag= dag, 
)

GameData >> TeamData >> PlayerData