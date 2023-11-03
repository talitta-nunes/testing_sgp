import requests
# import pandas as pd
# import sqlalchemy
from constants import URL, BODY

def sgpAPI():
    header = {'content-type': 'application/json'}
    try:
        res = requests.post(URL, headers=header, json=BODY)
        res.raise_for_status()  
        responseData = res.json()
        
        print(res) 
        print(responseData)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
sgpAPI()