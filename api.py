import pandas as pd
import json
import numpy as np
from utils import engine
from sqlalchemy import text, inspect


def add_data_to_database():
    inspector = inspect(engine)
    table_exists = inspector.has_table('sgp_iron_data')
    if not table_exists:
        df = pd.read_json("responseIronData.json")
        df.to_sql('sgp_iron_data', con=engine, index=False)
    else:
        print("Table 'sgp_iron_data' already exists. Not appending or replacing.")


# def retrieve_data_from_database():
#     with engine.connect() as conn:
#         results = conn.execute(text("""
#             SELECT
#                 `TOC (wt%)`,
#                 `interpreted age`
#             FROM
#                 sgp_all_data;                        
#         """)).fetchall()
#         result_data = np.array(results)
#         result = result_data.astype(float)

#     return result
       
# def perform_sindy_analysis(result):
#     import numpy as np
#     import pandas as pd
#     import matplotlib.pyplot as plt
#     from pysindy import SINDy, STLSQ
  
    
#     df = pd.DataFrame(result, columns=['toc',  'age'])
#     df = df.sort_values(by='age')
  

#     df['toc'] = df['toc'].interpolate(method='linear')
#     df['age'] = df['age'].interpolate(method='linear')
    
    
#     print('\nFinal DataFrame:')
#     print(df)
#     mean_toc = df.groupby('age')["toc"].mean().reset_index()

#     t = mean_toc["age"].values
#     toc_data = mean_toc["toc"].values
#     print(f'\neste é o t', t)
#     print(f'------------------------fim----------------------')
#     print(f'\neste é o toc', toc_data)
#     print(f'------------------------fim----------------------')
#     feature_names = ["toc"]
#     custom_optimizer = STLSQ(threshold=0)  
#     model = SINDy(optimizer=custom_optimizer, feature_names=feature_names)
#     model.fit(toc_data, t=t)
#     model.print()

#     predicted_toc = model.predict(toc_data)

#     plt.plot(t, toc_data, label='Original toc')
#     plt.plot(t, predicted_toc, label='Predicted toc', linestyle='--', color='red')
#     plt.gca().invert_xaxis()
#     plt.xlabel('Time (Ma)')
#     plt.ylabel('TOC (wt%)')
#     plt.legend()
#     plt.show()



# Add data to the database
# df = load_data_from_file('responseSGP.json')
# df_normalized = normalize_json_to_dataframe(df)
add_data_to_database()

# Retrieve data from the database
# result = retrieve_data_from_database()
# perform_sindy_analysis(result)






    
