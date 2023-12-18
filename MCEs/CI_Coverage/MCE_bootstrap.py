import numpy as np
import pandas as pd
import os
import networkx as nx
import time
from causalgraphicalmodels import CausalGraphicalModel
from processing_parallel import process
from training_parallel import train
from simulation_parallel import sim


def run_simulation(i, node_id, n):
    print(f"Running simulation {i} on Process ID: {os.getpid()}")
    start_time = time.time()

    data = pd.read_csv(f'/project/wodtke/cGNF_python_code/MCE_bootstrap/MCE_{n}/8k.csv')
    dag = pd.read_csv(f'/project/wodtke/cGNF_python_code/MCE_bootstrap/MCE_{n}/8k_DAG.csv')

    df = data.sample(n=len(data), replace=True)

    base_path = f'/project/wodtke/cGNF_python_code/MCE_bootstrap/MCE_{n}/bootstrap'
    folder = f'DF_{node_id}_{i}'  # Note the use of i to create a unique folder for each iteration
    path = os.path.join(base_path, folder, '')
    dataset_name = '8k'

    if not os.path.isdir(path):
        os.makedirs(path)

    df_filename = path + dataset_name + '.csv'
    dag_filename = path + dataset_name + '_DAG.csv'
    df.to_csv(df_filename, index=False)
    dag.to_csv(dag_filename, index=False)

    process(path=path, dataset_name=dataset_name, dag_name=dataset_name + '_DAG', test_size=0.2,
            cat_var=['C', 'A'], seed=None)

    train(path=path, dataset_name=dataset_name, model_name=path + 'boostrap',
          trn_batch_size=128, val_batch_size=4096, learning_rate=1e-4, seed=None, nb_epoch=50000,
          emb_net=[100, 90, 80, 70, 60],
          int_net=[60, 50, 40, 30, 20], nb_estop=50, val_freq=1)

    # ATE of X on Y
    ate_results_df=(
        sim(path=path, dataset_name=dataset_name, model_name=path + 'boostrap', n_mce_samples=10000, treatment='A',
        cat_list=[0, 1], moderator=None, mediator=None, outcome='Y', inv_datafile_name='ATE')
    )

    results_df = pd.concat([ate_results_df], ignore_index=True)

    values_list = results_df['Value'].tolist()

    end_time = time.time()
    time_taken = end_time - start_time

    values_list.append(time_taken)

    return values_list