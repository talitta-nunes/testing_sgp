import os
from dotenv import load_dotenv
import requests
from constants import URL, BODY
from sqlalchemy import create_engine

load_dotenv()


# def make_api_request():
#     header = {'content-type': 'application/json'}
#     try:
#         res = requests.post(URL, headers=header, json=BODY)
#         res.raise_for_status()  
#         responseData = res.json()
        
#         return responseData
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
        
# response_data = make_api_request()

engine = create_engine(f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_BASE')}")
