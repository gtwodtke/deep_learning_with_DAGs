import numpy as np
import pandas as pd
import os
import networkx as nx
import time
from causalgraphicalmodels import CausalGraphicalModel
from cGNF.process_parallel import process
from cGNF.train_parallel import train
from cGNF.simulation_parallel import sim


def run_simulation(i, node_id):
    print(f"Running simulation {i} on Process ID: {os.getpid()}")
    start_time = time.time()

    data = pd.read_csv('/project/wodtke/cGNF_python_code/blau_duncan_1967/blau_duncan_1967_cgnf.csv')

    df = data.sample(n=len(data), replace=True)

    base_path = '/project/wodtke/cGNF_python_code/blau_duncan_1967/bootstrap'
    folder = f'DF_{node_id}_{i}'  # Note the use of i to create a unique folder for each iteration
    path = os.path.join(base_path, folder, '')
    dataset_name = 'blau_duncan_1967_cgnf'

    if not os.path.isdir(path):
        os.makedirs(path)

    df_filename = path + dataset_name + '.csv'
    df.to_csv(df_filename, index=False)

    simDAG = CausalGraphicalModel(
        nodes=["U", "V", "W", "X", "Y"],
        edges=[("V", "X"), ("V", "U"), ("X", "U"), ("X", "W"), ("X", "Y"), ("U", "W"), ("U", "Y"), ("W", "Y")])

    df_cDAG = nx.to_pandas_adjacency(simDAG.dag, dtype=int)
    df_cDAG.to_csv(path + dataset_name + '_DAG.csv')

    process(path=path, dataset_name=dataset_name, dag_name=dataset_name + '_DAG', test_size=0.2,
            cat_var=['U', 'V', 'W', 'X', 'Y'], seed=None)

    train(path=path, dataset_name=dataset_name, path_save=path + 'boostrap',
          trn_batch_size=128, val_batch_size=4096, learning_rate=1e-4, seed=None, nb_epoch=50000,
          emb_net=[100, 90, 80, 70, 60],
          int_net=[60, 50, 40, 30, 20], nb_estop=50, val_freq=1)

    # ATE of X on Y
    ate_xy_results_df=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'boostrap', n_mce_samples=10000, treatment='X',
        cat_list=list(range(97)), moderator=None, mediator=None, outcome='Y', inv_datafile_name='ATE_XY')
    )

    # ATE of U on Y
    ate_uy_results_df=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'boostrap', n_mce_samples=10000, treatment='U',
        cat_list=list(range(9)), moderator=None, mediator=None, outcome='Y', inv_datafile_name='ATE_UY')
    )

    ndenie_results_df_1=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'boostrap', n_mce_samples=10000, treatment='X',
        cat_list=[9, 14], moderator=None, mediator=['U'], outcome='Y', inv_datafile_name='NDENIE')
    )

    ndenie_results_df_2=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'boostrap', n_mce_samples=10000, treatment='X',
        cat_list=[14, 18], moderator=None, mediator=['U'], outcome='Y', inv_datafile_name='NDENIE')
    )

    ndenie_results_df_3=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'boostrap', n_mce_samples=10000, treatment='X',
        cat_list=[18, 41], moderator=None, mediator=['U'], outcome='Y', inv_datafile_name='NDENIE')
    )

    ndenie_results_df_4=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'boostrap', n_mce_samples=10000, treatment='X',
        cat_list=[41, 61], moderator=None, mediator=['U'], outcome='Y', inv_datafile_name='NDENIE')
    )

    results_df = pd.concat([ate_xy_results_df, ate_uy_results_df, ndenie_results_df_1, ndenie_results_df_3, ndenie_results_df_3, ndenie_results_df_4], ignore_index=True)

    values_list = results_df['Value'].tolist()

    end_time = time.time()
    time_taken = end_time - start_time

    values_list.append(time_taken)

    return values_list
