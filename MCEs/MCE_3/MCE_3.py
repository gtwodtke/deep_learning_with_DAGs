import numpy as np
import pandas as pd
import os
import networkx as nx
import time
import re
from causalgraphicalmodels import CausalGraphicalModel
from cGNF.processing_parallel import process
from cGNF.training_parallel import train
from cGNF.simulation_parallel import sim


def run_simulation(i, node_id):
    print(f"Running simulation {i} on Process ID: {os.getpid()}")
    start_time = time.time()
    obs = 128000

    # Define probabilities for C
    prob_C = [0.3, 0.5, 0.2]  # Probabilities for C taking values 1, 2, and 3
    C = np.random.choice([1, 2, 3], size=obs, p=prob_C)

    # Treatment A, binary, influenced by C
    prob_A = 0.3 + 0.1 * C  # Probability influenced by C
    A = np.random.binomial(1, prob_A, obs)

    # Define conditions for L
    def assign_L(C_val, A_val):
        if A_val == 1:
            if C_val == 1:
                return np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])
            elif C_val == 2:
                return np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
            else:  # C_val == 3
                return np.random.choice([1, 2, 3], p=[0.2, 0.3, 0.5])
        else:  # A_val == 0
            return np.random.choice([1, 2, 3], p=[0.6, 0.2, 0.2])

    # Assign L based on C and A
    L = np.array([assign_L(c, a) for c, a in zip(C, A)])

    # Mediator M, binary, with non-linear interaction
    # Logistic transformation to ensure binary outcome
    logit_M = -0.5 + 0.4 * A + 0.2 * C + 0.3 * L
    prob_M = 1 / (1 + np.exp(-logit_M))  # Sigmoid function for binary conversion
    M = np.random.binomial(1, prob_M, obs)

    # Outcome Y, binary, with interaction and non-linear terms
    # Logistic transformation to ensure binary outcome
    logit_Y = -0.5 + 0.3 * A + 0.1 * C + 0.3 * M + 0.3 * A * M + 0.3 * L
    prob_Y = 1 / (1 + np.exp(-logit_Y))  # Sigmoid function for binary conversion
    Y = np.random.binomial(1, prob_Y, obs)

    # pack into a dataframe
    df = pd.DataFrame({'A': A, 'C': C, 'M': M, 'L': L, 'Y': Y})

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

    process(path=path, dataset_name=dataset_name, dag_name=dataset_name + '_DAG', test_size=0.2, cat_var=["A", "C", "M", "L", "Y"], seed=None)
    train(path=path, dataset_name=dataset_name, model_name =path + '128k_loop',
          trn_batch_size=128, val_batch_size=4096, learning_rate=1e-4, seed=None, nb_epoch=50000,
          emb_net=[100, 90, 80, 70, 60], int_net=[60, 50, 40, 30, 20], nb_estop=50, val_freq=1)

    pse_results_df = sim(path=path, dataset_name=dataset_name, model_name=path + '128k_loop', n_mce_samples=10000, treatment='A', cat_list=[0, 1],
       moderator=None, mediator=['L', 'M'], outcome='Y', inv_datafile_name='sim_pse_128k')

    med_results_df = sim(path=path, dataset_name=dataset_name, model_name=path + '128k_loop', n_mce_samples=10000, treatment='A', cat_list=[0, 1],
       moderator=None, mediator=['L'], outcome='M', inv_datafile_name='sim_med_128k')

    results_df = pd.concat([pse_results_df, med_results_df], ignore_index=True)

    values_list = results_df['Value'].tolist()

    end_time = time.time()
    time_taken = end_time - start_time

    values_list.extend([time_taken])

    return values_list
