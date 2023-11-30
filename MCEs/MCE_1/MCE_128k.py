import numpy as np
import pandas as pd
import os
import networkx as nx
import time
from causalgraphicalmodels import CausalGraphicalModel
from cGNF.process_parallel import process
from cGNF.train_parallel import train
from cGNF.simulation_parallel import sim
import statsmodels.api as sm

def run_simulation(i, node_id):
    print(f"Running simulation {i} on Process ID: {os.getpid()}")
    start_time = time.time()
    obs = 128000

    loc_c, scale_c = 0, 1
    C = np.random.normal(loc_c, scale_c, obs)

    # treatment, normal
    loc_a, scale_a = 0, 1  # mean and standard deviation of A
    A = np.random.normal(loc_a, scale_a, obs) + 0.1*C

    # exposure-induced confounder, normal
    loc_l, scale_l = 0, 1  # mean and standard deviation of L
    L = np.random.normal(loc_l, scale_l, obs) + 0.2*A + 0.2*C

    # mediator, exponential
    loc_m, scale_m = 0, 1
    M = np.random.normal(loc_m, scale_m, obs) + 0.1*A + 0.2*C + 0.25*L

    # outcome, normal
    loc_y, scale_y = 0, 1  # mean and standard deviation of Y
    Y = np.random.normal(loc_y, scale_y, obs) + 0.1*A + 0.1*C + 0.2*M + 0.25*L

    # pack into a dataframe
    df = pd.DataFrame({'A': A, 'C': C, 'M': M, 'L': L, 'Y': Y})

    def fit_with_statsmodels(df, dependent_var, independent_vars):
        X = sm.add_constant(df[independent_vars])
        model = sm.OLS(df[dependent_var], X).fit()
        return model.params


    coeff_l_statsmodels = fit_with_statsmodels(df, 'L', ['A', 'C'])
    coef_LA = coeff_l_statsmodels['A']

    coeff_m_statsmodels = fit_with_statsmodels(df, 'M', ['A', 'C', 'L'])
    coef_MA = coeff_m_statsmodels['A']
    coef_ML = coeff_m_statsmodels['L']

    coeff_y_statsmodels = fit_with_statsmodels(df, 'Y', ['A', 'C', 'M', 'L'])
    coef_YA = coeff_y_statsmodels['A']
    coef_YM = coeff_y_statsmodels['M']
    coef_YL = coeff_y_statsmodels['L']

    base_path = '/project/wodtke/cGNF_python_code/128k'
    folder = f'DF_{node_id}_{i}'  # Note the use of i to create a unique folder for each iteration
    path = os.path.join(base_path, folder, '')
    dataset_name = 'DF1_128k_loop'

    if not os.path.isdir(path):
        os.makedirs(path)

    df_filename = path + dataset_name + '.csv'
    df.to_csv(df_filename, index=False)

    simDAG = CausalGraphicalModel(
        nodes=["A", "C", "M", "L", "Y"],
        edges=[("A", "Y"), ("A", "M"), ("A", "L"), ("C", "A"), ("C", "M"), ("C", "L"), ("C", "Y"), ("M", "Y"),
               ("L", "M"), ("L", "Y")])

    df_cDAG = nx.to_pandas_adjacency(simDAG.dag, dtype=int)
    df_cDAG.to_csv(path + dataset_name + '_DAG.csv')

    process(path=path, dataset_name=dataset_name, dag_name=dataset_name + '_DAG', test_size=0.2, cat_var=None, seed=None)
    train(path=path, dataset_name=dataset_name, path_save =path + '128k_loop',
          trn_batch_size=128, val_batch_size=4096, learning_rate=1e-4, seed=None, nb_epoch=50000,
          emb_net=[100, 90, 80, 70, 60], int_net=[60, 50, 40, 30, 20], nb_estop=50, val_freq=1)

    pse_results_df = sim(path=path, dataset_name=dataset_name, path_save=path + '128k_loop', n_mce_samples=10000, treatment='A', cat_list=[0, 1],
       moderator=None, mediator=['L', 'M'], outcome='Y', inv_datafile_name='sim_pse_128k')

    med_results_df = sim(path=path, dataset_name=dataset_name, path_save=path + '128k_loop', n_mce_samples=10000, treatment='A', cat_list=[0, 1],
       moderator=None, mediator=['L'], outcome='M', inv_datafile_name='sim_med_128k')

    results_df = pd.concat([pse_results_df, med_results_df], ignore_index=True)

    values_list = results_df['Value'].tolist()

    end_time = time.time()
    time_taken = end_time - start_time

    values_list.extend([coef_LA, coef_MA, coef_ML, coef_YA, coef_YM, coef_YL, time_taken])

    return values_list
