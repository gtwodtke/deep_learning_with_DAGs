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
    obs = 64000
    
    # Baseline Confounders
    C1 = np.random.normal(0, 1, obs)
    C2 = np.random.normal(0, 1, obs)+ C1
    
    # Logistic transformation
    logit_A = 0.1 * C1 + 0.2 * C2
    prob_A = 1 / (1 + np.exp(-logit_A))
    
    # Generate binary A
    A = np.random.binomial(1, prob_A, obs)
    
    # Error for Y
    epsilon_Y = np.random.normal(0, 1, obs)
    
    # Standard normal Y
    Y = 0.1 * A + 0.1 * C2 + 0.3 * C1 + 0.2 * A * C1 * C2 + epsilon_Y
    
    # pack into a dataframe
    df = pd.DataFrame(data={'C1': C1, 'C2': C2, 'A': A, 'Y': Y})
    
    df_rf = df.copy()  # Create a copy for Random Forest operations
    
    # Fit a Random Forest Classifier for A with C1 and C2 as predictors
    rf_clf = RandomForestClassifier(
        n_estimators=200,
        min_samples_leaf=5,
        max_features=1
    )
    rf_clf.fit(df_rf[['C1', 'C2']], df_rf['A'])
    
    # Fit a Random Forest Regressor for Y with C1, C2, and A as predictors
    rf_reg = RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=5,
        max_features=1
    )
    rf_reg.fit(df_rf[['C1', 'C2', 'A']], df_rf['Y'])
    
    # Predict phat using the model for A with observed C1 and C2
    df_rf['phat'] = rf_clf.predict_proba(df_rf[['C1', 'C2']])[:, 1]
    
    # Predict Yhat based on the model for Y with observed A, C1, and C2
    df_rf['Yhat'] = rf_reg.predict(df_rf[['C1', 'C2', 'A']])
    
    # Predict Yhat_1 (all A = 1)
    df_rf['Yhat_1'] = rf_reg.predict(df_rf[['C1', 'C2']].assign(A=1))
    
    # Predict Yhat_0 (all A = 0)
    df_rf['Yhat_0'] = rf_reg.predict(df_rf[['C1', 'C2']].assign(A=0))
    
    # Compute ipw
    df_rf['ipw'] = (df_rf['A'] / df_rf['phat']) - ((1 - df_rf['A']) / (1 - df_rf['phat']))
    
    # Compute residue term for Y model
    df_rf['residue'] = df_rf['Y'] - df_rf['Yhat']
    
    # Compute eif
    df_rf['eif'] = df_rf['ipw'] * df_rf['residue'] + (df_rf['Yhat_1'] - df_rf['Yhat_0'])
    
    # Compute ATEhat
    ATEhat = df_rf['eif'].mean()

    base_path = '/project/wodtke/cGNF_python_code/64k'
    folder = f'DF_{node_id}_{i}'  # Note the use of i to create a unique folder for each iteration
    path = os.path.join(base_path, folder, '')
    dataset_name = 'DF1_64k_loop'

    if not os.path.isdir(path):
        os.makedirs(path)
    
    df_filename = path + dataset_name + '.csv'
    df.to_csv(df_filename, index=False)
    
    simDAG = CausalGraphicalModel(
        nodes=["C1", "C2", "A", "Y"],
        edges=[ ("C1", "C2"), ("C1", "A"), ("C2", "A"), ("C1", "Y"), ("C2", "Y"), ("A", "Y")])
    
    df_cDAG = nx.to_pandas_adjacency(simDAG.dag, dtype=int)
    df_cDAG.to_csv(path + dataset_name + '_DAG.csv')
    
    process(path=path, dataset_name=dataset_name, dag_name=dataset_name + '_DAG', test_size=0.2, cat_var=['A'], seed=None)
    train(path=path, dataset_name=dataset_name, model_name =path + '64k_loop',
          trn_batch_size=128, val_batch_size=4096, learning_rate=1e-4, seed=None, nb_epoch=50000,
          emb_net=[100, 90, 80, 70, 60], int_net=[60, 50, 40, 30, 20], nb_estop=50, val_freq=1)

    ate_results_df = sim(path=path, dataset_name=dataset_name, model_name=path + '64k_loop', n_mce_samples=100000, treatment='A', cat_list=[0, 1],
       confounder=["C1", "C2"], moderator=None, mediator=None, outcome='Y', inv_datafile_name='boot_ate_64k')

    results_df = pd.concat([ate_results_df], ignore_index=True)

    values_list = results_df['Value'].tolist()

    end_time = time.time()
    time_taken = end_time - start_time

    values_list.extend([ATEhat, time_taken])
    
    return values_list
