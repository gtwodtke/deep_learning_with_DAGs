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

    data = pd.read_csv('/project/wodtke/cGNF_python_code/zhou_2019/zhou_2019_cgnf.csv')

    df = data.sample(n=len(data), replace=True)

    base_path = '/project/wodtke/cGNF_python_code/zhou_2019/bootstrap'
    folder = f'DF_{node_id}_{i}'  # Note the use of i to create a unique folder for each iteration
    path = os.path.join(base_path, folder, '')
    dataset_name = 'zhou_2019_cgnf'

    if not os.path.isdir(path):
        os.makedirs(path)

    df_filename = path + dataset_name + '.csv'
    df.to_csv(df_filename, index=False)

    # DAG SPECIFICATION
    simDAG = CausalGraphicalModel(
        nodes=["Y", "X", "C", "S", "F", "H", "B", "U", "A", "L", "M", "N"],
        edges=[("X", "Y"),
               ("X", "C"),
               ("C", "Y"),
               ("X", "A"), ("X", "L"),
               ("A", "C"), ("A", "Y"),
               ("L", "C"), ("L", "Y"),
               ("L", "A"),
               ("S", "X"), ("F", "X"), ("H", "X"), ("B", "X"), ("U", "X"), ("M", "X"), ("N", "X"),
               ("S", "A"), ("S", "L"), ("S", "C"), ("S", "Y"),
               ("F", "A"), ("F", "L"), ("F", "C"), ("F", "Y"),
               ("H", "A"), ("H", "L"), ("H", "C"), ("H", "Y"),
               ("B", "A"), ("B", "L"), ("B", "C"), ("B", "Y"),
               ("U", "A"), ("U", "L"), ("U", "C"), ("U", "Y"),
               ("M", "A"), ("M", "L"), ("M", "C"), ("M", "Y"),
               ("N", "A"), ("N", "L"), ("N", "C"), ("N", "Y"), ])

    print(simDAG.draw())  # Draws and prints the DAG.

    # Converts the DAG to a pandas adjacency matrix.
    df_cDAG = nx.to_pandas_adjacency(simDAG.dag, dtype=int)

    print("------- Adjacency Matrix -------")
    print(df_cDAG)  # Prints the adjacency matrix.

    # Saves the adjacency matrix to a csv file.
    df_cDAG.to_csv(path + dataset_name + '_DAG.csv')

    process(path=path, dataset_name=dataset_name, dag_name=dataset_name + '_DAG', test_size=0.2,
            cat_var=['C', 'S', 'F', 'H', 'B', 'U', 'L', 'M', 'N'], seed=None)

    train(path=path, dataset_name=dataset_name, path_save=path + 'point',  # General parameters
          trn_batch_size=128, val_batch_size=4096, learning_rate=1e-4, seed=None, nb_epoch=50000,
          emb_net=[100, 90, 80, 70, 60],
          int_net=[60, 50, 40, 30, 20], nb_estop=50, val_freq=1)

    # Conditional mobility
    conditional=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'point', n_mce_samples=10000, treatment='X',
        cat_list=[0.14, 0.65], moderator='C', mediator=None, outcome='Y', inv_datafile_name='conditional')
    )

    # Controlled mobility
    controlled_1=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'point', n_mce_samples=10000, treatment='X',
        cat_list=[0.14, 0.65], moderator=None, mediator=['C=1'], outcome='Y', inv_datafile_name='controlled_1')
    )

    controlled_0=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'point', n_mce_samples=10000, treatment='X',
        cat_list=[0.14, 0.65], moderator=None, mediator=['C=0'], outcome='Y', inv_datafile_name='controlled_0')
    )

    # Path-specific effects
    pse=(
        sim(path=path, dataset_name=dataset_name, path_save=path + 'point', n_mce_samples=10000, treatment='X',
        cat_list=[0.14, 0.65], moderator=None, mediator=['L', 'A', 'C'], outcome='Y', inv_datafile_name='PSE')
    )

    results_df = pd.concat([conditional, controlled_1, controlled_0, pse], ignore_index=True)

    values_list = results_df['Value'].tolist()

    end_time = time.time()
    time_taken = end_time - start_time

    values_list.append(time_taken)

    return values_list
