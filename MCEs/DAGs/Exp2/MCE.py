import numpy as np
import pandas as pd
import os
import networkx as nx
import time
from causalgraphicalmodels import CausalGraphicalModel
from processing_parallel import process
from training_parallel import train
from simulation_parallel_new import sim

def run_simulation(i, node_id):
    print(f"Running simulation {i} on Process ID: {os.getpid()}")
    start_time = time.time()
    obs = 32000

    # Baseline Confounders
    C2 = np.random.normal(0, 1, obs)
    C1 = np.random.normal(0, 1, obs) + C2

    # Logistic transformation
    logit_A = 0.1 * C1
    prob_A = 1 / (1 + np.exp(-logit_A))

    # Generate binary A
    A = np.random.binomial(1, prob_A, obs)

    # Error for Y
    epsilon_Y = np.random.normal(0, 1, obs)

    # Standard normal Y
    Y = 0.1 * A + 0.1 * C2 + 0.3 * C1 + 0.2 * A * C1 * C2 + epsilon_Y

    # pack into a dataframe
    df = pd.DataFrame(data={'C1': C1, 'C2': C2, 'A': A, 'Y': Y})

    base_path = '/project/wodtke/cGNF_python_code/32k'
    folder = f'DF_{node_id}_{i}'  # Note the use of i to create a unique folder for each iteration
    path = os.path.join(base_path, folder, '')
    dataset_name = 'DF1_32k_loop'

    if not os.path.isdir(path):
        os.makedirs(path)

    df_filename = path + dataset_name + '.csv'
    df.to_csv(df_filename, index=False)

    simDAG = CausalGraphicalModel(
        nodes=["C1", "C2", "A", "Y"],
        edges=[("C1", "C2"), ("C1", "A"), ("C2", "A"), ("C1", "Y"), ("C2", "Y"), ("A", "Y")])

    df_cDAG = nx.to_pandas_adjacency(simDAG.dag, dtype=int)
    df_cDAG.to_csv(path + dataset_name + '_DAG.csv')

    process(path=path, dataset_name=dataset_name, dag_name=dataset_name + '_DAG', test_size=0.2, cat_var=['A'], seed=None)
    train(path=path, dataset_name=dataset_name, model_name =path + '32k_loop',
          trn_batch_size=128, val_batch_size=4096, learning_rate=1e-4, seed=None, nb_epoch=50000,
          emb_net=[100, 90, 80, 70, 60], int_net=[60, 50, 40, 30, 20], nb_estop=50, val_freq=1)

    ate_results_df = sim(path=path, dataset_name=dataset_name, model_name=path + '32k_loop', n_mce_samples=100000, treatment='A', cat_list=[0, 1],
       moderator=None, mediator=None, outcome='Y', inv_datafile_name='sim_ate_32k')

    results_df = pd.concat([ate_results_df], ignore_index=True)

    values_list = results_df['Value'].tolist()

    end_time = time.time()
    time_taken = end_time - start_time

    values_list.append(time_taken)

    return values_list
