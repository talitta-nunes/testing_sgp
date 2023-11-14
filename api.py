import pandas as pd
import json
import numpy as np
from utils import engine
from sqlalchemy import text

def load_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data_from_file = json.load(file)
    return data_from_file

def normalize_json_to_dataframe(data):
    df = pd.json_normalize(data)  
    return df

def connect_to_database(df):
    df.to_sql(name='sgp_brazil_data', con=engine, index=False, if_exists='append')
    with engine.connect() as conn:
        results =  conn.execute(text("SELECT `TOC (wt%)`, `S (wt%)` FROM sgp_brazil_data WHERE `TOC (wt%)` IS NOT NULL AND `S (wt%)` IS NOT NULL")).fetchall()
        result_data = np.array(results)
        result = result_data.astype(float)

        return result
        
def perform_sindy_analysis(resul):
    from pysindy import SINDy
    

    

# calling functions
data_from_file = load_data_from_file('response_data.json')
df = normalize_json_to_dataframe(data_from_file)
connect_to_database(df)
result = connect_to_database(df)








    
