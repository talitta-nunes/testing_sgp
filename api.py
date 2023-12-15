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
    table_exists = inspector.has_table('sgp_all_data')

    if not table_exists:
        df.to_sql(name='sgp_all_data', con=engine, index=False, if_exists='fail')
    else:
        df.to_sql(name='sgp_all_data', con=engine, index=False, if_exists='append')

    with engine.connect() as conn:
        results = conn.execute(text("""
        SELECT
    `TOC (wt%)`,
    `interpreted age`
        FROM
    sgp_all_data;                        
        """)).fetchall()
        result_data = np.array(results)
        result = result_data.astype(float)

    return result
       
def perform_sindy_analysis(result):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from pysindy import SINDy, STLSQ
  
    
    df = pd.DataFrame(result, columns=['toc',  'age'])
    
    df = df.sort_values(by='age')
    
    df['toc'] = df['toc'].interpolate(method='linear')
    df['age'] = df['age'].interpolate(method='linear')

    mean_toc = df.groupby('age')["toc"].mean().reset_index()

    t = mean_toc["age"].values
    toc_data = mean_toc["toc"].values

    feature_names = ["toc"]
    custom_optimizer = STLSQ(threshold=0)  
    model = SINDy(optimizer=custom_optimizer, feature_names=feature_names)
    model.fit(toc_data, t=t)
    model.print()

    predicted_toc = model.predict(toc_data)

    plt.plot(t, toc_data, label='Original toc')
    plt.plot(t, predicted_toc, label='Predicted toc', linestyle='--', color='red')
    plt.gca().invert_xaxis()
    plt.xlabel('Time (Ma)')
    plt.ylabel('TOC (wt%)')
    plt.legend()
    plt.show()



# calling functions
data_from_file = load_data_from_file('responseSGP.json')
df = normalize_json_to_dataframe(data_from_file)
connect_to_database(df)
result = connect_to_database(df)
perform_sindy_analysis(result)








    
