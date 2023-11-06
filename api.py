import requests
import pandas as pd
import json
from constants import URL, BODY
from utils import engine

def make_api_request():
    header = {'content-type': 'application/json'}
    try:
        res = requests.post(URL, headers=header, json=BODY)
        res.raise_for_status()  
        responseData = res.json()
        return responseData
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def load_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data_from_file = json.load(file)
    return data_from_file

def normalize_json_to_dataframe(data):
    df = pd.json_normalize(data)  
    return df

def connect_to_database(df):
    df.to_sql(name='sgp_brazil_data', con=engine, index=False, if_exists='append')


response_data = make_api_request()
data_from_file = load_data_from_file('response_data.json')
df = normalize_json_to_dataframe(data_from_file)
connect_to_database(df)






    
