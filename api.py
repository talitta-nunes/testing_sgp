import pandas as pd
import json
import numpy as np
from utils import engine
from sqlalchemy import text, inspect
import pysindy as ps
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
import dask.dataframe as dd
import statsmodels.api as sm
from pysindy import SINDy, STLSQ
from scipy.interpolate import interp1d
from scipy import signal
from pysindy.feature_library import FourierLibrary, PolynomialLibrary, GeneralizedLibrary, CustomLibrary, IdentityLibrary
from scipy.integrate import ode
from sklearn.linear_model import LinearRegression
from sklearn.exceptions import NotFittedError
from scipy.signal import savgol_filter
from scipy.integrate import solve_ivp
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from scipy.signal import butter, filtfilt
from sklearn.preprocessing import PolynomialFeatures

# # def add_data_to_database():
# #     inspector = inspect(engine)
# #     table_exists = inspector.has_table('sgp_iron_data')
# #     if not table_exists:
# #         df = pd.read_json("responseIronData.json")
# #         df.to_sql('sgp_iron_data', con=engine, index=False)
# #     else:
# #         print("Table 'sgp_iron_data' already exists. Not appending or replacing.")


# def retrieve_data_from_database():
#     with engine.connect() as conn:
#         results = conn.execute(text("""
#             SELECT
#                 `TOC (wt%)`,
#                 `interpreted age`,
#                 `P (ppm)`,
#                 `FeHR/FeT (wt%)`,
#                 `Fe-py/FeHR (wt%)`
                                    
#             FROM
#                 sgp_iron_data;                        
#         """)).fetchall()
#         result_data = np.array(results)
#         result = result_data.astype(float)

#     return result

#  result = retrieve_data_from_database()      
def apply_butterworth_and_sindy(cutoff, order):
    # Carregar e preparar os dados
    data = dd.read_csv("DATA_IRON_ONLY.csv")
    data = np.array(data).astype(float)
    df = pd.DataFrame(data, columns=['toc', 'age', 'ironspec', 'pyrite', 'p'])
    df.info()
    df = df.sort_values('age')
    df.interpolate(limit_direction="both", inplace=True)
    filtered_df = df[(df['age'] >= 440) & (df['age'] <= 445)]
    filtered_df['rounded_age'] = filtered_df['age'].round(1)
    grouped_data = filtered_df.groupby('rounded_age').mean().reset_index()
    grouped_data['p'] = grouped_data['p'] / 10000  # Normalize phosphorous

    # Aplicar o filtro Butterworth
    def apply_butterworth_filter(data, cutoff, order):
        b, a = butter(order, cutoff, btype='low', analog=False)
        filtered_data = filtfilt(b, a, data)
        filtered_data[filtered_data < 0] = 0  # Ensure non-negative values
        return filtered_data

    grouped_data['toc_smooth'] = apply_butterworth_filter(grouped_data['toc'].values, cutoff, order)
    grouped_data['pyrite_smooth'] = apply_butterworth_filter(grouped_data['pyrite'].values, cutoff, order)
    grouped_data['p_smooth'] = apply_butterworth_filter(grouped_data['p'].values, cutoff, order)
    grouped_data['ironspec_smooth'] = apply_butterworth_filter(grouped_data['ironspec'].values, cutoff, order)
    grouped_data.plot(x='age', subplots=True)

    # Salvar os dados agrupados em um arquivo Excel
    # file_name = f'Data_SGP_cutoff{cutoff}_order{order}.xlsx'
    # grouped_data.to_excel(file_name)

    # Extrair os dados necessários para o PYSINDY
    t = grouped_data["age"].values
    data_p = grouped_data['p_smooth'].values
    data_py = grouped_data['pyrite_smooth'].values
    data_toc = grouped_data["toc_smooth"].values
    data_ironspec = grouped_data["ironspec_smooth"].values
    # Ajustar o modelo aos dados
    data_list = np.stack((data_toc, data_py, data_p, data_ironspec), axis=-1)
    dif = ps.SINDyDerivative(kind='kalman', alpha = 0.2)

    differentiation_method = ps.SmoothedFiniteDifference(smoother_kws={'window_length': 4})
    poly_lib=ps.PolynomialLibrary(degree=2, include_bias=False)
    feature_names = ["toc", "pyrite", "p", "ironspec"]
    custom_optimizer = ps.STLSQ(threshold=1e-6)

    model = ps.SINDy(differentiation_method=dif,feature_names=feature_names, optimizer=custom_optimizer)
    model.fit(data_list, t, ensemble=True)
    print("\nDerivatives for SINDy:")
    model.print()
    # Simular os dados
    simulated_data_list = model.simulate(data_list[0], t, integrator='solve_ivp')

    # Plotar os resultados da simulação
    fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
    axs[0].plot(t, data_toc, label='DATA TOC')
    axs[0].plot(t, simulated_data_list[:, 0], '--', label='SINDY TOC')
    axs[0].set(ylabel='TOC')
    axs[0].legend()
    axs[0].grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    axs[1].plot(t, data_py, label='DATA FePy/FeHR')
    axs[1].plot(t, simulated_data_list[:, 1], '--', label='SINDY FePy/FeHR')
    axs[1].set(ylabel='FePy/FeHR')
    axs[1].legend()
    axs[1].grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    axs[2].plot(t, data_p, label='DATA phosphorous')
    axs[2].plot(t, simulated_data_list[:, 2], '--', label='SINDY phosphorous')
    axs[2].set(ylabel='Phosphorous')
    axs[2].legend()
    axs[2].grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    axs[3].plot(t, data_p, label='DATA Ironspec')
    axs[3].plot(t, simulated_data_list[:, 3], '--', label='SINDY Ironspec')
    axs[3].set(ylabel='Ironspec')
    axs[3].legend()
    axs[3].grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    axs[-1].set(xlabel='Age')
    plt.tight_layout()
    plt.show()

# Testar diferentes valores de cutoff e order
cutoff_values = [0.1, 0.2, 0.3, 0.4]
order_values = [1, 2, 3, 4, 5]

for cutoff in cutoff_values:
    for order in order_values:
        print(f"\nTesting with cutoff={cutoff} and order={order}")
        apply_butterworth_and_sindy(cutoff, order)

#Add data to the database
# df = load_data_from_file('responseSGP.json')
# df_normalized = normalize_json_to_dataframe(df)
# add_data_to_database()

#Retrieve data from the database








    
