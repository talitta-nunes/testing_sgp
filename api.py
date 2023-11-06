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
        results =  conn.execute(text("SELECT `TOC (wt%)`, `S (wt%)` FROM sgp_brazil_data")).fetchall()
        result_data = np.array(results)
        result = result_data.astype(float)

        result = result[~np.isnan(result).any(axis=1)]
        result[np.isnan(result)] = 0 
        return result
        
def testing_pysindy(result):
    from pysindy import SINDy
    
    model = SINDy()
    model.fit(result)
    
    feature_names = model.get_feature_names()
    coefficients = model.coefficients()

    for feature, coefficient in zip(feature_names, coefficients):
        equation = f"{feature} = {coefficient[0]:.4f}" 
        print(equation)

# calling functions
data_from_file = load_data_from_file('response_data.json')
df = normalize_json_to_dataframe(data_from_file)
connect_to_database(df)
result = connect_to_database(df)
testing_pysindy(result)






    
