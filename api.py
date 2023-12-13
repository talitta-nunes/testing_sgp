import pandas as pd
import json
import numpy as np
from utils import engine
from sqlalchemy import text, inspect

def load_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data_from_file = json.load(file)
    return data_from_file

def normalize_json_to_dataframe(data):
    df = pd.json_normalize(data)  
    return df

def connect_to_database(df):
   
    inspector = inspect(engine)
    table_exists = inspector.has_table('sgp_brazil_data')

    if not table_exists:
        df.to_sql(name='sgp_brazil_data', con=engine, index=False, if_exists='fail')
    else:
        df.to_sql(name='sgp_brazil_data', con=engine, index=False, if_exists='append')

    with engine.connect() as conn:
        results = conn.execute(text("SELECT `TOC (wt%)`, `S (wt%)`, `Mo (ppm)`, `U (ppm)`, `V (ppm)` FROM sgp_brazil_data WHERE `Mo (ppm)` IS NOT NULL AND `U (ppm)` IS NOT NULL AND `V (ppm)` IS NOT NULL AND `TOC (wt%)` IS NOT NULL AND `S (wt%)` IS NOT NULL")).fetchall()
        result_data = np.array(results)
        result = result_data.astype(float)

    return result
        
def perform_sindy_analysis(result):
    import numpy as np
    import pandas as pd
    from pysindy import SINDy, STLSQ
    
    df = pd.DataFrame(result, columns=['TOC', 'S', 'Mo', 'U', 'V'])
    print(df)
    feature_names = ["toc", "s", "mo", "u", "v"]
    custom_optimizer = STLSQ(threshold=0.1)  
    model = SINDy(optimizer=custom_optimizer, feature_names=feature_names)


    model.fit(df.values)


    model.print()

# calling functions
data_from_file = load_data_from_file('responseData.json')
df = normalize_json_to_dataframe(data_from_file)
connect_to_database(df)
result = connect_to_database(df)
perform_sindy_analysis(result)








    
