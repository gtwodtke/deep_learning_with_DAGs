import numpy as np
import pandas as pd
import os
import networkx as nx
import time
from causalgraphicalmodels import CausalGraphicalModel
from processing_parallel import process
from training_parallel import train
from simulation_parallel_new import sim
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

def run_simulation(i, node_id):
    print(f"Running simulation {i} on Process ID: {os.getpid()}")
    start_time = time.time()

    base_path = '/project/wodtke/cGNF_python_code/compare_10cat/64k'
    folder = f'DF_{node_id}_{i}'  # Note the use of i to create a unique folder for each iteration
    path = os.path.join(base_path, folder, '')
    dataset_name = 'DF1_64k_loop'

    df_filename = path + dataset_name + '.csv'

    # Pack data into a DataFrame
    df = pd.read_csv(df_filename)
    
    df_rf = df.copy()  # Create a copy for Random Forest operations

    # Fit a Random Forest Classifier for A with C1 and C2 as predictors
    rf_clf = RandomForestClassifier(
        n_estimators=200,
        min_samples_leaf=80,
        max_features=1
    )

    rf_clf.fit(df_rf[['C1', 'C2']], df_rf['A'])

    # Fit a Random Forest Regressor for Y with C1, C2, and A as predictors
    rf_reg = RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=80,
        max_features=1
    )

    rf_reg.fit(df_rf[['C1', 'C2', 'A']], df_rf['Y'])

    # Predict phat for A = 7 and A = 2
    df_rf['phat_7'] = rf_clf.predict_proba(df_rf[['C1', 'C2']])[:, 7]
    df_rf['phat_2'] = rf_clf.predict_proba(df_rf[['C1', 'C2']])[:, 2]

    # Predict Yhat based on the model for Y with observed A, C1, and C2
    df_rf['Yhat'] = rf_reg.predict(df_rf[['C1', 'C2', 'A']])

    # Predict Yhat_7 (all A = 7)
    df_rf['Yhat_7'] = rf_reg.predict(df_rf[['C1', 'C2']].assign(A=7))

    # Predict Yhat_2 (all A = 2)
    df_rf['Yhat_2'] = rf_reg.predict(df_rf[['C1', 'C2']].assign(A=2))

    # Compute ipw_7
    df_rf['ipw_7'] = ((df_rf['A'] == 7).astype(int) / df_rf['phat_7'])

    # Compute ipw_2
    df_rf['ipw_2'] = ((df_rf['A'] == 2).astype(int) / df_rf['phat_2'])

    # Compute residue term for Y model
    df_rf['residue'] = df_rf['Y'] - df_rf['Yhat']

    # Compute dr_7
    df_rf['dr_7'] = df_rf['ipw_7'] * df_rf['residue'] + df_rf['Yhat_7']

    # Compute dr_2
    df_rf['dr_2'] = df_rf['ipw_2'] * df_rf['residue'] + df_rf['Yhat_2']

    # Mean of dr_7 and dr_2
    dr_7_mean = df_rf['dr_7'].mean()
    dr_2_mean = df_rf['dr_2'].mean()

    ATEhat = dr_7_mean - dr_2_mean

    end_time = time.time()
    time_taken = end_time - start_time

    return [ATEhat, time_taken]

